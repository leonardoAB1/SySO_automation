import os
import openai
import pandas as pd
import numpy as np
from IPython.display import display, Markdown
import questionary
from questionary import select

openai.api_key = os.environ['SYS_OPENIA_API_KEY']

class gestion_program(pd.DataFrame):
    def __init__(self, IPER):
        peligros = IPER['PELIGRO_x000D_\n_x000D_\n(Evento Peligroso, categorias de Lista Maestra OST-SGI.SI.001)'].unique()
        sectores = IPER['SECTOR / AREA / UNIDAD / PROCESO O SUB-PROCESO'].unique()
        
        # Crear DataFrame con las columnas especificadas
        super().__init__(columns=['# PLANILLA IDENTIFICACIÓN  Y EVALUACIÓN', 'OBJETIVO',
                                 'PELIGRO RELACIONADO', 'SECTOR / AREA / UNIDAD / PROCESO O SUB-PROCESO', 'ACTIVIDAD / TAREA / LUGAR / EQUIPO / EVENTO',
                                 'META', 'ACTIVIDAD',
                                 'RESPONSABLE EJECUCIÓN', 'RECURSOS (Bs)', 'PLAZOS (Dias)',
                                 'RESPONSABLE SEGUIMIENTO', 'AVANCE DE  SEGUIMIENTO %'])
        self.index.name = '#'

        # Generar filas por combinación de sector y peligro
        for peligro in peligros:
            objetivo = self.generate_objective(peligro)

            for sector in sectores:
                indices = IPER[(IPER['SECTOR / AREA / UNIDAD / PROCESO O SUB-PROCESO'] == sector) &
                               (IPER['PELIGRO_x000D_\n_x000D_\n(Evento Peligroso, categorias de Lista Maestra OST-SGI.SI.001)'] == peligro)].index.tolist()
                
                subsectores = IPER[(IPER['SECTOR / AREA / UNIDAD / PROCESO O SUB-PROCESO'] == sector) &
                                          (IPER['PELIGRO_x000D_\n_x000D_\n(Evento Peligroso, categorias de Lista Maestra OST-SGI.SI.001)'] == peligro)]['ACTIVIDAD / TAREA / LUGAR / EQUIPO / EVENTO'].tolist()

                actividad = self.generate_activity(objetivo, sector, subsectores, peligro)

                self.loc[len(self)] = [', '.join(map(str, indices)), objetivo, peligro, sector, ', '.join(map(str, subsectores)), "100 % de Actividades Ejecutadas", actividad, '', '', '', '', '0.00']
        
        # Replace empty strings with NaN
        self['# PLANILLA IDENTIFICACIÓN  Y EVALUACIÓN'].replace('', np.nan, inplace=True)
        self['ACTIVIDAD / TAREA / LUGAR / EQUIPO / EVENTO'].replace('', np.nan, inplace=True)

        # Drop rows where '# PLANILLA IDENTIFICACIÓN  Y EVALUACIÓN' column is empty
        self.dropna(subset=['# PLANILLA IDENTIFICACIÓN  Y EVALUACIÓN'], inplace=True)
        self.dropna(subset=['ACTIVIDAD / TAREA / LUGAR / EQUIPO / EVENTO'], inplace=True)

    def generate_objective(self, peligro):
        # Llamar a la API de OpenAI para generar un objetivo conciso para el peligro dado
        prompt = f"Genera un objetivo de salud y seguridad en el trabajo en máximo 5 palabras que resuelva el peligro: {peligro}. \nNo empezar el texto con saltos de linea, signos de putnuación ni similar."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=20,
            n=1,
            stop=None,
            temperature=0.7
        )
        objective = response.choices[0].text.strip()

        return objective

    def generate_activity(self, objetivo, sector, subsectores, peligro):
        # Llamar a la API de OpenAI para generar una actividad enfocada en resolver 
        # los peligros en ese sector especificando los subsectores de cada indice involucrado.
        prompt = f"Genera en pocas palabras, el resumen de una actividad enfocada en resolver los peligros en el sector {sector}, especificando los subsectores: {', '.join(subsectores).lower()}, para alcanzar el objetivo: {objetivo}. Peligro relacionado: {peligro}. \nNo empezar el texto con saltos de linea, signos de putnuación ni similar."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=60,
            n=1,
            stop=None,
            temperature=0.9
        )
        activity = response.choices[0].text.strip()

        return activity

if __name__ == '__main__':  
    # Read the Excel file
    file_path = 'IPER_example.xlsx'
    iper = pd.read_excel(file_path)

    #Prepare file
    # Drop rows with NaN values
    iper = iper.dropna()
    iper = iper.set_index('#', drop=True)
    iper = iper.head()

    # Create an instance of gestion_program
    program = gestion_program(iper)

    # Save the instance to an Excel file
    filename = 'programa_de_gestion.xlsx'
    program.to_excel(filename, index=False)
    print(f"Programa de gestión guardado como {filename}")

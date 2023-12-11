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
        """
        Crea un programa de gestión a partir de los datos de la IPER.

        Argumentos:
        
        - IPER: DataFrame que contiene los datos del la Matriz IPER.

        """
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
        
        # Reemplazar cadenas vacías por NaN
        self['# PLANILLA IDENTIFICACIÓN  Y EVALUACIÓN'].replace('', np.nan, inplace=True)
        self['ACTIVIDAD / TAREA / LUGAR / EQUIPO / EVENTO'].replace('', np.nan, inplace=True)

        # Eliminar filas donde la columna '# PLANILLA IDENTIFICACIÓN  Y EVALUACIÓN' esté vacía
        self.dropna(subset=['# PLANILLA IDENTIFICACIÓN  Y EVALUACIÓN'], inplace=True)
        self.dropna(subset=['ACTIVIDAD / TAREA / LUGAR / EQUIPO / EVENTO'], inplace=True)

    def generate_objective(self, peligro):
        """
        Genera un objetivo de salud y seguridad en el trabajo basado en el peligro dado.

        Argumentos:
        - peligro: Peligro específico.

        Retorna:
        - Objetivo generado.

        """
        # Llamar a la API de OpenAI para generar un objetivo conciso para el peligro dado
        prompt = f"Genera un objetivo de salud y seguridad en el trabajo en máximo 5 palabras que resuelva el peligro: {peligro}. \nNo empezar el texto con saltos de linea, signos de putnuación ni similar."
        
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=20,
            n=1,
            stop=None,
            temperature=0.7
        )
        
        objective = response.choices[0].message["content"].strip()

        return objective

    def generate_activity(self, objetivo, sector, subsectores, peligro):
        """
        Genera una actividad enfocada en resolver los peligros en un sector específico, 
        especificando los subsectores involucrados.

        Argumentos:
        - objetivo: Objetivo de salud y seguridad en el trabajo.
        - sector: Sector específico.
        - subsectores: Lista de subsectores involucrados.
        - peligro: Peligro relacionado.

        Retorna:
        - Actividad generada.

        """
        # Llamar a la API de OpenAI para generar una actividad enfocada en resolver 
        # los peligros en ese sector especificando los subsectores de cada indice involucrado.
        prompt = f"Genera en pocas palabras, el resumen de una actividad enfocada en resolver los peligros en el sector {sector}, especificando los subsectores: {', '.join(subsectores).lower()}, para alcanzar el objetivo: {objetivo}. Peligro relacionado: {peligro}. \nNo empezar el texto con saltos de linea, signos de putnuación ni similar.\n Escribir la respuesta en futuro y con tono imperativo."
        
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=60,
            n=1,
            stop=None,
            temperature=0.9
        )

        activity = response.choices[0].message["content"].strip()

        return activity

if __name__ == '__main__':  
    # Leer el archivo Excel
    file_path = 'IPER_example.xlsx'
    iper = pd.read_excel(file_path)

    # Preparar el archivo
    # Eliminar filas con valores NaN
    iper = iper.dropna()
    iper = iper.set_index('#', drop=True)
    iper = iper.head()

    # Crear una instancia de gestion_program
    program = gestion_program(iper)

    # Guardar la instancia en un archivo Excel
    filename = 'programa_de_gestion.xlsx'
    program.to_excel(filename, index=True)
    print(f"Programa de gestión guardado como {filename}")

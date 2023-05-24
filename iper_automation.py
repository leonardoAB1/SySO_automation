import os
import openai
import pandas as pd
from IPython.display import display, Markdown
import questionary
from questionary import select


openai.api_key = os.environ['SYS_OPENIA_API_KEY']

class IPER_Row:
    '''
    Fila de la Matriz IPER.
    En términos simples, IPER es una descripción organizada de las actividades, 
    controles y peligros que permitan identificar los posibles riesgos. 
    Esta permitirá evaluar, monitorear, controlar y comunicar estos peligros 
    o sucesos no deseados, pudiendo también identificar los niveles de riesgo 
    y las consecuencias de estos.

    Los valores y definiciones de los distintos indicadores se describen a continuación:
        Índice de número de personas expuestas (self.INPE): Se determina en función de la cantidad de personas expuestas, en el lugar o entorno de trabajo.
        0: No aplica (NO existe exposición de personas, sólo de equipos/infraestructura)
        1: De 1 a 10 personas      
        2: De 11 a 20 personas
        3: Más de 20 personas

        Índice de Frecuencia y Duración de la exposición (self.IFDE): Considera dos variables, “Frecuencia” y “Duración” de la exposición según la siguiente tabla:
        Frecuencia de exposición del personal Duración de la exposición Índice 
        4: DIARIA o todos los días Menos del 50% del turno de trabajo
        5: DIARIA o todos los días Más del 50% del turno de trabajo
        3: SEMANALMENTE o todas las semanas (pero no se reitera cada día) Menos del 50% del turno de trabajo
        4: SEMANALMENTE o todas las semanas (pero no se reitera cada día) Más del 50% del turno de trabajo
        2: MENSUALMENTE (pero no se reitera cada semana) a SEMESTRALMENTE Menos del 50% del turno de trabajo 
        3: MENSUALMENTE (pero no se reitera cada semana) a SEMESTRALMENTE Más del 50% del turno de trabajo
        1: Se realiza con una frecuencia mayor a la SEMESTRAL Menos del 50% del turno de trabajo
        2: Se realiza con una frecuencia mayor a la SEMESTRAL Más del 50% del turno de trabajo
        2: Se está evaluando en Condiciones de Falla/no rutinaria o Anormales ó sólo se exponen equipos, no personas 

        Índice de Controles existentes (self.ICO)
        1: Existen controles implementados → Se tienen al menos tres condiciones implementadas (A, B, C ó D) 
        6: Existen controles parciales → Se tienen dos condiciones implementadas
        10: Los controles son bajos o insuficientes o no están implementados → 
        * Se cumple sólo una condición implementada o ninguna ó 
        * se identificaron "permanentes" desvíos comportamentales de incumplimiento a las normas referidas al peligro ó 
        * Es una evaluación "IPER anticipada para actividades" 

            Condiciones 
            Condicion A.  Existen ya implementados como parte del SGI procedimientos/documentos o controles operativos específself.ICOs para controlar el Peligro (p.e. PT, EPP, bloqueo/etiquetado, IT, guías, normas, inspecciones específicas).
            Condicion B.  Para el peligro específself.ICO existen implementados medios de infraestructura o ingeniería o protección colectiva o de emergencia para el Peligro (resguardos, barandas, cubiertas, líneas de vida, barreras de protección, aislamientos, medios de detección/alarma del peligro, dispositivos de enclavamiento/corte automátself.ICO, extintores, accesorios para mejorar la ergonomía, mantenimiento preventivo).
            Condicion C.  El personal ya tiene experiencia o fue capacitado/entrenado sobre el peligro específself.ICO al realizar la actividad.
            Condicion D. Se cuenta con señalización/alerta específica in-situ implementada para el peligro o situación peligrosa.

        Criterios de Severidad de Daño:
        1: "Daño Menor"
            - Lesiones que sólo requieren primeros auxilios o atención médica de seguimiento.
            - Lesiones/enfermedades que ocasionan ausencia laboral de menos de un día o transferencia de actividad por ese período.
            - Daños a equipos con costos estimados menores a 1,000 USD.

        2: "Daño Mediano"
            - Lesiones/enfermedades que ocasionan ausencia laboral temporal de 1 día a 1 mes o transferencia de actividad por ese período.
            - Daños a equipos con costos entre 1,001 y 10,000 USD.

        3: "Daño Mayor"
            - Lesiones que ocasionan ausencia laboral temporal de 1 mes a 6 meses o transferencia de actividad por ese período.
            - Lesiones/enfermedades que ocasionan "incapacidades permanentes parciales".
            - Daños a equipos con costos entre 10,001 y 100,000 USD.

        4: "Daño Extremo"
            - Lesiones/enfermedades que ocasionan ausencia laboral temporal de 6 meses a 1 año o transferencia de actividad por ese período.
            - Lesiones o enfermedades que generan "incapacidad total" al trabajador.
            - Muerte.
            - Daños a equipos con costos estimados superiores a 100,000 USD.
    '''
    def __init__(self, sector, subsector, implemented_controls,  problem_description):
        
        self.sector = sector # string
        self.subsector = subsector # string
        self.problem_description = problem_description # string
        self.implemented_controls = implemented_controls # list
        #self.person_count = person_count #int
        #self.usage_time = usage_time #int horas-semana

        # Indices
        self.INPE = self._get_inpe()
        self.IFDE = self._get_ifde() 
        self.ICO = self._get_ico()

        self.probabilidad = self._evaluar_probabilidad()
        self.nivel_de_riesgo = self._calcular_nivel_riesgo()
        self.aceptabilidad = self._evaluar_aceptabilidad()

        self.severidad_daño = self._get_severidad()
        self.string_severidad_daño = self._get_severidad_daño()

        self.condicion_evaluacion = self._elegir_condicion()
        self.peligro = self._seleccionar_peligro()
        self.origen_peligro = self._generar_origen_peligrp()
        self.controles_pre_existentes = self._generar_controles_pre_existentes() 

        self.opciones_peligro = {
            1: "A1. Caída de personas al mismo nivel",
            2: "A2. Caídas menores a distinto nivel (entre 0,3 y 1,8 m)",
            3: "A3. Caídas mayores a distinto nivel (mayor a 1,8 m)",
            4: "A4. Contactos eléctricos (Choque eléctrico)",
            5: "A5. Contactos con partes o elementos calientes/fríos",
            6: "A6. Proyección de partículas, fragmentos",
            7: "A7. Proyección de gases, polvo o líquidos a presión ó calientes",
            8: "A8. Atrapamientos mecánicos",
            9: "A9. Cortes, golpes, penetraciones por herramientas",
            10: "A10. Cortes, golpes, penetraciones, excoriaciones de otra clase (no por herramientas)",
            11: "A11. Caída de objetos menores (menos de 5 kg) o herramientas",
            12: "A12. Aplastamiento/Ahogamiento (entre objetos o por caída/deslizamiento de objetos mayores a 5 Kg)",
            13: "A13. Golpes por objetos/equipos móviles o atropellamiento por vehículos",
            14: "A14. Golpes por objetos inmóviles o partes salientes",
            15: "A15. Incendios",
            16: "A16. Explosiones / deflagraciones",
            17: "A17. Choques de vehículos en movimiento",
            18: "A18. Vuelcos vehiculares o de equipo",
            19: "A19. Exposición a ruido",
            20: "A20. Exposición a vibraciones",
            21: "A21. Exposición a inadecuada iluminación",
            22: "A22. Exposición a temperaturas extremas (extremadamente mayor a la normal o menor a 0°C)",
            23: "A23. Exposición a humedad extrema",
            24: "A24. Exposición a radiaciones ionizantes",
            25: "A25. Exposición a radiaciones no ionizantes",
            26: "B1. Contacto o ingestión de sólidos/líquidos peligrosos",
            27: "B2. Exposición a polvos o fibras",
            28: "B3. Exposición a gases/vapores tóxicos o asfixiantes",
            29: "B4. Derrames o fugas mayores de sustancias peligrosas",
            30: "B5. Exposición a insectos/animales peligrosos",
            31: "B6. Exposición a bacterias, virus u hongos",
            32: "C1. Ejecución de posturas inadecuadas",
            33: "C2. Ejecución de movimientos repetitivos",
            34: "C3. Ejecución de sobre esfuerzo físicos",
            35: "C4. Exposición a sobre esfuerzo visual",
            36: "C5. Exposición a sobre esfuerzo mental",
            37: "D1. Sismos",
            38: "D2. Inundaciones (por lluvias o granizadas intensas o desborde de ríos)",
            39: "D3. Tormentas eléctricas o de vientos huracanados",
            40: "D4. Deslizamientos de tierra",
            41: "D5. Incendios de plantas aledañas o forestales",
            42: "D6. Convulsión social"
        }

    def _evaluar_probabilidad(self):
        '''
        Evalúa la probabilidad de riesgo en función de los indicadores.

        Args:
            self.INPE (int): Índice de número de personas expuestas. (0-3)
            self.IFDE (int): Índice de Frecuencia y Duración de la exposición. (1-5)
            self.ICO (int): Índice de Controles existentes. (1, 6, 10)

        Returns:
            int: Valor de la probabilidad de riesgo (1-5) o None si no se cumple ninguna condición.
        '''
        suma = self.INPE + self.IFDE + self.ICO
        if suma <= 6:
            return 1
        elif suma <= 10:
            return 2
        elif suma <= 14:
            return 3
        elif suma <= 18:
            return 4
        elif suma > 18:
            return 5
        else:
            return None

    def _calcular_nivel_riesgo(self):
        '''
        Calcula el nivel de riesgo en función de la probabilidad y la severidad del daño.

        Args:
            self.probabilidad (int): Valor de la probabilidad de riesgo (1-5).
            self.severidad_daño (int): Valor de la severidad del daño (1-5).

        Returns:
            str: Nivel de riesgo ("Trivial", "Bajo", "Moderado", "Alto" o "Intolerable").
        '''
        resultado = self.probabilidad * self.severidad_daño
        nivel = ""
        if resultado <= 2:
            nivel = "Trivial"
        elif resultado <= 6:
            nivel = "Bajo"
        elif resultado <= 9:
            nivel = "Moderado"
        elif resultado <= 15:
            nivel = "Alto"
        elif resultado >= 16:
            nivel = "Intolerable"

        return nivel

    def _evaluar_aceptabilidad(self):
        '''
        Evalúa la aceptabilidad del riesgo en función de la probabilidad y la severidad del daño.

        Args:
            self.probabilidad (int): Valor de la probabilidad de riesgo (1-5).
            self.severidad_daño (int): Valor de la severidad del daño (1-5).

        Returns:
            str: Aceptabilidad del riesgo ("Aceptable" o "No Aceptable").
        '''
        resultado = self.probabilidad * self.severidad_daño
        nivel = ""
        if resultado > 7:
            nivel = "No Aceptable"
        else:
            nivel = "Aceptable"

        return nivel

    def _elegir_condicion(self):

        # Define the prompt using self.problem_description
        prompt = f"""Selecciona la condición más adecuada basada en la siguiente descripción:

        Descripción del problema: 
        {self.problem_description}

        Opciones de condición:
        0. Normal/Rutinaria
        1. Anormal/Emergencia/No rutinaria
        """

        # Generate a response using the ChatGPT API
        response = openai.Completion.create(
            engine='davinci',
            prompt=prompt,
            max_tokens=1,
            n=1,
            stop=None,
            temperature=0,
        )

        # Extract the selected option (con_eval) from the generated response
        con_eval = int(response.choices[0].text.strip())

        if con_eval == 0:
            return "Normal/Rutinaria"
        elif con_eval == 1:
            return "Anormal/Emergencia/No rutinaria"
        else:
            return None

    def _seleccionar_peligro(self):
        # Define the prompt using self.problem_description and opciones_peligro
        prompt = f"""Selecciona el peligro más adecuado basado en la siguiente descripción:

        Descripción del problema: {self.problem_description}

        Opciones de peligro:
        {self.opciones_peligro}
        """

        # Generate a response using the ChatGPT API
        response = openai.Completion.create(
            engine='davinci',
            prompt=prompt,
            max_tokens=1,
            n=1,
            stop=None,
            temperature=0,
        )

        # Extract the selected option (key) from the generated response
        selected_option = int(response.choices[0].text.strip())

        return selected_option

    def _generar_origen_peligro(self):
        pass

    def _generar_controles_pre_existentes(self):
        pass
    
    def _get_severidad(self):
        daño_menor = [1, 2, 5, 9, 10, 14, 19, 20, 21, 22, 23, 25, 29, 30, 31, 32, 33, 34, 35, 36, 39, 40, 41, 42]
        daño_mediano = [3, 4, 7, 8, 13, 17, 18, 24, 27, 37]
        daño_mayor = [6, 11, 16, 26, 38]
        daño_extremo = [15, 25]

        if self.peligro in daño_menor:
            return 1 
        elif self.peligro in daño_mediano:
            return 2 
        elif self.peligro in daño_mayor:
            return 3 
        elif self.peligro in daño_extremo:
            return 4
        else:
            return 0
    
    def _get_severidad_daño(self):
        daño_menor = [1, 2, 5, 9, 10, 14, 19, 20, 21, 22, 23, 25, 29, 30, 31, 32, 33, 34, 35, 36, 39, 40, 41, 42]
        daño_mediano = [3, 4, 7, 8, 13, 17, 18, 24, 27, 37]
        daño_mayor = [6, 11, 16, 26, 38]
        daño_extremo = [15, 25]

        if self.peligro in daño_menor:
            return 'daño menor'
        elif self.peligro in daño_mediano:
            return 'daño mediano'
        elif self.peligro in daño_mayor:
            return 'daño mayor'
        elif self.peligro in daño_extremo:
            return 'daño extremo'
        else:
            return 0

    def _get_inpe(self):
        opciones_cantidad = [
            'No aplica (NO existe exposición de personas, sólo de equipos/infraestructura',
            'De 1 a 10 personas',
            'De 11 a 20 personas',
            'Más de 20 personas'
            ]

        cantidad = select('Selecciona una opción', choices=opciones_cantidad).ask()

        if cantidad == 'De 1 a 10 personas':
            return 1
        elif cantidad == 'De 11 a 20 personas':
            return 3
        elif cantidad == 'Más de 20 personas':
            return 5
        else:
            return None

        
    def _get_ifde(self):
        opciones_frecuencia = [
        'DIARIA o todos los días',
        'SEMANALMENTE o todas las semanas (pero no se reitera cada día)',
        'MENSUALMENTE (pero no se reitera cada semana) a SEMESTRALMENTE',
        'Se realiza con una frecuencia mayor a la SEMESTRAL',
        'Se está evaluando en Condiciones de Falla/no rutinaria o Anormales ó sólo se exponen equipos, no personas'
        ]

        opciones_duracion = [
            'Menos del 50% del turno de trabajo',
            'Más del 50% del turno de trabajo'
            ]

        frecuencia = select('Selecciona una opción', choices=opciones_frecuencia).ask()

        if frecuencia == 'DIARIA o todos los días':
            duracion = select('Selecciona una opción', choices=opciones_duracion).ask()
            if duracion == 'Menos del 50% del turno de trabajo':
                return 4
            else:
                return 5
        elif frecuencia == 'SEMANALMENTE o todas las semanas (pero no se reitera cada día)':
            duracion = select('Selecciona una opción', choices=opciones_duracion).ask()
            if duracion == 'Menos del 50% del turno de trabajo':
                return 3
            else:
                return 4
        elif frecuencia == 'MENSUALMENTE (pero no se reitera cada semana) a SEMESTRALMENTE':
            duracion = select('Selecciona una opción', choices=opciones_duracion).ask()
            if duracion == 'Menos del 50% del turno de trabajo':
                return 2
            else:
                return 3
        elif frecuencia == 'Se realiza con una frecuencia mayor a la SEMESTRAL':
            duracion = select('Selecciona una opción', choices=opciones_duracion).ask()
            if duracion == 'Menos del 50% del turno de trabajo':
                return 1
            else:
                return 2
        elif frecuencia == 'Se está evaluando en Condiciones de Falla/no rutinaria o Anormales ó sólo se exponen equipos, no personas':
            return 2
        else:
            return None
        

    def _get_ico(self):
            x = len(self.implemented_controls)
            if x == 3:
                return 1 
            elif x == 2:
                return 6
            elif x == 1:
                return 10
        
if __name__ == "__main__":
    while():
        sector= input("Define el sector: ")
        subsector= input("Define el area: ")
        problem_description = input("Define el area: ")
        person_count = None
        usage_time = None
        implemented_controls = None
        print('')
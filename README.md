# Programa de Salud y Seguridad en el Trabajo

Este proyecto tiene como objetivo automatizar el proceso de generación de un programa de salud y seguridad en el trabajo. Un programa de salud y seguridad en el trabajo es esencial para garantizar un entorno laboral seguro y saludable para todos los empleados.

## Características principales

- Generación automatizada: Este programa utiliza algoritmos y técnicas de procesamiento de lenguaje natural para generar automáticamente un programa de salud y seguridad en el trabajo basado en parámetros específicos. Esto incluye, pero no se limita a generar la matriz de IPER para la identificación y gestión de riesgos.
- Personalización: Permite personalizar el programa según las necesidades y requisitos de la organización. Se pueden agregar secciones y políticas adicionales, así como modificar las existentes.
- Cumplimiento normativo: El programa generado se basa en las regulaciones y normativas locales de salud y seguridad en el trabajo, asegurando el cumplimiento legal.
- Documentación detallada: Proporciona una documentación detallada de las políticas, procedimientos y medidas de seguridad incluidas en el programa.

## Instalación

1. Clona el repositorio a tu máquina local.
2. Asegúrate de tener instalado Python 3.
3. Instala las dependencias necesarias ejecutando el siguiente comando:

   ```
   pip install -r requirements.yml
   ```

4. Configura la variable de entorno del sistema con el nombre 'SYS_OPENIA_API_KEY' y asigna tu API key de OpenAI como valor. Puedes solicitar tu API key personal en la dirección: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys).

   **En Windows:**
   
   - Abre el menú de inicio y busca "Variables de entorno".
   - Selecciona "Editar las variables de entorno del sistema".
   - Haz clic en el botón "Variables de entorno".
   - En la sección "Variables del sistema", crea la variable "SYS_OPENIA_API_KEY" y haz clic en "Editar".
   - Ingresa tu API key de OpenAI en el campo "Valor de la variable".
   - Haz clic en "Aceptar" para guardar los cambios.

5. Ejecuta el programa utilizando el siguiente comando:

   ```
   python generar_programa_gestion.py
   ```

## Instalación de Conda

Conda es un sistema de gestión de paquetes y un entorno virtual para Python. Aquí tienes los pasos para instalar Conda:

1. **Paso 1: Acceder al sitio web oficial de Conda:** Ve a la página de descargas de Conda en el sitio web oficial (https://docs.conda.io/en/latest/miniconda.html) en tu navegador web.

2. **Paso 2: Descargar el instalador de Miniconda:** En la página de descargas, encontrarás diferentes versiones de Conda. Elige la versión de Miniconda adecuada para tu sistema operativo (por ejemplo, Miniconda3 para Python 3.x). Haz clic en el enlace de descarga correspondiente.

3. **Paso 3: Ejecutar el instalador:** Una vez descargado el instalador de Miniconda, ábrelo y ejecútalo. Sigue las instrucciones del instalador. Asegúrate de marcar la opción "Add Anaconda to my PATH environment variable" (Agregar Anaconda a mi variable de entorno PATH) durante la instalación. Esto asegurará que puedas acceder a Conda desde cualquier ubicación en tu sistema.

4. **Paso 4: Verificar la instalación:** Abre una nueva línea de comandos (Terminal o Command Prompt) y escribe el siguiente comando:
   
   ```shell
   conda --version
   ```

   Esto mostrará la versión de Conda instalada en tu sistema. Si se muestra la versión correctamente, ¡has instalado Conda con éxito!

Espero que esta guía te sea útil. ¡Disfruta programando con Python y Conda!


## Licencia

Este proyecto se encuentra bajo la [Licencia MIT](LICENSE).

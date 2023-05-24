# Programa de Salud y Seguridad en el Trabajo

Este proyecto tiene como objetivo automatizar el proceso de generación de un programa de salud y seguridad en el trabajo. Un programa de salud y seguridad en el trabajo es esencial para garantizar un entorno laboral seguro y saludable para todos los empleados.

## Características principales

- Generación automatizada: Este programa utiliza algoritmos y técnicas de procesamiento de lenguaje natural para generar automáticamente un programa de salud y seguridad en el trabajo basado en parámetros específicos. Esto incluye, pero no se limita a generar la matriz de IPER para la identificación y gestión de riesgos.
- Personalización: Permite personalizar el programa según las necesidades y requisitos de la organización. Se pueden agregar secciones y políticas adicionales, así como modificar las existentes.
- Cumplimiento normativo: El programa generado se basa en las regulaciones y normativas locales de salud y seguridad en el trabajo, asegurando el cumplimiento legal.
- Documentación detallada: Proporciona una documentación detallada de las políticas, procedimientos y medidas de seguridad incluidas en el programa.
- Formato Markdown: El programa se genera en formato Markdown, lo que permite una fácil visualización, edición y exportación a otros formatos, como PDF.

## Instalación

1. Clona el repositorio a tu máquina local.
2. Asegúrate de tener instalado Python 3.
3. Instala las dependencias necesarias ejecutando el siguiente comando:

   ```
   pip install -r requirements.yml
   ```

4. Ejecuta el programa utilizando el siguiente comando:

   ```
   python generar_programa_gestion.py
   ```

## Uso

1. Abre el archivo `IPER_example.xlsx` y asegúrate de que contenga los datos correctos para la generación del programa de gestión.
2. Ejecuta el programa utilizando el comando mencionado anteriormente.
3. El programa generará automáticamente el archivo `programa_de_gestion.xlsx` con el programa de gestión en formato Excel.

## Contribución

¡Las contribuciones son bienvenidas! Si deseas contribuir a este proyecto, sigue estos pasos:

1. Haz un fork de este repositorio.
2. Crea una rama con la nueva funcionalidad: `git checkout -b mi-nueva-funcionalidad`.
3. Realiza los cambios necesarios y haz commit: `git commit -m "Agregar nueva funcionalidad"`.
4. Envía los cambios a tu repositorio fork: `git push origin mi-nueva-funcionalidad`.
5. Abre un pull request en este repositorio.

## Licencia

Este proyecto se encuentra bajo la [Licencia MIT](LICENSE).

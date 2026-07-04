import matplotlib.pyplot as plt
import os

# Obtener la ruta del directorio donde se encuentra el script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Configurar matplotlib para usar el backend PGF
plt.rcParams.update({
    "pgf.texsystem": "pdflatex",  # Cambiar a "xelatex" o "lualatex" si prefieres
    "font.family": "serif",
    "text.usetex": True,
    "pgf.rcfonts": False,
})

# Datos de la distribución
labels = ['Planificación', 'Comité Mixto', 'Estudios de Higiene', 'Plan de Emergencia', 'Otras Actividades(9)']
sizes = [40, 10, 10, 20, 20]
#colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']  # Colores opcionales para cada sector

# Crear el gráfico
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.0f\\%%', startangle=90, 
            wedgeprops = {"edgecolor" : "black", 
                        'linewidth': 1, 
                        'antialiased': True})

# Igualar el aspecto para que el gráfico sea circular
ax.axis('equal')

# Título del gráfico
#plt.title('Distribución del Presupuesto')

# Guardar el gráfico en formato PGF en el mismo directorio que el script
output_path = os.path.join(script_dir, 'grafico_distribucion.png')
plt.savefig(output_path)

# Mostrar el gráfico
#plt.show()

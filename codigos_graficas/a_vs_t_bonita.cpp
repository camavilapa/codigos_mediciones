import matplotlib.pyplot as plt
import numpy as np

# 1. CARGA DE DATOS DESDE EL ARCHIVO .TXT
# 'unpack=True' sirve para separar las columnas directamente en tiempo y aceleracion.
archivo1 = 'espuma_con_sin/Conespuma_definitivo.txt'
nombre_grafica = 'variando_Espuma/a_Con2.png'

tiempo, aceleracion = np.loadtxt(f'datos/{archivo1}', delimiter='\t', unpack=True)

# 2. CONVERSIÓN DE MILISEGUNDOS A SEGUNDOS
# Al ser un array de NumPy, podemos dividir todo el vector entre 1000 directamente.
tiempo = tiempo / 1000

# 3. DETECCIÓN DEL VALOR PICO (máximo absoluto de la señal)
# Usamos el valor absoluto para detectar el pico sin importar si es positivo o negativo
indice_pico = np.argmax(np.abs(aceleracion))
tiempo_pico = tiempo[indice_pico]
valor_pico = aceleracion[indice_pico]


# 4. CONFIGURACIÓN Y CREACIÓN DE LA GRÁFICA
# Ajustamos el tamaño de la figura (ancho, alto)
fig, ax = plt.subplots(figsize=(8, 5))

# Graficamos con una línea negra ('black') y un grosor estilizado
# líneas: ax.plot(tiempo, aceleracion, color='black', linewidth=1)
# puntos: ax.plot(tiempo, aceleracion, 'o', color='black', markersize=2.5, alpha=0.6, markeredgewidth=0)
ax.plot(tiempo, aceleracion, marker='o', color='#1f77b4', markersize=3, linewidth=0.9, alpha=1, markeredgewidth=0)





# --- MARCAMOS EL VALOR PICO ---
# Punto rojo sobre el pico para destacarlo
ax.plot(tiempo_pico, valor_pico, 'o', color="#E91E8C", markersize=4, zorder=5)

# Etiqueta con el valor exacto del pico (ej. "0.85 g")
# xytext desplaza el texto para que no tape la línea ni el punto
ax.annotate(f"{valor_pico:.3f} m s$^{{-2}}$",
            xy=(tiempo_pico, valor_pico),
            xytext=(10, 10),
            textcoords='offset points',
            fontsize=10,
            fontweight='bold',
            color='#212021',
            #arrowprops=dict(arrowstyle='->', color='#212021', lw=1)
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='none', alpha=0.9)
            )
            

# Títulos de los ejes (tamaño y estilo tomados de _bonita.py)
ax.set_xlabel('Tiempo (s)', fontsize=18, fontweight='bold', labelpad=18)
ax.set_ylabel(r"Aceleración ($\mathbf{m/s^2}$)", fontsize=18, fontweight='bold', labelpad=15)

# Cuadrícula del fondo (gris clara y sutil)
# ax.grid(True, linestyle='-', alpha=0.6, color='lightgray')

# Ticks en los cuatro lados, apuntando hacia adentro (estilo _bonita.py)
ax.tick_params(
    axis='both',
    which='major',0
    direction='in',
    top=True,
    right=True,
    length=7,
    width=1.0,
    labelsize=16
)

ax.tick_params(
    axis='both',
    which='minor',
    direction='in',
    top=True,
    right=True,
    length=3.5,
    width=0.8
)

ax.minorticks_on()

for spine in ax.spines.values():
    spine.set_linewidth(1.0)

# Ajustar márgenes automáticos para que no se corte ningún texto
plt.tight_layout()

# Guardar y mostrar la gráfica
plt.savefig(f'graficas/{nombre_grafica}', format='png', dpi=300)

print(f"Valor pico de aceleración: {valor_pico:.6f} g en t = {tiempo_pico:.4f} s")

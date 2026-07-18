import matplotlib.pyplot as plt
import numpy as np

# 1. CARGA DE DATOS DESDE EL ARCHIVO .TXT
# Cambia 'datos.txt' por el nombre real de tu archivo.
# 'unpack=True' sirve para separar las columnas directamente en tiempo y aceleracion.
archivo1 = 'espuma_con_sin/conespuma4.txt'
nombre_grafica = 'variando_Espuma/a_conespuma4.png'

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
fig, ax = plt.subplots(figsize=(6, 5.5))

# Graficamos con una línea negra ('black') y un grosor estilizado
# líneas: ax.plot(tiempo, aceleracion, color='black', linewidth=1)
# puntos: ax.plot(tiempo, aceleracion, 'o', color='black', markersize=2.5, alpha=0.6, markeredgewidth=0)
ax.plot(tiempo, aceleracion, marker='o', color='black', markersize=2.5, linewidth=0.7, alpha=0.7, markeredgewidth=0)





# --- MARCAMOS EL VALOR PICO ---
# Punto rojo sobre el pico para destacarlo
ax.plot(tiempo_pico, valor_pico, 'o', color="#EF2C2C", markersize=2.5, zorder=5)

# Etiqueta con el valor exacto del pico (ej. "0.85 g")
# xytext desplaza el texto para que no tape la línea ni el punto
ax.annotate(f"{valor_pico:.3f} g",
            xy=(tiempo_pico, valor_pico),
            xytext=(10, 10),
            textcoords='offset points',
            fontsize=10,
            fontweight='bold',
            color='#212021',
            #arrowprops=dict(arrowstyle='->', color='#212021', lw=1)
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='none', alpha=0.9)
            )
            

# Títulos de los ejes (idénticos a tu imagen)
ax.set_xlabel('Time (s)', fontsize=12, labelpad=8)
ax.set_ylabel('Acceleration (g)', fontsize=12, labelpad=8)

# Cuadrícula del fondo (gris clara y sutil)
ax.grid(True, linestyle='-', alpha=0.6, color='lightgray')

# Estilo de la caja (hacer las líneas del borde un poco más delgadas si se desea)
for spine in ax.spines.values():
    spine.set_linewidth(0.8)

# Añadir la etiqueta "a)" abajo en el centro de la figura
#fig.text(0.53, 0.02, 'a)', horizontalalignment='center', fontsize=18)

# Ajustar márgenes automáticos para que no se corte ningún texto
plt.tight_layout()
#plt.subplots_adjust(bottom=0.15)  # Deja espacio abajo para la letra "a)"

# Guardar y mostrar la gráfica
plt.savefig(f'graficas/{nombre_grafica}', format='png', dpi=300)

# Imprimir el valor pico en consola también, por si lo necesitas para tu reporte
print(f"Valor pico de aceleración: {valor_pico:.6f} g en t = {tiempo_pico:.4f} s")

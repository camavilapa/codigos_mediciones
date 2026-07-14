import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

# 1. CARGA Y PREPARACIÓN DE DATOS
archivo1 = 'datos_enY1.txt'
nombre_grafica = 'psd_5V.png'
tiempo, aceleracion = np.loadtxt(f'datos/{archivo1}', delimiter='\t', unpack=True)
tiempo = tiempo / 1000  # Convertir milisegundos a segundos

# 2. CÁLCULO DE LA FRECUENCIA DE MUESTREO Y PSD
dt = tiempo[1] - tiempo[0]
fs = 1.0 / dt 
frecuencias, psd = signal.welch(aceleracion, fs=fs, nperseg=1024)

# 3. DETECCIÓN AUTOMÁTICA DE LOS 3 PICOS DE RESONANCIA
# 'distance=10' evita que Python elija dos puntos que pertenezcan al mismo pico.
todos_los_picos, _ = signal.find_peaks(psd, distance=10)

# Filtramos los picos para buscar solo en el rango visible (0 a 50 Hz)
picos_en_rango = [p for p in todos_los_picos if 0 <= frecuencias[p] <= 50]

# Ordenamos los picos de mayor a menor magnitud (potencia) y nos quedamos con los 3 más altos
picos_ordenados_por_magnitud = sorted(picos_en_rango, key=lambda x: psd[x], reverse=True)
top_3_picos = picos_ordenados_por_magnitud[:1]

# Los volvemos a ordenar, pero esta vez por frecuencia (de izquierda a derecha) para el gráfico
top_3_picos = sorted(top_3_picos)


# 4. CONFIGURACIÓN Y CREACIÓN DE LA GRÁFICA
fig, ax = plt.subplots(figsize=(6, 5.5))

# Graficamos la PSD
ax.plot(frecuencias, psd, color='#E53935', linewidth=1.2)

# --- COLOCACIÓN AUTOMÁTICA DE LAS ETIQUETAS ---
for p in top_3_picos:
    f_pico = frecuencias[p]
    psd_pico = psd[p]
    
    # Dibujamos un pequeño punto negro sobre el pico para marcarlo
    ax.plot(f_pico, psd_pico, 'ko', markersize=4)
    
    # Añadimos el texto interactivo al lado del pico (ej. "4.08 Hz")
    # 'xytext=(5, 5)' desplaza el texto ligeramente arriba y a la derecha del punto para que no lo tape
    ax.annotate(f"({psd_pico:.2f} dB, {f_pico:.2f} Hz)", 
                xy=(f_pico, psd_pico), 
                xytext=(5, 5), 
                textcoords='offset points',
                fontsize=10, 
                fontweight='bold',
                color='black')

# Configuraciones de escala y límites (Idéntico a tu imagen)
ax.set_yscale('log')
#ax.set_xlim(0, 50)       
#ax.set_ylim(1e-8, 1e2)   

ax.set_xlabel('Frequency (Hz)', fontsize=14, labelpad=8)
ax.set_ylabel('Magnitude (dB)', fontsize=14, labelpad=8)
ax.grid(True, which='both', linestyle='-', alpha=0.3, color='lightgray')

for spine in ax.spines.values():
    spine.set_linewidth(0.8)

#fig.text(0.53, 0.02, 'b)', horizontalalignment='center', fontsize=22)
plt.tight_layout()
#plt.subplots_adjust(bottom=0.16)

# Guardar y mostrar
plt.savefig(f'graficas/{nombre_grafica}', format='png', dpi=300)

import numpy as np

# Nombre del archivo
archivo = "datos/espuma_con_sin/Conespuma_definitivo.txt"

# Cargar datos del archivo
# Se asume el formato:
# tiempo[TAB]aceleracion
datos = np.loadtxt(archivo, delimiter="\t")

# Extraer columnas
tiempo = datos[:, 0]
aceleracion = datos[:, 1]

# Calcular RMS de la aceleración
aceleracion_rms = np.sqrt(np.mean(aceleracion**2))

print(f"Aceleración RMS: {aceleracion_rms:.4f} m/s²")
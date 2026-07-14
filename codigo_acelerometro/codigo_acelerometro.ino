#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;

float offsetZ = 0.0;
unsigned long startTime = 0;          // Guarda el momento en que inicia la medición
const unsigned long duration = 15000; // Duración de la medición (10 segundos en ms)
bool medicionActiva = false;          // Controla si el sensor debe seguir midiendo
bool medicionTerminada = false;       // Evita que el mensaje de fin se repita

void setup(void) {
  Serial.begin(250000);

  Serial.println("--- Buscando el modulo MPU6050 ---");

  if (!mpu.begin()) {
    Serial.println("Error: No se pudo encontrar el chip MPU6050. Verifica las conexiones.");
    while (1) {
      delay(10);
    }
  }

  Serial.println("¡MPU6050 encontrado y conectado con exito!");

  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_44_HZ);

  // --- PROCESO DE CALIBRACIÓN ---
  Serial.println("No muevas el sensor. Calibrando Z...");
  delay(2000);

  const int N = 1000;
  float sumaZ = 0.0;
  sensors_event_t a, g, temp;

  for (int i = 0; i < N; i++) {
    mpu.getEvent(&a, &g, &temp);
    sumaZ += a.acceleration.z;
    delay(2);
  }

  offsetZ = sumaZ / N;

  Serial.print("Offset Z calibrado = ");
  Serial.println(offsetZ, 6);
  Serial.println("---------------------------------------");

  // --- PAUSA HASTA PRESIONAR UNA TECLA ---
  Serial.println("Calibracion COMPLETA. Sensor listo.");
  Serial.println("Escribe cualquier caracter y presiona ENTER en el Monitor Serie para empezar...");

  // Espera a que el buffer del Serial reciba datos
  while (Serial.available() == 0) {
    delay(10); 
  }

  // Limpia el buffer de entrada para que no afecte a futuras lecturas
  while (Serial.available() > 0) {
    Serial.read();
  }

  Serial.println("\n--- INICIANDO LECTURA DE 10 SEGUNDOS ---");
  Serial.println("Tiempo(ms),Aceleracion_Z(m/s^2)"); // Encabezado para tus datos

  startTime = millis(); // Registramos el tiempo exacto de inicio
  medicionActiva = true;
}

void loop() {
  // Solo ejecuta si la medición está activa
  if (medicionActiva) {
    unsigned long currentTime = millis();

    // Comprueba si han pasado menos de 10 segundos (10000 ms)
    if (currentTime - startTime < duration) {
      sensors_event_t a, g, temp;
      mpu.getEvent(&a, &g, &temp);

      float az = a.acceleration.z - offsetZ;

      // Tiempo relativo (empieza en 0 ms para que tu gráfica sea más limpia)
      Serial.print(currentTime - startTime);
      Serial.print("\t");
      Serial.println(az, 6);

      delay(5);   // Frecuencia de muestreo de ~200 Hz
    } 
    else {
      // Si pasaron los 10 segundos, desactivamos la medición
      medicionActiva = false;
      medicionTerminada = true;
      Serial.println("--- MEDICIÓN FINALIZADA ---");
    }
  }

  // Si ya terminó, el Arduino se queda aquí en reposo sin hacer nada más
  if (medicionTerminada) {
    // Si quieres repetir la prueba, tendrías que reiniciar el Arduino
  }
}
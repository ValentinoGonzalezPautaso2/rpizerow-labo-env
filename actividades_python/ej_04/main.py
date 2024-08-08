from gpiozero import PWMLED
import ADS1x15
import time
import math

# Declara el pin de I2C y el registro
ADS = ADS1x15.ADS1115(1,0x48)
# Declara el modo a utilizar.
ADS.setMode(ADS.MODE_SINGLE)
# Hace que la ganancia del ADC sea de +-6,144V.
ADS.setGain(ADS.PGA_4_096V)
# Convierte el valor obtenido por el ADC a un valor de voltaje.
factor = ADS.toVoltage()

# Declara que los pines 26 y 19 corresponden al LED rojo y azul y permite variar su brillo usando PWM.
LEDAzul = PWMLED(26)
LEDRojo = PWMLED(19)

# Variables para el cálculo de la temperatura
vcc = 3.3  # Voltaje de referencia (VCC)
r = 10000  # Resistencia fija en el divisor de tensión
beta = 3900  # Constante beta del termistor
t0 = 298.15  # Temperatura de referencia (25 °C en Kelvin)
t= 0 # Temperatura en grados Celsius
rt = 0 # Resistencia del termistor


while True:
    # Lectura de los valores analógicos del potenciómetro y termistor
    LecturaPote = ADS.readADC(3)
    LecturaTerm = ADS.readADC(1)

    # Conversión de las lecturas a voltaje
    LecturaPoteVoltaje = LecturaPote * factor
    LecturaTermVoltaje = LecturaTerm * factor

    # Cálculo de la resistencia del termistor
    rt = (r * LecturaTermVoltaje) / (vcc - LecturaTermVoltaje)

    # Conversión a temperatura usando la ecuación de Steinhart-Hart
    t = beta / (math.log(rt / r) + (beta / t0))
    t = t - 273.15  # Conversión a grados Celsius

    # Escalar el voltaje del potenciómetro a un rango de 0 a 30 grados Celsius
    TempPote = (LecturaPoteVoltaje / 3.3) * 30

    # Calcular la diferencia entre la temperatura deseada y la medida
    diff = abs(TempPote - t)

    # Limitar la diferencia a un máximo de 5 grados
    if diff > 5:
        diff = 5

    # Control de los LEDs según la diferencia de temperatura
    if TempPote > t:
        LEDRojo.value = diff / 5  # Brillo proporcional a la diferencia
        LEDAzul.value = 0
    elif TempPote < t:
        LEDAzul.value = diff / 5
        LEDRojo.value = 0
    else:
        LEDAzul.value = 0
        LEDRojo.value = 0


    print("Termistor: {0:.3f} V, {1:.3f} °C".format(LecturaTermVoltaje, t))
    print("Potenciómetro: {0:.2f} °C".format(TempPote))

    time.sleep(1)

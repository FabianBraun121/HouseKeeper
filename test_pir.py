import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
# Initialisierung des PIR-Sensors auf PIN 12
PIR = 18
GPIO.setup(PIR, GPIO.IN)
print("PIR-Sensor aktiv!")

while True:
    if (GPIO.input(PIR) == 0):  # Wenn der Sensor Input = 0 ist
        print("Keine Bewegung ...")  # Wird der print Befehl ausgeführt
    elif (GPIO.input(PIR) == 1):  # Wenn der Sensor Input = 1 ist
        print("Bewegung Erkannt!")  # Wird der print Befehl ausgeführt
    time.sleep(0.5)  # 0,5 Sekunde wartentry: # Beginn einer Schleife

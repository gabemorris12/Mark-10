import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.OUT)

for _ in range(10):
    GPIO.output(36, True)
    sleep(0.5)
    GPIO.output(36, False)
    sleep(0.5)

GPIO.cleanup()

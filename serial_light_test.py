from serial_connection import SerialConnection
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

data = SerialConnection('/dev/ttyUSB0')
data.check_serial_threads[-1].start()
time.sleep(10)
data.stop_checking_serial = True
time.sleep(1)

GPIO.cleanup()

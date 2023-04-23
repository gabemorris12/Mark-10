import RPi.GPIO as GPIO
from serial_connection import SerialConnection
import time
import matplotlib.pyplot as plt
import numpy as np

refresh_rate = 10

GPIO.setmode(GPIO.BOARD)
data = SerialConnection('/dev/ttyUSB0')
GPIO.setup(data.button_num, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

mark_data = []
unit = data.get_unit()

while True:
    if GPIO.input(data.button_num):
        mark_data = data.run_test()

    if mark_data:
        break

    time.sleep(0.01)

fig, ax = plt.subplots()
time_ = np.arange(0, len(mark_data)/refresh_rate, 1/refresh_rate)

ax.plot(time_, mark_data)
ax.set_xlabel('Time (s)')
ax.set_ylabel(f'Force ({unit})')
ax.grid()
fig.savefig('scratch.png')
GPIO.cleanup()

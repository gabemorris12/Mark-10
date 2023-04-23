import RPi.GPIO as GPIO
from serial_connection import SerialConnection, list_to_bytes
from client_connection import ClientConnection
import socket
import time
import matplotlib.pyplot as plt
import numpy as np

refresh_rate = 10
address = ('9C:B6:D0:F7:47:E2', 4)

GPIO.setmode(GPIO.BOARD)
data = SerialConnection('/dev/ttyUSB0')
GPIO.setup(data.button_num, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

mark_data = []
unit = data.get_unit()

while True:
    if GPIO.input(data.button_num):
        mark_data = data.run_test()
        break

    time.sleep(0.01)

client = ClientConnection(socket.AF_BLUETOOTH, socket.SOCK_STREAM, 3, address=address)
client.check_bluetooth_threads[-1].start()
time.sleep(1)
client.send(unit.encode())
time.sleep(1)
client.stop_checking_bluetooth = True
GPIO.output(client.bluetooth_num, False)
time.sleep(1)
print(client.check_bluetooth_threads[-1].is_alive())
print(mark_data)
print(len(list_to_bytes(mark_data)))
client.sendall(list_to_bytes(mark_data))

fig, ax = plt.subplots()
time_ = np.arange(0, len(mark_data)/refresh_rate, 1/refresh_rate)

ax.plot(time_, mark_data)
ax.set_xlabel('Time (s)')
ax.set_ylabel(f'Force ({unit})')
ax.grid()
plt.show()
GPIO.cleanup()

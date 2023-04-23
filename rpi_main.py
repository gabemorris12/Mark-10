from serial_connection import SerialConnection, list_to_bytes
from client_connection import ClientConnection
import socket
import RPi.GPIO as GPIO
import time

# ADJUSTABLE PARAMETERS ################################################################################################

SERIAL_PORT = '/dev/ttyUSB0'  # Port path to USB connection
ADDRESS = ('9C:B6:D0:F7:47:E2', 4)  # Address and port that is being run on the server
NAME = 'Joffin'  # Device name
REFRESH_RATE = 125  # Samples per second (needs to match the Mark 10)

########################################################################################################################

GPIO.setmode(GPIO.BOARD)
data = SerialConnection(SERIAL_PORT)
GPIO.setup(data.button_num, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
client = ClientConnection(socket.AF_BLUETOOTH, socket.SOCK_STREAM, 3, name=NAME, address=ADDRESS)

client.check_bluetooth_threads[-1].start()
data.check_serial_threads[-1].start()

try:
    while True:
        if GPIO.input(data.button_num) and data.data_active and client.bluetooth_active:
            data.stop_checking_serial, client.stop_checking_bluetooth = True, True
            time.sleep(0.1)

            unit = data.get_unit()
            client.send(unit.encode())

            mark_data = data.run_test()
            # TODO: Add plot and store method here

            client.sendall(list_to_bytes(mark_data))
            time.sleep(0.1)

            data.stop_checking_serial, client.stop_checking_bluetooth = False, False
            client.check_bluetooth_threads[-1].start()
            data.check_serial_threads[-1].start()
        elif GPIO.input(data.button_num) and (not data.data_active or not client.bluetooth_active):
            for _ in range(5):
                GPIO.output(data.run_num, True)
                time.sleep(0.5)
                GPIO.output(data.run_num, False)
                time.sleep(0.5)

        time.sleep(0.05)
except KeyboardInterrupt:
    data.stop_checking_serial, client.stop_checking_bluetooth = True, True
    time.sleep(0.1)
    GPIO.cleanup()
    client.close()
    data.close()

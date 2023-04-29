from serial_connection import SerialConnection, list_to_bytes
from client_connection import ClientConnection
from server_connection import plot_store_data
import socket
import RPi.GPIO as GPIO
import time
import serial

# ADJUSTABLE PARAMETERS ################################################################################################

SERIAL_PORT = '/dev/ttyUSB0'  # Port path to USB connection
ADDRESS = ('9C:B6:D0:F7:47:E2', 4)  # Address and port that is being run on the server
NAME = 'Jeffry'  # Device name
REFRESH_RATE = 10  # Samples per second (needs to match the Mark 10)

########################################################################################################################


def error_flash(i):
    for _ in range(i):
        GPIO.output(37, True)
        time.sleep(0.5)
        GPIO.output(37, False)
        time.sleep(0.5)


GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.OUT)
# error_flash(20)

while True:
        try:
            data = SerialConnection(SERIAL_PORT)
        except serial.serialutil.SerialException:
            error_flash(5)
        else:
            break

GPIO.setup(data.button_num, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
client = ClientConnection(socket.AF_BLUETOOTH, socket.SOCK_STREAM, 3, name=NAME, address=ADDRESS)

client.check_bluetooth_threads[-1].start()
data.check_serial_threads[-1].start()


def main():

    while True:
        if GPIO.input(data.button_num) and data.data_active and client.bluetooth_active:
            data.stop_checking_serial, client.stop_checking_bluetooth = True, True
            time.sleep(0.1)

            unit = data.get_unit()
            client.send(unit.encode())

            mark_data = data.run_test()
            try:
                plot_store_data(REFRESH_RATE, mark_data, unit, NAME, launch_file=False)
            except PermissionError:
                pass

            client.sendall(list_to_bytes(mark_data))
            time.sleep(0.1)

            data.stop_checking_serial, client.stop_checking_bluetooth = False, False
            client.check_bluetooth_threads[-1].start()
            data.check_serial_threads[-1].start()
        elif GPIO.input(data.button_num) and (not data.data_active or not client.bluetooth_active):
            error_flash(5)

        time.sleep(0.05)


try:
    main()
except (KeyboardInterrupt, serial.SerialException, RuntimeError, ConnectionResetError):
    data.stop_checking_serial, client.stop_checking_bluetooth = True, True
    time.sleep(0.1)
    GPIO.cleanup()
    client.close()
    data.close()

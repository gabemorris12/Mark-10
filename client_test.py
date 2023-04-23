import socket
from client_connection import ClientConnection
import RPi.GPIO as GPIO

address = ('9C:B6:D0:F7:47:E2', 4)
GPIO.setmode(GPIO.BOARD)

client = ClientConnection(socket.AF_BLUETOOTH, socket.SOCK_STREAM, 3, address=address)

try:
    client.check_bluetooth()
except KeyboardInterrupt:
    GPIO.cleanup()

# Tests the serial connection by printing the output
from serial_connection import SerialConnection

data = SerialConnection('/dev/ttyUSB0')
data.print_output()
data.close()

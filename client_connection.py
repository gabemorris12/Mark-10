import socket
import RPi.GPIO as GPIO
import threading


class ClientConnection(socket.socket):
    def __init__(self, family=-1, type_=-1, proto=-1, file_no=None, bluetooth_num=36, address=None, name='Joffin'):
        super().__init__(family=family, type=type_, proto=proto, fileno=file_no)

        self.address = address
        self.name = name

        self.bluetooth_num = bluetooth_num
        GPIO.setup(self.bluetooth_num, GPIO.OUT)

        self.check_bluetooth_threads = [threading.Thread(target=self.check_bluetooth, name='Check Bluetooth')]
        self.bluetooth_active = False
        self.connection_made = False
        self.stop_checking_bluetooth = False

    def check_bluetooth(self):
        while not self.stop_checking_bluetooth:
            if not self.connection_made:
                try:
                    super().__init__(self.family, self.type, self.proto)
                    self.connect(self.address)
                except (ConnectionRefusedError, OSError):
                    self.bluetooth_active = False
                else:
                    self.connection_made = True
                    self.send(self.name.encode())
            else:
                try:
                    self.send(self.name.encode())
                    received = self.recv(1024)
                except ConnectionResetError:
                    self.connection_made, self.bluetooth_active = False, False
                else:
                    if received.decode() == 'received':
                        self.bluetooth_active = True
                    else:
                        self.bluetooth_active = False

            GPIO.output(self.bluetooth_num, self.bluetooth_active)

        # GPIO.output(self.bluetooth_num, False)
        self.check_bluetooth_threads.append(threading.Thread(target=self.check_bluetooth, name='Check Bluetooth'))


if __name__ == '__main__':
    address_ = ('9C:B6:D0:F7:47:E2', 4)
    GPIO.setmode(GPIO.BOARD)

    client = ClientConnection(socket.AF_BLUETOOTH, socket.SOCK_STREAM, 3, address=address_)

    try:
        client.check_bluetooth()
    except KeyboardInterrupt:
        client.close()
        GPIO.cleanup()

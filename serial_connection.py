import time
import serial
import re
import RPi.GPIO as GPIO
import threading
import struct


class SerialConnection(serial.Serial):

    def __init__(self, port=None, baudrate=9600, button_num=40, serial_num=38, run_num=37, **kwargs):
        super().__init__(port, baudrate, **kwargs)

        self.button_num = button_num
        self.serial_num = serial_num
        self.run_num = run_num
        GPIO.setup(self.serial_num, GPIO.OUT)
        GPIO.setup(self.run_num, GPIO.OUT)

        self.check_serial_threads = [threading.Thread(target=self.check_serial, name='Check Serial')]
        self.data_active = False
        self.stop_checking_serial = False

    def is_receiving_data(self):
        """
        Used to test if the pi is receiving data from the Mark 10. The function takes a little over a second to
        complete.

        :return: bool
        """
        start = time.perf_counter()
        datas = []
        self.reset_input_buffer()
        while time.perf_counter() - start <= 0.1:
            if self.inWaiting():
                try:
                    data = self.readline().decode()
                    datas.append(data)
                except UnicodeDecodeError:
                    pass

        return True if datas else False, datas

    def check_serial(self):
        """
        Checks the serial connection and turns on/off a light to indicate the connection.
        """
        while not self.stop_checking_serial:
            self.data_active = self.is_receiving_data()[0]
            GPIO.output(self.serial_num, self.data_active)

        # self.data_active = False
        # GPIO.output(self.serial_num, False)
        self.check_serial_threads.append(threading.Thread(target=self.check_serial, name='Check Serial'))

    def get_unit(self):
        """
        Gets the unit of force from the Mark 10. The only options are lbF, kgF, and kN.

        :return: str
        """
        bool_, datas = self.is_receiving_data()
        assert bool_, 'Port is not receiving data.'

        unit_pattern = re.compile(r'[A-Za-z]+')
        units = []
        for line in datas:
            match = unit_pattern.search(line)
            if match:
                units.append(match.group().strip())

        if 'lbF' in units:
            return 'lbF'
        elif 'kgF' in units:
            return 'kgF'
        elif 'kN' in units:
            return 'kN'

        return ''

    def print_output(self):
        """
        Prints out the raw data from the Mark 10 for troubleshooting.
        """
        try:
            while True:
                if self.inWaiting():
                    data = self.readline().decode()
                    print(data, end='')
        except KeyboardInterrupt:
            exit()

    def run_test(self):
        """
        Records and returns data.

        :return: List
        """
        data = []
        start = time.perf_counter()
        GPIO.output(self.run_num, True)
        self.reset_input_buffer()

        while True:
            if self.inWaiting():
                string = self.readline().decode()
                data += clean_data(string)

            if GPIO.input(self.button_num) and time.perf_counter() - start > 1:
                break

        GPIO.output(self.run_num, False)

        return data


def clean_data(data):
    """
    Cleans up the data received from the serial connection and returns a list of floats.

    :param data: str; raw input from the Mark 10
    :return: List
    """
    matches = re.findall(r'[0-9.]+', data)
    return [float(match) for match in matches]


def list_to_bytes(data):
    byte_list = []
    for f in data:
        byte_list += struct.pack('d', f)

    byte_stream = bytes(byte_list)
    data_size = len(byte_stream)
    byte_stream = struct.pack('q', data_size) + byte_stream
    return byte_stream

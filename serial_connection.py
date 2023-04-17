import time
import serial
import re


class SerialConnection:
    def __init__(self, port, baud_rate=9600):
        self.port, self.baud_rate = port, baud_rate
        self.serial = serial.Serial(port, baud_rate)

    def is_receiving_data(self):
        """
        Used to test if the pi is receiving data from the Mark 10. The function takes a little over a second to
        complete.

        :return: True or False
        """
        start = time.perf_counter()
        datas = []
        while time.perf_counter() - start <= 1.1:
            if self.serial.inWaiting():
                try:
                    data = self.serial.readline().decode()
                    datas.append(data)
                except UnicodeDecodeError:
                    pass

        return True if datas else False, datas

    def get_unit(self):
        """
        Gets the unit of force from the Mark 10. The only options are lbF, kgF, and kN.

        :return:
        """
        bool_, datas = self.is_receiving_data()
        assert bool_, 'Port is not receiving data.'

        unit_pattern = re.compile(r'[A-Za-z\-]+')
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
        Prints out the raw data from the Mark 10 for troubleshoooting.

        :return:
        """
        try:
            while True:
                if self.serial.inWaiting():
                    data = self.serial.readline().decode()
                    print(data, end='')
        except KeyboardInterrupt:
            exit()

    def close(self):
        self.serial.close()

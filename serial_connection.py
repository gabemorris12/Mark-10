import time
import serial
import re


class SerialConnection:
    def __init__(self, port, baud_rate=9600):
        self.port, self.baud_rate = port, baud_rate
        self.serial = serial.Serial(port, baud_rate)

    def is_receiving_data(self):
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
        bool_, datas = self.is_receiving_data()
        assert bool_, 'Port is not receiving data.'

        unit_pattern = re.compile(r'[A-Za-z\-]+')
        units = []
        for line in datas:
            match = unit_pattern.search(line)
            if match:
                units.append(match.group().strip())

        if 'lbF' in units:
            return 'lbf'
        elif 'kgF' in units:
            return 'kgF'
        elif 'kN' in units:
            return 'kN'

        return ''

    def close(self):
        self.serial.close()

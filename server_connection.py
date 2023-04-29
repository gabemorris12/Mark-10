import socket
import threading
import struct
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime
import csv
import warnings

# ADJUSTABLE PARAMETERS ################################################################################################

REFRESH_RATE = 10  # Samples per second (needs to match the Mark 10)
ADDRESS = ('9C:B6:D0:F7:47:E2', 4)

########################################################################################################################

warnings.filterwarnings('ignore', category=UserWarning)

bytes_length = struct.calcsize('q')
float_size = struct.calcsize('d')

if not os.path.isdir('data'):
    os.mkdir('data')


class ServerConnection(socket.socket):
    def __init__(self, family=-1, type_=-1, proto=-1, file_no=None, address=None):
        super().__init__(family=family, type=type_, proto=proto, fileno=file_no)

        self.address = address
        self.bind(self.address)
        self.listen()
        print(f'Server listening on {self.address[0]}')

        self.client_threads = []

        while True:
            client_obj, client_address = self.accept()
            name = client_obj.recv(1024).decode()
            print(f'Connection made with {name} at {client_address}')
            thread = threading.Thread(target=handle_client, args=(client_obj, name))
            self.client_threads.append(thread)
            thread.start()


def handle_client(client_obj, name):
    unit = ''

    while True:
        content = client_obj.recv(1024)
        if not content:
            print(f'Disconnected with {name}')
            client_obj.close()
            break

        try:
            value = content.decode()
            if value == name:
                client_obj.send('received'.encode())
            elif value in ['lbF', 'kgF', 'kN']:
                unit = value
                print(f'Received {unit} unit from {name}')
            else:
                data = retrieve_data(content, client_obj)
                print(f'Data received from {name}')
                threading.Thread(target=plot_store_data, args=(REFRESH_RATE, data, unit, name)).start()
        except:
            data = retrieve_data(content, client_obj)
            print(f'Data received from {name}')
            threading.Thread(target=plot_store_data, args=(REFRESH_RATE, data, unit, name)).start()


def retrieve_data(content_, client_obj_):
    while len(content_) < bytes_length:
        content_ += client_obj_.recv(1024)
    data_size_bytes = content_[:bytes_length]
    data_size = struct.unpack('q', data_size_bytes)[0]

    data_bytes = content_[bytes_length:]
    while len(data_bytes) < data_size:
        data_bytes += client_obj_.recv(1024)

    data = [struct.unpack('d', data_bytes[i:i + float_size])[0] for i in range(0, data_size, float_size)]
    return data


def plot_store_data(refresh_rate_, data_, unit_, name_, launch_file=True):
    dir_ = os.path.join('data', name_)
    if not os.path.isdir(dir_):
        os.mkdir(dir_)

    instant = datetime.datetime.now()
    stamp = instant.strftime('%d-%m-%Y_%H-%M-%S')
    file_name = f'{name_} {stamp}'

    fig, ax = plt.subplots()
    time_ = np.arange(0, len(data_)/refresh_rate_, 1/refresh_rate_)

    ax.plot(time_, data_, color='#db011c')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel(f'Force ({unit_})')
    ax.grid()

    with open(os.path.join(dir_, file_name + '.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Time (s)', f'Force ({unit_})'])
        for row in zip(time_, data_):
            writer.writerow(row)

    image_file = os.path.join(dir_, file_name + '.png')
    fig.savefig(image_file, dpi=240)

    if launch_file:
        os.startfile(image_file)


if __name__ == '__main__':
    server = None
    try:
        server = ServerConnection(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM, address=ADDRESS)
    except KeyboardInterrupt:
        server.close()

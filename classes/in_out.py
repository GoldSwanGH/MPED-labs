import struct

import numpy as np


class InOut:

    @staticmethod
    def read_dat(path):
        floats = []
        with open(path, mode="rb") as file:
            content = file.read()
            for i in range(0, len(content), 4):
                fl = struct.unpack('f', content[i:i+4])
                floats.append(fl)
        floats = np.array(floats)
        return floats

    @staticmethod
    def write_dat():
        pass
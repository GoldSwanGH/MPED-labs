import struct
import uuid
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
    def write_dat(path_to_file, data):
        bytesarr = bytearray(data)
        with open(path_to_file + "newfile_" + str(uuid.uuid4()) + ".dat", mode="wb") as file:
            file.write(bytesarr)

    @staticmethod
    def read_wav():
        pass

    @staticmethod
    def write_wav():
        pass

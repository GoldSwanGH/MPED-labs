import struct
import uuid
from random import random

from scipy.io import wavfile
import numpy
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
        floats = np.array(object=floats, dtype=numpy.float32)
        return floats

    @staticmethod
    def write_dat(path_to_file, data, file_name="newfile_" + str(uuid.uuid4())):
        if isinstance(data, np.ndarray):
            bytesarr = data.tobytes()
        else:
            bytesarr = bytearray(data)
        with open(path_to_file + file_name + ".dat", mode="wb") as file:
            file.write(bytesarr)

    @staticmethod
    def read_wav(path):
        samplerate, data = wavfile.read(path)
        return samplerate, data

    @staticmethod
    def write_wav(path_to_file, data, rate, file_name="sound_" + str(uuid.uuid4())):
        data = data.astype(dtype="int16")
        wavfile.write(filename=path_to_file + file_name + ".wav", rate=rate, data=data)

import copy
import numpy as np

from classes.harm_data import HarmData
from classes.noise_data import NoiseData
from classes.noise_type import NoiseType
from classes.polyharm_data import PolyHarmData
from classes.trend_data import TrendData


class Model:

    @staticmethod
    def trend(N, a, b, data_type):  # Task 1
        return TrendData(N, a, b, data_type)

    @staticmethod
    def noise(N=1000, R=10):  # Task 2
        return NoiseData(N, R, NoiseType.DEFAULT)

    @staticmethod
    def my_noise(N=1000, R=10):  # Task 2
        return NoiseData(N, R, NoiseType.CUSTOM)

    @staticmethod
    def shift(in_data, C):  # Task 4
        out_data = copy.deepcopy(in_data)
        out_data.y = out_data.y + C
        return out_data

    @staticmethod
    def impulse_noise(data, M=None, R=1000, Rs=None):  # Task 4
        if Rs is None:
            Rs = R / 10
        if M is None:
            M = int((np.random.randint(500, 1000) / 100000) * data.N)

        data_copy = copy.deepcopy(data)

        outliers = np.random.randint(0, data.N, M)

        for i in range(M):
            sign = np.random.randint(0, 2)
            value = np.random.randint(R-Rs, R+Rs)
            data_copy.y[outliers[i]] = value * ((-1) ** sign)

        return data_copy

    @staticmethod
    def harm(N=1000, A0=100, f0=33, dt=0.001):
        return HarmData(N, A0, dt, f0)

    @staticmethod
    def poly_harm(N=1000, A0=100, f0=33, A1=15, f1=5, A2=10, f2=170, dt=0.001):
        return PolyHarmData(N=N, A0=A0, dt=dt, f0=f0, A1=A1, f1=f1, A2=A2, f2=f2)

    @staticmethod
    def add_model(data1, data2):
        data = copy.deepcopy(data1)
        data.y += data2.y

        return data



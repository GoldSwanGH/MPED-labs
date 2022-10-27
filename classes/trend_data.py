import math
import numpy as np

from classes.data_type import DataType


class TrendData:

    def __init__(self, N, a, b, data_type):
        self.N = N
        self.type = type
        self.a = a
        self.b = b

        self.x = np.arange(N)

        if data_type == DataType.LINEAR:
            self.y = -a * self.x + b
        elif data_type == DataType.EXPONENTIAL:
            self.y = b * np.exp(-a * self.x)

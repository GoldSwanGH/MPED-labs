from classes.my_random import MyRandom
from classes.noise_type import NoiseType
import numpy as np


class NoiseData:

    def __init__(self, N, R, noise_type: NoiseType):
        self.N = N
        self.type = type

        self.x = np.arange(N)
        if noise_type == NoiseType.DEFAULT:
            self.y = np.random.rand(N)
        elif noise_type == NoiseType.CUSTOM:
            rnd = MyRandom()
            self.y = rnd.rand(N)

        y_max = self.y.max(initial=-1)
        y_min = self.y.min(initial=1)
        for y_i in np.nditer(self.y, op_flags=['readwrite']):
            y_i[...] = ((y_i - y_min) / (y_max - y_min) - 0.5) * 2 * R

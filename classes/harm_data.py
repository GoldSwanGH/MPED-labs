import math
import numpy as np


class HarmData:

    def __init__(self, N=1000, A0=100, dt=0.001, f0=33):
        self.N = N
        self.A = A0
        self.f = f0
        self.x = np.arange(N)
        self.y = A0 * np.sin(2 * math.pi * f0 * dt * self.x)

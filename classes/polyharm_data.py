import math
import numpy as np


class PolyHarmData:

    def __init__(self, N=1000, A0=100, f0=33, A1=15, f1=5, A2=10, f2=170, dt=0.001):
        self.N = N
        self.dt = dt
        self.A0 = A0
        self.A1 = A1
        self.A2 = A2
        self.f0 = f0
        self.f1 = f1
        self.f2 = f2
        self.x = np.arange(N)
        self.y = A0 * np.sin(2 * math.pi * f0 * dt * self.x) \
                 + A1 * np.sin(2 * math.pi * f1 * dt * self.x) \
                 + A2 * np.sin(2 * math.pi * f2 * dt * self.x)

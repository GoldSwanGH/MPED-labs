import datetime
import numpy as np


class MyRandom:

    def __init__(self, m=2**32, a=1664525, c=1013904223, seed=None):
        if seed is None:
            self.seed = datetime.datetime.now().microsecond
        else:
            self.seed = seed

        self.m = m
        self.a = a
        self.c = c

    def next_double(self):
        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed / self.m

    def rand(self, N=1):
        if N < 1:
            raise ValueError("N must be at least 1")
        elif N == 1:
            return self.next_double()

        new_list = []
        for i in range(N):
            new_list.append(self.next_double())

        return np.array(new_list)

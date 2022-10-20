import copy

import numpy as np


class Processing:

    @staticmethod
    def anti_shift(data):  # Task 7.3
        data_copy = copy.deepcopy(data)
        mean = data.y.mean()
        for k in range(data.N):
            data_copy.y[k] = data.y[k] - mean

        return data_copy

    @staticmethod
    def anti_spike(data, R):  # Task 7.4
        data_copy = copy.deepcopy(data)
        mean = data.y.mean()

        for k in range(data.N):
            if -R < data.y[k] < R:
                continue
            elif k == 0 or k == (data.N - 1):
                data_copy.y[k] = mean
            else:
                prev = data_copy.y[k - 1]
                foll = data_copy.y[k + 1]
                new_val = prev + foll / 2
                if -R < new_val < R:
                    data_copy.y[k] = new_val
                else:
                    data_copy.y[k] = mean

        return data_copy

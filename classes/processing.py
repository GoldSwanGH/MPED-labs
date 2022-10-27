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

    @staticmethod
    def anti_trend_linear(data):
        new_data = copy.deepcopy(data)
        new_data.N = data.N - 1
        new_data.x = data.x[0:-1]
        new_data.y = np.empty(data.N - 1)

        for i in range(data.N - 1):
            new_data.y[i] = data.y[i+1] - data.y[i]

        return new_data

    @staticmethod
    def anti_trend_non_linear(data, W=10):
        new_data = copy.deepcopy(data)

        for i in range(data.N - W):
            trend_elem = 0
            for k in range(W):
                trend_elem += data.y[i + k]
            trend_elem = trend_elem / W
            new_data.y[i] = data.y[i] - trend_elem

        # for i in range(data.N - 1, data.N - W - 1):
        #     trend_elem = 0
        #     for k in range(W):
        #         trend_elem += data.y[i - k]
        #     trend_elem = trend_elem / W
        #     new_data.y[i] = data.y[i] - trend_elem

        return new_data
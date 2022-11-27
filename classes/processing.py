import copy

import matplotlib.pyplot as plt
import numpy as np

from classes.noise_data import NoiseData
from classes.model import Model


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
        exp_trend = copy.deepcopy(data)

        for i in range(data.N - W):
            trend_elem = 0
            for k in range(W):
                trend_elem += data.y[i + k]
            trend_elem = trend_elem / W
            new_data.y[i] = data.y[i] - trend_elem
            exp_trend.y[i] = trend_elem
        new_data.N = data.N - W
        new_data.x = new_data.x[:-W]
        new_data.y = new_data.y[:-W]
        exp_trend.N = data.N - W
        exp_trend.x = exp_trend.x[:-W]
        exp_trend.y = exp_trend.y[:-W]
        print("Выделенный экспоненциальный тренд")
        plt.plot(exp_trend.x, exp_trend.y)
        plt.show()
        print("Нажмите Enter для следующего графика...")
        input()

        # end_data = copy.deepcopy(data)
        # end_data.y = np.empty(W)
        # j = data.N - 1
        # end = data.N - W - 1
        # ctr = 0
        # while True:
        #     if j == end:
        #         break
        #     trend_elem = 0
        #     for k in range(W):
        #         trend_elem += data.y[j - k]
        #     trend_elem = trend_elem / W
        #     end_data.y[ctr] = data.y[j] - trend_elem
        #     j -= 1
        #     ctr += 1
        # end_data.N = ctr
        # end_data = Processing.anti_shift(end_data)
        #
        # end = data.N - 1
        # j = data.N - W - 1
        # for i in end_data.y:
        #     new_data.y[j] = i
        #     j += 1

        return new_data

    @staticmethod
    def anti_noise(data=None, M=1):
        if data is None:
            data = NoiseData(N=1000, R=30)
            data.y = data.y / M
            for i in range(M - 1):
                noise = NoiseData(noise_type=data.type, N=data.N, R=data.R)
                data.y += noise.y / M
            return data
        else:
            noise = NoiseData(N=data.N, R=30)
            additive = Model.add_model(noise, data)
            additive.y = additive.y / M
            for i in range(M - 1):
                noise = NoiseData(noise_type=additive.type, N=additive.N, R=additive.R)
                new_add = Model.add_model(noise, data)
                additive.y += new_add.y / M
            return additive

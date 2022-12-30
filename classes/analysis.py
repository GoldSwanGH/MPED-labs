import copy
import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Analysis:

    @staticmethod
    def statistics(data):  # Task 3

        N = data.N
        data_min = data.y.min(initial=float('inf'))
        data_max = data.y.max(initial=float('-inf'))
        data_mean = data.y.mean()
        data_std = data.y.std()
        data_disp = data_std ** 2

        data_asym = 0
        data_excess = 0
        data_mean_square = 0
        for i in range(N):
            data_asym += (data.y[i] - data_mean) ** 3
            data_excess += (data.y[i] - data_mean) ** 4
            data_mean_square += data.y[i] ** 2

        data_asym = data_asym / N
        data_excess = data_excess / N

        data_asym_coef = data_asym / (data_std ** 3)
        data_kurt = (data_excess / (data_std ** 4)) - 3

        data_mean_square = data_mean_square / N

        data_rms = math.sqrt(data_mean_square)

        print("Статистические характеристики данных")
        print("Максимальное значение: " + str(data_max))
        print("Минимальное значение: " + str(data_min))
        print("Среднее значение: " + str(data_mean))
        print("Дисперсия: " + str(data_disp))
        print("Стандартное отклонение: " + str(data_std))
        print("Асимметрия: " + str(data_asym))
        print("Коэффициент асимметрии: " + str(data_asym_coef))
        print("Эксцесс: " + str(data_excess))
        print("Куртозис: " + str(data_kurt))
        print("Средний квадрат: " + str(data_mean_square))
        print("Среднеквадратическая ошибка: " + str(data_rms))
        print()

    @staticmethod
    def stationary(M, data):  # Task 3
        split_arr = np.split(data.y, M)

        ctr = 0
        mean_mean_deviation = 0
        mean_std_deviation = 0
        for i in range(M):
            for j in range(M):
                if i == j:
                    continue
                i_mean = np.array(split_arr[i]).mean()
                j_mean = np.array(split_arr[j]).mean()
                i_std = np.array(split_arr[i]).std()
                j_std = np.array(split_arr[j]).std()

                mean_mean_deviation += ((i_mean - j_mean) / j_mean) * 100
                mean_std_deviation += ((i_std - j_std) / j_std) * 100
                ctr += 1

        mean_mean_deviation = mean_mean_deviation / ctr
        mean_std_deviation = mean_std_deviation / ctr

        if mean_mean_deviation < 10 and mean_std_deviation < 10:
            print("Процесс стационарный")
        else:
            print("Процесс не стационарный")
        print()

    @staticmethod
    def hist(data, M):  # Task 6
        s = pd.Series(data.y)

        ymax = np.amax(data.y)
        ymin = np.amin(data.y)
        bin_size = (ymax - ymin) / M
        x = []
        bins = []
        bin = 0
        for i in range(M):
            x.append(ymin + i * bin_size)
            bins.append(0)
            # lmin = ymin + i * bin_size
            # lmax = ymin + (i + 1) * bin_size

        for i in data.y:
            for j in range(len(x)):
                if x[j] <= i < x[j] + bin_size:
                    bins[j] += 1
                    break

        return s.plot.hist(bins=M)

    @staticmethod
    def kde(data):  # Task 6 (extra)
        s = pd.Series(data.y)

        return s.plot.kde()

    @staticmethod
    def acf(data):  # Task 7.1

        Rxx = []
        mean = data.y.mean()

        for L in data.x:
            value = 0
            for k in range(data.N - L - 1):
                value += (data.y[k] - mean) * (data.y[k + L] - mean)
            Rxx.append(value)

        Rxx = np.array(Rxx)
        Rxx = Rxx / data.N
        R = Rxx / np.amax(a=Rxx)
        return R

    @staticmethod
    def ccf(dataX, dataY):  # Task 7.2
        if dataY.N < dataX.N:
            raise ValueError("dataY N must be equal or more than dataX N")

        Rxy = []
        meanX = dataX.y.mean()
        meanY = dataY.y.mean()

        for L in dataX.x:
            value = 0
            for k in range(dataX.N - int(L) - 1):
                value += (dataX.y[k] - meanX) * (dataY.y[k + int(L)] - meanY)
            Rxy.append(value)

        Rxy = np.array(Rxy)
        Rxy = Rxy / dataX.N
        return Rxy

    @staticmethod
    def fourier(data, window=0):
        data_copy = copy.deepcopy(data)
        Xn = copy.deepcopy(data)
        if window != 0:
            for i in range(data.N - window, data.N):
                data_copy.y[i] = 0
        # Re = []
        # Im = []
        for i in range(data.N):
            elemRe = 0
            elemIm = 0
            for j in range(data.N):
                elemRe += data_copy.y[j] * np.cos((2 * np.pi * i * j) / data.N)
                elemIm += data_copy.y[j] * np.sin((2 * np.pi * i * j) / data.N)
            elemRe = elemRe / data.N
            elemIm = elemIm / data.N
            # Re.append(elemRe)
            # Im.append(elemIm)
            Xn.y[i] = np.sqrt(elemRe ** 2 + elemIm ** 2)

        return Xn

    @staticmethod
    def spectre_fourier(Xn):
        new_Xn = copy.deepcopy(Xn)
        f_gr = 1 / (2 * new_Xn.dt)
        f_d = 2 * f_gr
        df = f_d / new_Xn.N
        N = int(new_Xn.N / 2)
        new_Xn.x = new_Xn.x[:N]
        new_Xn.y = new_Xn.y[:N]
        new_Xn.x = new_Xn.x * df
        new_Xn.N = N

        return new_Xn

    # @staticmethod
    # def harm_search(spec, e=0.05):  # e - порог срабатывания
    #     freqs = []
    #     ampls = []
    #
    #     if spec.y[0] - spec.y[1] > e:
    #         freqs.append(spec.x[0])
    #         ampls.append(int(float(spec.y[0]) * 2))
    #     for i in range(1, len(spec.y) - 1):
    #         if spec.y[i] - spec.y[i - 1] > e and spec.y[i] - spec.y[i + 1] > e:
    #             freqs.append(spec.x[i])
    #             ampls.append(int(round(float(spec.y[i]) * 2)))
    #     if spec.y[len(spec.y) - 1] - spec.y[len(spec.y) - 2] > e:
    #         freqs.append(spec.x[len(spec.y) - 1])
    #         ampls.append(int(float(spec.y[len(spec.y) - 1]) * 2))
    #
    #     return [freqs, ampls]

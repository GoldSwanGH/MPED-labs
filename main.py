import copy
from sys import exit
import matplotlib.pyplot as plt
import numpy as np
import os

from classes.analysis import Analysis
from classes.data_type import DataType
from classes.model import Model
from classes.in_out import InOut
from classes.processing import Processing


while True:
    plt.rcParams["figure.figsize"] = (9.6, 7.2)  # 4:3 формат графиков по умолчанию (оставил), увеличил разрешение в 1.5 раза
    print("Введите номер задания (от 1 до 15), 18 для зачета или 0 для выхода: ")
    i = int(input())

    if i == 1:
        lin_asc = Model.trend(N=1000, a=-2, b=3, data_type=DataType.LINEAR)
        lin_des = Model.trend(N=1000, a=2, b=3, data_type=DataType.LINEAR)
        non_lin_asc = Model.trend(N=1000, a=-0.01, b=10000, data_type=DataType.EXPONENTIAL)
        non_lin_des = Model.trend(N=1000, a=0.01, b=10000, data_type=DataType.EXPONENTIAL)

        plt.subplot(221)
        plt.plot(lin_asc.x, lin_asc.y, 'b-')

        plt.subplot(222)
        plt.plot(lin_des.x, lin_des.y, 'b-')

        plt.subplot(223)
        plt.plot(non_lin_asc.x, non_lin_asc.y, 'b-')

        plt.subplot(224)
        plt.plot(non_lin_des.x, non_lin_des.y, 'b-')

        plt.show()

    elif i == 2:
        default_noise_1 = Model.noise(N=1000, R=10)
        custom_noise = Model.my_noise(N=1000, R=10)

        plt.subplot(121)
        plt.plot(default_noise_1.x, default_noise_1.y, 'b.')

        plt.subplot(122)
        plt.plot(custom_noise.x, custom_noise.y, 'b.')

        plt.show()

    elif i == 3:
        lin_asc = Model.trend(N=1000, a=-2, b=3, data_type=DataType.LINEAR)
        default_noise_1 = Model.noise(N=1000, R=10)
        non_lin_asc = Model.trend(N=1000, a=-0.01, b=10000, data_type=DataType.EXPONENTIAL)
        print()
        print("Тренд:")
        Analysis.statistics(lin_asc)
        Analysis.stationary(10, lin_asc)

        print()
        print("Экспонента:")
        Analysis.statistics(non_lin_asc)
        Analysis.stationary(10, non_lin_asc)

        print("Случайный шум:")
        Analysis.statistics(default_noise_1)
        Analysis.stationary(10, default_noise_1)

        print("Случаный шум с выбросами")
        impulsed_noise = Model.impulse_noise(default_noise_1)
        Analysis.statistics(impulsed_noise)
        Analysis.stationary(10, impulsed_noise)

    elif i == 4:
        default_noise_1 = Model.noise(N=1000, R=10)
        shifted_noise = Model.shift(default_noise_1, 20)

        default_noise_2 = Model.noise(N=1000, R=50)
        impulsed_noise = Model.impulse_noise(default_noise_2)

        plt.subplot(221)
        plt.plot(default_noise_1.x, default_noise_1.y, 'b.')
        plt.subplot(222)
        plt.plot(shifted_noise.x, shifted_noise.y, 'b.')
        plt.subplot(223)
        plt.plot(impulsed_noise.x, impulsed_noise.y, 'b.')

        plt.show()

    elif i == 5:
        print("Итерационное повышение f0")
        o = 0
        for i in range(12):
            f0 = 33+(50 * i)
            harm_1 = Model.harm(N=100, A0=100, f0=f0)
            plt.subplot(6, 1, i + 1 + o)
            plt.plot(harm_1.x, harm_1.y)
            if i == 5:
                plt.show()
                print("Нажмите Enter для следующего графика...")
                input()
                o = -6
                plt.clf()

        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        polyharm = Model.poly_harm()
        plt.plot(polyharm.x, polyharm.y)
        plt.show()

    elif i == 6:
        default_noise_1 = Model.noise(N=10000, R=10)
        lin_asc = Model.trend(N=10000, a=-2, b=3, data_type=DataType.LINEAR)
        non_lin_asc = Model.trend(N=10000, a=0.001, b=10000, data_type=DataType.EXPONENTIAL)
        harm_1 = Model.harm(N=10000, A0=100, f0=33)

        list = [default_noise_1, lin_asc, non_lin_asc, harm_1]

        for data in list:
            plt.subplot(211)
            Analysis.hist(data, 100)
            plt.subplot(212)
            Analysis.kde(data)
            plt.show()

            print("Гистограмма процесса типа " + data.__class__.__name__)
            print("Нажмите Enter для следующего графика...")
            input()

            plt.clf()

    elif i == 7:
        # Task 7.1
        print("График ковариационной (автокорреляционной) функции для случайного шума")
        default_noise_1 = Model.noise(N=1000, R=10)
        harm_1 = Model.harm(N=1000, A0=100, f0=33)

        plt.plot(default_noise_1.x, Analysis.acf(default_noise_1))
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        print("График ковариационной (автокорреляционной) функции для гармонического процесса")
        plt.plot(harm_1.x, Analysis.acf(harm_1))
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        # Task 7.2

        default_noise_2 = Model.noise(N=1000, R=10)
        my_noise_1 = Model.my_noise(N=1000, R=10)
        my_noise_2 = Model.my_noise(N=1000, R=10)
        harm_2 = Model.harm(N=1000, A0=50, f0=33)

        print("График взаимнокорреляционной (кросскорреляционной, кросс-ковариационной) функции для dataX и dataY"
              " случайного шума, реализованного стандартными библиотеками псевдослучайных чисел")
        plt.plot(default_noise_1.x, Analysis.ccf(default_noise_1, default_noise_2))
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        print("График взаимнокорреляционной (кросскорреляционной, кросс-ковариационной) функции для dataX и dataY"
              " случайного шума, реализованного с помощью самописной библиотеки псевдослучайных чисел")
        plt.plot(my_noise_1.x, Analysis.ccf(my_noise_1, my_noise_2))
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        print("График взаимнокорреляционной (кросскорреляционной, кросс-ковариационной) функции для dataX и dataY"
              " гармонического процесса")
        plt.plot(harm_1.x, Analysis.ccf(harm_1, harm_2))
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        # Task 7.3

        print("Удаление смещения")

        shifted_noise = Model.shift(default_noise_1, 20)

        plt.subplot(211)
        plt.plot(shifted_noise.x, shifted_noise.y)
        plt.subplot(212)
        plt.plot(shifted_noise.x, Processing.anti_shift(shifted_noise).y)

        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        plt.clf()

        # Task 7.4

        print("Удаление выбросов, случайный шум с добавлением выбросов")

        impulsed_noise = Model.impulse_noise(default_noise_1)
        anti_spike_noise = Processing.anti_spike(impulsed_noise, 100)

        plt.subplot(211)
        plt.plot(impulsed_noise.x, impulsed_noise.y)
        plt.subplot(212)
        plt.plot(anti_spike_noise.x, anti_spike_noise.y)
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        print("Удаление выбросов, гармонический процесс с добавлением выбросов")

        impulsed_harm = Model.impulse_noise(harm_1)
        anti_spike_harm = Processing.anti_spike(harm_1, 200)

        plt.subplot(211)
        plt.plot(impulsed_harm.x, impulsed_harm.y)
        plt.subplot(212)
        plt.plot(anti_spike_harm.x, anti_spike_harm.y)
        plt.show()

    elif i == 8:
        print("Функция аддитивной модели")
        print("...линейного тренда trend и гармонического процесса harm")

        lin = Model.trend(N=1000, a=0.1, b=20, data_type=DataType.LINEAR)
        f0 = 250
        harm = Model.harm(N=1000, A0=5, f0=f0)

        added_a = Model.add_model(lin, harm)
        plt.plot(added_a.x, added_a.y)
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        print("...экспоненциального тренда trend и случайного шума noise")

        exp = Model.trend(N=1000, a=0.002, b=10, data_type=DataType.EXPONENTIAL)
        noise = Model.noise(N=1000, R=10)

        added_b = Model.add_model(exp, noise)
        plt.plot(added_b.x, added_b.y)
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        print("Удаление линейного тренда из первого графика")

        anti_lin = Processing.anti_shift(Processing.anti_trend_linear(added_a))
        anti_lin.y = anti_lin.y # * (166.5/f0)
        plt.plot(anti_lin.x, anti_lin.y)
        plt.show()

        # Амплитуда меняется в зависимости от частоты изначального процесса
        # Отношение новой амплитуды к старой:
        # 0.309, 0.308, 0.3086, 0.309 при f=50
        # 0.1254 при f=20
        # ~1.0 при f=166 и f=167
        # Чтобы вернуть амплитуду, можно умножить данные на 166.5/f0
        # Update: неверно для частот > 166
        old_A = harm.A
        new_A_1 = np.amax(anti_lin.y)
        new_A_2 = np.amin(anti_lin.y)

        print("old A = " + str(old_A) + " new A_1 = " + str(new_A_1) + " new A_2 = " + str(new_A_2))

        print("Нажмите Enter для следующего графика...")
        input()

        print("Удаление экспоненциального тренда из второго графика")

        anti_exp_1 = Processing.anti_trend_non_linear(added_b, 10)
        anti_exp_2 = Processing.anti_trend_non_linear(added_b, 15)
        anti_exp_3 = Processing.anti_trend_non_linear(added_b, 20)
        anti_exp_4 = Processing.anti_trend_non_linear(added_b, 25)
        anti_exp_5 = Processing.anti_trend_non_linear(added_b, 30)
        plt.subplot(321)
        plt.plot(noise.x, noise.y)
        plt.subplot(322)
        plt.plot(anti_exp_1.x, anti_exp_1.y)
        plt.subplot(323)
        plt.plot(anti_exp_2.x, anti_exp_2.y)
        plt.subplot(324)
        plt.plot(anti_exp_3.x, anti_exp_3.y)
        plt.subplot(325)
        plt.plot(anti_exp_4.x, anti_exp_4.y)
        plt.subplot(326)
        plt.plot(anti_exp_5.x, anti_exp_5.y)
        plt.show()

    elif i == 9:

        dt = 0.002

        harm = Model.harm(N=1000, dt=dt, f0=33)
        polyharm = Model.poly_harm(N=1000, dt=dt, f0=33, f1=5)

        print("Амплитудный спектр Фурье для гармонического процесса")

        spec = Analysis.spectre_fourier(Xn=Analysis.fourier(harm))
        plt.plot(spec.x, spec.y)
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        print("Амплитудный спектр Фурье для полигармонического процесса")

        spec = Analysis.spectre_fourier(Xn=Analysis.fourier(polyharm))
        plt.plot(spec.x, spec.y)
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        print("Амплитудный спектр Фурье для гармонического процесса c окном 24")

        harm = Model.harm(N=1024, dt=dt)
        spec = Analysis.spectre_fourier(Xn=Analysis.fourier(harm, window=24))
        plt.plot(spec.x, spec.y)
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        print("Амплитудный спектр Фурье для полигармонического процесса c окном 24")

        polyharm = Model.poly_harm(N=1024, dt=dt)
        spec = Analysis.spectre_fourier(Xn=Analysis.fourier(polyharm, window=24))
        plt.plot(spec.x, spec.y)
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        print("Амплитудный спектр Фурье для гармонического процесса c окном 124")

        harm = Model.harm(N=1024, dt=dt)
        spec = Analysis.spectre_fourier(Xn=Analysis.fourier(harm, window=124))
        plt.plot(spec.x, spec.y)
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        print("Амплитудный спектр Фурье для полигармонического процесса c окном 124")

        polyharm = Model.poly_harm(N=1024, dt=dt)
        spec = Analysis.spectre_fourier(Xn=Analysis.fourier(polyharm, window=124))
        plt.plot(spec.x, spec.y)
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        print("Амплитудный спектр Фурье для гармонического процесса c окном 224")

        harm = Model.harm(N=1024, dt=dt)
        spec = Analysis.spectre_fourier(Xn=Analysis.fourier(harm, window=224))
        plt.plot(spec.x, spec.y)
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        print("Амплитудный спектр Фурье для полигармонического процесса c окном 224")

        polyharm = Model.poly_harm(N=1024, dt=dt)
        spec = Analysis.spectre_fourier(Xn=Analysis.fourier(polyharm, window=224))
        plt.plot(spec.x, spec.y)
        plt.show()

    elif i == 10:
        print("Подавление случайного шума")
        for M in [1, 10, 100, 10000]:
            anti_noise = Processing.anti_noise(M=M)
            plt.plot(anti_noise.x, anti_noise.y)
            plt.show()

            print("Стандартное отклонение при M = " + str(M) + ": " + str(anti_noise.y.std()))
            print("Нажмите Enter для следующего графика...")
            input()

        M_values = []
        M_std_results = []
        M_values.append(1)
        for i in range(10, 1001, 20):
            M_values.append(i)

        for i in M_values:
            anti_noise = Processing.anti_noise(M=i)
            M_std_results.append(anti_noise.y.std())

        M_values = np.array(M_values)
        M_std_results = np.array(M_std_results)

        plt.plot(M_values, M_std_results)
        plt.show()

        print("График зависимости стандартного отклонения от M")
        print("Нажмите Enter для следующего графика...")
        input()

        harm = Model.harm(dt=0.001, f0=5, A0=10)
        print("Подавление случайного шума в аддитивной модели шума и гармонического процесса")
        for M in [1, 10, 100, 10000]:
            anti_noise = Processing.anti_noise(data=harm, M=M)
            plt.plot(anti_noise.x, anti_noise.y)
            plt.show()

            print("Стандартное отклонение при M = " + str(M) + ": " + str(anti_noise.y.std()))
            print("Нажмите Enter для следующего графика...")
            input()

    elif i == 11:
        data = InOut.read_dat("data/pgp_2ms.dat")
        # data = InOut.read_dat("data/newfile_a1fc33f6-e871-431c-b0dd-990a34bb1340.dat")
        plt.plot(np.arange(1000), data)
        plt.show()

        # InOut.write_dat("data/", data)

        print("Прочитанные данные из файла")
        print("Нажмите Enter для следующего графика...")
        input()

        harm = Model.harm(N=1000, dt=0.002)
        harm.y = data
        spec = Analysis.spectre_fourier(Xn=Analysis.fourier(harm))
        plt.plot(spec.x, spec.y)
        plt.show()

        freqs = []
        ampls = []
        e = 0.05  # порог

        if spec.y[0] - spec.y[1] > e:
            freqs.append(spec.x[0])
            ampls.append(float(spec.y[0]) * 2)
        for i in range(1, len(spec.y) - 1):
            if spec.y[i] - spec.y[i - 1] > e and spec.y[i] - spec.y[i + 1] > e:
                freqs.append(spec.x[i])
                ampls.append(float(spec.y[i]) * 2)
        if spec.y[len(spec.y) - 1] - spec.y[len(spec.y) - 2] > e:
            freqs.append(spec.x[len(spec.y) - 1])
            ampls.append(float(spec.y[len(spec.y) - 1]) * 2)

        print("Амплитудный спектр данных из файла")
        print("Гармоники:")
        for i in range(0, len(freqs)):
            print(str(i + 1) + ". Частота " + str(freqs[i]) + ", амплитуда " + str(ampls[i]))
        print("Нажмите Enter для следующего графика...")
        input()

        N = 1000
        M = 200

        harm = Model.harm(N=M, A0=1, f0=7, dt=0.005)
        trend = Model.trend(N=M, a=-30*0.005, b=1, data_type=DataType.EXPONENTIAL)
        ht = Model.mult_model(harm, trend)
        max_ht = ht.y.max(initial=float('-inf'))
        ht.y = (ht.y / max_ht) * 120

        xt = Model.noise(N=N, R=0)
        for i in [200, 400, 600, 800]:
            xt.y[i] = np.random.uniform(0.9, 1.1)

        yt = Model.noise(N=N + M, R=0)

        for k in range(N + M):
            yt.y[k] = 0
            for m in range(M):
                if k < m or k >= 1000:
                    continue
                yt.y[k] += xt.y[k - m] * ht.y[m]

        yt.y = yt.y[:N]
        yt.x = yt.x[:N]
        yt.N = N

        plt.rcParams["figure.figsize"] = (8, 13)

        plt.subplot(311)
        plt.plot(ht.x, ht.y)
        plt.xlabel("Импульсная реакция линейной модели сердечной мышцы")
        plt.subplot(312)
        plt.plot(xt.x, xt.y)
        plt.xlabel("Управляющая функция ритма")
        plt.subplot(313)
        plt.plot(yt.x, yt.y)
        plt.xlabel("Первое приближение модели кардиограммы")
        plt.subplots_adjust(hspace=0.5)
        plt.show()

    elif i == 12:
        m = 64
        dt = 0.002

        lpf = Model.poly_harm(N=(m * 2 + 1), dt=dt)
        hpf = Model.poly_harm(N=(m * 2 + 1), dt=dt)
        bpf = Model.poly_harm(N=(m * 2 + 1), dt=dt)
        bsf = Model.poly_harm(N=(m * 2 + 1), dt=dt)

        lpf.y = Processing.lpf(m=m, dt=dt)
        hpf.y = Processing.hpf(m=m, dt=dt)
        bpf.y = Processing.bpf(m=m, dt=dt)
        bsf.y = Processing.bsf(m=m, dt=dt)

        plt.rcParams["figure.figsize"] = (8, 13)

        plt.subplot(411)
        plt.plot(lpf.x, lpf.y)
        plt.xlabel("lpf")
        plt.subplot(412)
        plt.plot(hpf.x, hpf.y)
        plt.xlabel("hpf")
        plt.subplot(413)
        plt.plot(bpf.x, bpf.y)
        plt.xlabel("bpf")
        plt.subplot(414)
        plt.plot(bsf.x, bsf.y)
        plt.xlabel("bsf")
        plt.subplots_adjust(hspace=0.5)
        plt.show()

        print("Графики весовых функций")
        print("Нажмите Enter для следующего графика...")
        input()

        spec_lpf = Analysis.spectre_fourier(Analysis.fourier(lpf))
        spec_lpf.y = spec_lpf.y * (m * 2 + 1)
        spec_hpf = Analysis.spectre_fourier(Analysis.fourier(hpf))
        spec_hpf.y = spec_hpf.y * (m * 2 + 1)
        spec_bpf = Analysis.spectre_fourier(Analysis.fourier(bpf))
        spec_bpf.y = spec_bpf.y * (m * 2 + 1)
        spec_bsf = Analysis.spectre_fourier(Analysis.fourier(bsf))
        spec_bsf.y = spec_bsf.y * (m * 2 + 1)

        plt.subplot(411)
        plt.plot(spec_lpf.x, spec_lpf.y)
        plt.xlabel("lpf")
        plt.subplot(412)
        plt.plot(spec_hpf.x, spec_hpf.y)
        plt.xlabel("hpf")
        plt.subplot(413)
        plt.plot(spec_bpf.x, spec_bpf.y)
        plt.xlabel("bpf")
        plt.subplot(414)
        plt.plot(spec_bsf.x, spec_bsf.y)
        plt.xlabel("bsf")
        plt.subplots_adjust(hspace=0.5)
        plt.show()

        print("Амплитудный спектр весовых функций")

    elif i == 13:

        data = InOut.read_dat("data/pgp_2ms.dat")

        polyharm = Model.harm(N=1000, dt=0.002)
        polyharm.y = data
        spec = Analysis.spectre_fourier(Xn=Analysis.fourier(polyharm))

        freqs = []
        ampls = []
        e = 0.05  # порог

        if spec.y[0] - spec.y[1] > e:
            freqs.append(spec.x[0])
            ampls.append(float(spec.y[0]) * 2)
        for i in range(1, len(spec.y) - 1):
            if spec.y[i] - spec.y[i - 1] > e and spec.y[i] - spec.y[i + 1] > e:
                freqs.append(spec.x[i])
                ampls.append(float(spec.y[i]) * 2)
        if spec.y[len(spec.y) - 1] - spec.y[len(spec.y) - 2] > e:
            freqs.append(spec.x[len(spec.y) - 1])
            ampls.append(float(spec.y[len(spec.y) - 1]) * 2)

        print("Гармоники:")
        for i in range(0, len(freqs)):
            print(str(i + 1) + ". Частота " + str(freqs[i]) + ", амплитуда " + str(ampls[i]))

        plt.rcParams["figure.figsize"] = (8, 13)

        m = 128
        dt = 0.002
        filters = [Processing.lpf(m=m, dt=dt, fc=13),
                   Processing.hpf(m=m, dt=dt, fc=90),
                   Processing.bpf(m=m, dt=dt, fc1=18, fc2=42),
                   Processing.bsf(m=m, dt=dt, fc1=6, fc2=40)]

        for filt in filters:
            plt.subplot(511)
            plt.plot(np.arange(1000), data)
            plt.xlabel("Исходные данные")

            plt.subplot(512)
            plt.plot(spec.x, spec.y)
            plt.xlabel("Спектр исходных данные")

            plt.subplot(513)
            packed_filter = Model.poly_harm(N=(m * 2 + 1), dt=dt)
            packed_filter.y = filt
            spec_filt = Analysis.spectre_fourier(Analysis.fourier(packed_filter))
            spec_filt.y = spec_filt.y * (m * 2 + 1)
            plt.plot(spec_filt.x, spec_filt.y)
            plt.xlabel("Частотная характеристика фильтра")

            plt.subplot(514)
            filtered = Processing.convol(polyharm, packed_filter)
            filtered.N = 900
            filtered.x = filtered.x[100:1000]
            filtered.y = filtered.y[100:1000]
            plt.plot(filtered.x, filtered.y)
            plt.xlabel("Отфильтрованные данные")

            plt.subplot(515)
            spec_filtered = Analysis.spectre_fourier(Analysis.fourier(filtered))
            plt.plot(spec_filtered.x, spec_filtered.y)
            plt.xlabel("Спектр отфильтрованных данных")
            plt.subplots_adjust(hspace=0.3)

            plt.show()
            print("Нажмите Enter для следующего графика...")
            input()

    elif i == 14:
        rate, data = InOut.read_wav("data/вИна.wav")
        N = len(data)
        dt = 1 / rate

        model = Model.poly_harm(N=N, dt=dt)
        model.y = data
        plt.plot(model.x, model.y)
        plt.xlabel("Осциллограмма голосовой записи")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        multdata = Model.trend(N=N, data_type=DataType.LINEAR, a=0, b=0)

        multdata.y = np.ndarray([N], dtype=float)

        for i in range(5000):
            multdata.y[i] = 0.0

        for i in range(5000, 14000):
            multdata.y[i] = 0.5

        for i in range(14000, 16000):
            multdata.y[i] = 0.0

        for i in range(16000, 21700):
            multdata.y[i] = 4.0

        for i in range(21700, N):
            multdata.y[i] = 0.0

        result = Model.mult_model(model, multdata)
        result.y = result.y.astype(dtype="int16")
        plt.plot(result.x, result.y)
        plt.xlabel("Осциллограмма голосовой записи после изменения ударения")
        plt.show()
        print("Нажмите Enter для следующего графика...")
        input()

        InOut.write_wav(path_to_file="data/", rate=rate, data=result.y)
        # InOut.write_wav(path_to_file="data/", rate=rate, data=data)
        print("wav файл был записан")

    elif i == 15:
        rate, data = InOut.read_wav("data/вИна.wav")
        N = len(data)
        dt = 1 / rate
        data = data.astype(dtype=np.float32)

        model = Model.poly_harm(N=N, dt=dt)
        model.y = data
        plt.subplot(311)
        plt.plot(model.x, model.y)
        plt.xlabel("Осциллограмма голосовой записи")

        syllable1_data = data[5000:14000]
        syllable2_data = data[16000:21700]

        syllable1 = Model.poly_harm(N=len(syllable1_data), dt=dt)
        syllable1.y = syllable1_data
        plt.subplot(312)
        plt.plot(syllable1.x, syllable1.y)
        plt.xlabel("Осциллограмма первого слога")

        syllable2 = Model.poly_harm(N=len(syllable2_data), dt=dt)
        syllable2.y = syllable2_data
        plt.subplot(313)
        plt.plot(syllable2.x, syllable2.y)
        plt.xlabel("Осциллограмма второго слога")

        plt.subplots_adjust(hspace=0.3)
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        if os.path.exists("data/spec_data.dat"):
            raw_spec_data = InOut.read_dat("data/spec_data.dat")
            spec_data = Model.poly_harm(N=len(raw_spec_data), dt=dt)
            spec_data.y = raw_spec_data
            spec_data.x = spec_data.x * (rate / (spec_data.N * 2))
        else:
            spec_data = Analysis.spectre_fourier(Xn=Analysis.fourier(model))
            InOut.write_dat("data/", spec_data.y, file_name="spec_data")

        if os.path.exists("data/spec_syllable1.dat"):
            raw_spec_syllable1 = InOut.read_dat("data/spec_syllable1.dat")
            spec_syllable1 = Model.poly_harm(N=len(raw_spec_syllable1), dt=dt)
            spec_syllable1.y = raw_spec_syllable1
            spec_syllable1.x = spec_syllable1.x * (rate / (spec_syllable1.N * 2))
        else:
            spec_syllable1 = Analysis.spectre_fourier(Xn=Analysis.fourier(syllable1))
            InOut.write_dat("data/", spec_syllable1.y, file_name="spec_syllable1")

        if os.path.exists("data/spec_syllable2.dat"):
            raw_spec_syllable2 = InOut.read_dat("data/spec_syllable2.dat")
            spec_syllable2 = Model.poly_harm(N=len(raw_spec_syllable2), dt=dt)
            spec_syllable2.y = raw_spec_syllable2
            spec_syllable2.x = spec_syllable2.x * (rate / (spec_syllable2.N * 2))
        else:
            spec_syllable2 = Analysis.spectre_fourier(Xn=Analysis.fourier(syllable2))
            InOut.write_dat("data/", spec_syllable2.y, file_name="spec_syllable2")

        new_N = int(spec_data.N / 2)
        spec_data.y = spec_data.y[:new_N]
        spec_data.x = spec_data.x[:new_N]
        spec_data.N = new_N

        new_N = int(spec_syllable1.N / 2)
        spec_syllable1.y = spec_syllable1.y[:new_N]
        spec_syllable1.x = spec_syllable1.x[:new_N]
        spec_syllable1.N = new_N

        new_N = int(spec_syllable2.N / 2)
        spec_syllable2.y = spec_syllable2.y[:new_N]
        spec_syllable2.x = spec_syllable2.x[:new_N]
        spec_syllable2.N = new_N

        plt.plot(spec_data.x, spec_data.y)
        plt.xlabel("Амплитудный спектр всего слова")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        plt.plot(spec_syllable1.x, spec_syllable1.y)
        plt.xlabel("Амплитудный спектр первого слога")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        plt.plot(spec_syllable2.x, spec_syllable2.y)
        plt.xlabel("Амплитудный спектр второго слога")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        m = 64
        # выделение ОТ и формант первого слога

        ot = Processing.lpf(m=m, dt=dt, fc=400)
        f1 = Processing.bpf(m=m, dt=dt, fc1=2200, fc2=2700)
        f2 = Processing.bpf(m=m, dt=dt, fc1=2700, fc2=3400)

        # Основной тон
        packed_filter = Model.poly_harm(N=(m * 2 + 1), dt=dt)
        packed_filter.y = ot

        filtered = Processing.convol(syllable1, packed_filter)
        plt.plot(filtered.x, filtered.y)
        plt.xlabel("Основной тон первого слога")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        if os.path.exists("data/spec_OT_s1.dat"):
            raw_spec_filtered = InOut.read_dat("data/spec_OT_s1.dat")
            spec_filtered = Model.poly_harm(N=len(raw_spec_filtered), dt=dt)
            spec_filtered.y = raw_spec_filtered
            spec_filtered.x = spec_filtered.x * (rate / (spec_filtered.N * 2))
        else:
            spec_filtered = Analysis.spectre_fourier(Analysis.fourier(filtered))
            spec_filtered.y = spec_filtered.y.astype(dtype=np.float32)
            InOut.write_dat("data/", spec_filtered.y, file_name="spec_OT_s1")

        new_N = int(spec_filtered.N / 2)
        spec_filtered.y = spec_filtered.y[:new_N]
        spec_filtered.x = spec_filtered.x[:new_N]
        spec_filtered.N = new_N

        plt.plot(spec_filtered.x, spec_filtered.y)
        plt.xlabel("Спектр основного тона первого слога")
        plt.show()

        InOut.write_wav(path_to_file="data/", rate=rate, data=filtered.y, file_name="OT_s1")
        print("Нажмите Enter для следующего графика...")
        input()

        # Первая форманта

        packed_filter = Model.poly_harm(N=(m * 2 + 1), dt=dt)
        packed_filter.y = f1

        filtered = Processing.convol(syllable1, packed_filter)
        plt.plot(filtered.x, filtered.y)
        plt.xlabel("Первая форманта первого слога")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        if os.path.exists("data/spec_f1_s1.dat"):
            raw_spec_filtered = InOut.read_dat("data/spec_f1_s1.dat")
            spec_filtered = Model.poly_harm(N=len(raw_spec_filtered), dt=dt)
            spec_filtered.y = raw_spec_filtered
            spec_filtered.x = spec_filtered.x * (rate / (spec_filtered.N * 2))
        else:
            spec_filtered = Analysis.spectre_fourier(Analysis.fourier(filtered))
            spec_filtered.y = spec_filtered.y.astype(dtype=np.float32)
            InOut.write_dat("data/", spec_filtered.y, file_name="spec_f1_s1")

        new_N = int(spec_filtered.N / 2)
        spec_filtered.y = spec_filtered.y[:new_N]
        spec_filtered.x = spec_filtered.x[:new_N]
        spec_filtered.N = new_N

        plt.plot(spec_filtered.x, spec_filtered.y)
        plt.xlabel("Спектр первой форманты первого слога")
        plt.show()

        InOut.write_wav(path_to_file="data/", rate=rate, data=filtered.y, file_name="f1_s1")
        print("Нажмите Enter для следующего графика...")
        input()

        # Вторая форманта

        packed_filter = Model.poly_harm(N=(m * 2 + 1), dt=dt)
        packed_filter.y = f2

        filtered = Processing.convol(syllable1, packed_filter)
        plt.plot(filtered.x, filtered.y)
        plt.xlabel("Вторая форманта первого слога")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        if os.path.exists("data/spec_f2_s1.dat"):
            raw_spec_filtered = InOut.read_dat("data/spec_f2_s1.dat")
            spec_filtered = Model.poly_harm(N=len(raw_spec_filtered), dt=dt)
            spec_filtered.y = raw_spec_filtered
            spec_filtered.x = spec_filtered.x * (rate / (spec_filtered.N * 2))
        else:
            spec_filtered = Analysis.spectre_fourier(Analysis.fourier(filtered))
            spec_filtered.y = spec_filtered.y.astype(dtype=np.float32)
            InOut.write_dat("data/", spec_filtered.y, file_name="spec_f2_s1")

        new_N = int(spec_filtered.N / 2)
        spec_filtered.y = spec_filtered.y[:new_N]
        spec_filtered.x = spec_filtered.x[:new_N]
        spec_filtered.N = new_N

        plt.plot(spec_filtered.x, spec_filtered.y)
        plt.xlabel("Спектр второй форманты первого слога")
        plt.show()

        InOut.write_wav(path_to_file="data/", rate=rate, data=filtered.y, file_name="f2_s1")
        print("Нажмите Enter для следующего графика...")
        input()

        # выделение ОТ и формант второго слога

        ot = Processing.lpf(m=m, dt=dt, fc=400)
        f1 = Processing.bpf(m=m, dt=dt, fc1=500, fc2=900)
        f2 = Processing.bpf(m=m, dt=dt, fc1=1200, fc2=1700)
        f3 = Processing.bpf(m=m, dt=dt, fc1=2800, fc2=3200)
        f4 = Processing.bpf(m=m, dt=dt, fc1=3500, fc2=4100)

        # Основной тон
        packed_filter = Model.poly_harm(N=(m * 2 + 1), dt=dt)
        packed_filter.y = ot

        filtered = Processing.convol(syllable2, packed_filter)
        plt.plot(filtered.x, filtered.y)
        plt.xlabel("Основной тон второго слога")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        if os.path.exists("data/spec_OT_s2.dat"):
            raw_spec_filtered = InOut.read_dat("data/spec_OT_s2.dat")
            spec_filtered = Model.poly_harm(N=len(raw_spec_filtered), dt=dt)
            spec_filtered.y = raw_spec_filtered
            spec_filtered.x = spec_filtered.x * (rate / (spec_filtered.N * 2))
        else:
            spec_filtered = Analysis.spectre_fourier(Analysis.fourier(filtered))
            spec_filtered.y = spec_filtered.y.astype(dtype=np.float32)
            InOut.write_dat("data/", spec_filtered.y, file_name="spec_OT_s2")

        new_N = int(spec_filtered.N / 2)
        spec_filtered.y = spec_filtered.y[:new_N]
        spec_filtered.x = spec_filtered.x[:new_N]
        spec_filtered.N = new_N

        plt.plot(spec_filtered.x, spec_filtered.y)
        plt.xlabel("Спектр основного тона второго слога")
        plt.show()

        InOut.write_wav(path_to_file="data/", rate=rate, data=filtered.y, file_name="OT_s2")
        print("Нажмите Enter для следующего графика...")
        input()

        # Первая форманта

        packed_filter = Model.poly_harm(N=(m * 2 + 1), dt=dt)
        packed_filter.y = f1

        filtered = Processing.convol(syllable2, packed_filter)
        plt.plot(filtered.x, filtered.y)
        plt.xlabel("Первая форманта второго слога")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        if os.path.exists("data/spec_f1_s2.dat"):
            raw_spec_filtered = InOut.read_dat("data/spec_f1_s2.dat")
            spec_filtered = Model.poly_harm(N=len(raw_spec_filtered), dt=dt)
            spec_filtered.y = raw_spec_filtered
            spec_filtered.x = spec_filtered.x * (rate / (spec_filtered.N * 2))
        else:
            spec_filtered = Analysis.spectre_fourier(Analysis.fourier(filtered))
            spec_filtered.y = spec_filtered.y.astype(dtype=np.float32)
            InOut.write_dat("data/", spec_filtered.y, file_name="spec_f1_s2")

        new_N = int(spec_filtered.N / 2)
        spec_filtered.y = spec_filtered.y[:new_N]
        spec_filtered.x = spec_filtered.x[:new_N]
        spec_filtered.N = new_N

        plt.plot(spec_filtered.x, spec_filtered.y)
        plt.xlabel("Спектр первой форманты второго слога")
        plt.show()

        InOut.write_wav(path_to_file="data/", rate=rate, data=filtered.y, file_name="f1_s2")
        print("Нажмите Enter для следующего графика...")
        input()

        # Вторая форманта

        packed_filter = Model.poly_harm(N=(m * 2 + 1), dt=dt)
        packed_filter.y = f2

        filtered = Processing.convol(syllable2, packed_filter)
        plt.plot(filtered.x, filtered.y)
        plt.xlabel("Вторая форманта второго слога")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        if os.path.exists("data/spec_f2_s2.dat"):
            raw_spec_filtered = InOut.read_dat("data/spec_f2_s2.dat")
            spec_filtered = Model.poly_harm(N=len(raw_spec_filtered), dt=dt)
            spec_filtered.y = raw_spec_filtered
            spec_filtered.x = spec_filtered.x * (rate / (spec_filtered.N * 2))
        else:
            spec_filtered = Analysis.spectre_fourier(Analysis.fourier(filtered))
            spec_filtered.y = spec_filtered.y.astype(dtype=np.float32)
            InOut.write_dat("data/", spec_filtered.y, file_name="spec_f2_s2")

        new_N = int(spec_filtered.N / 2)
        spec_filtered.y = spec_filtered.y[:new_N]
        spec_filtered.x = spec_filtered.x[:new_N]
        spec_filtered.N = new_N

        plt.plot(spec_filtered.x, spec_filtered.y)
        plt.xlabel("Спектр второй форманты второго слога")
        plt.show()

        InOut.write_wav(path_to_file="data/", rate=rate, data=filtered.y, file_name="f2_s2")
        print("Нажмите Enter для следующего графика...")
        input()

        # Третья форманта

        packed_filter = Model.poly_harm(N=(m * 2 + 1), dt=dt)
        packed_filter.y = f3

        filtered = Processing.convol(syllable2, packed_filter)
        plt.plot(filtered.x, filtered.y)
        plt.xlabel("Третья форманта второго слога")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        if os.path.exists("data/spec_f3_s2.dat"):
            raw_spec_filtered = InOut.read_dat("data/spec_f3_s2.dat")
            spec_filtered = Model.poly_harm(N=len(raw_spec_filtered), dt=dt)
            spec_filtered.y = raw_spec_filtered
            spec_filtered.x = spec_filtered.x * (rate / (spec_filtered.N * 2))
        else:
            spec_filtered = Analysis.spectre_fourier(Analysis.fourier(filtered))
            spec_filtered.y = spec_filtered.y.astype(dtype=np.float32)
            InOut.write_dat("data/", spec_filtered.y, file_name="spec_f3_s2")

        new_N = int(spec_filtered.N / 2)
        spec_filtered.y = spec_filtered.y[:new_N]
        spec_filtered.x = spec_filtered.x[:new_N]
        spec_filtered.N = new_N

        plt.plot(spec_filtered.x, spec_filtered.y)
        plt.xlabel("Спектр третьей форманты второго слога")
        plt.show()

        InOut.write_wav(path_to_file="data/", rate=rate, data=filtered.y, file_name="f3_s2")
        print("Нажмите Enter для следующего графика...")
        input()

        # Четвертая форманта

        packed_filter = Model.poly_harm(N=(m * 2 + 1), dt=dt)
        packed_filter.y = f4

        filtered = Processing.convol(syllable2, packed_filter)
        plt.plot(filtered.x, filtered.y)
        plt.xlabel("Четвертая форманта второго слога")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        print("Нажмите Enter для следующего графика...")
        input()

        if os.path.exists("data/spec_f4_s2.dat"):
            raw_spec_filtered = InOut.read_dat("data/spec_f4_s2.dat")
            spec_filtered = Model.poly_harm(N=len(raw_spec_filtered), dt=dt)
            spec_filtered.y = raw_spec_filtered
            spec_filtered.x = spec_filtered.x * (rate / (spec_filtered.N * 2))
        else:
            spec_filtered = Analysis.spectre_fourier(Analysis.fourier(filtered))
            spec_filtered.y = spec_filtered.y.astype(dtype=np.float32)
            InOut.write_dat("data/", spec_filtered.y, file_name="spec_f4_s2")

        new_N = int(spec_filtered.N / 2)
        spec_filtered.y = spec_filtered.y[:new_N]
        spec_filtered.x = spec_filtered.x[:new_N]
        spec_filtered.N = new_N

        plt.plot(spec_filtered.x, spec_filtered.y)
        plt.xlabel("Спектр четвертой форманты второго слога")
        plt.show()

        InOut.write_wav(path_to_file="data/", rate=rate, data=filtered.y, file_name="f4_s2")

    elif i == 16:
        # Шум окружения
        N = 10000
        R = 1
        random_noise = Model.noise(N=N, R=R)
        outer_noise = Model.impulse_noise(data=random_noise, R=100) # надо бы проверить различные R для impulse noise
        # outer_noise - это шум окружающей (внешней) среды без шума поезда

        plt.plot(outer_noise.x, outer_noise.y)
        plt.xlabel("Шум окружающей среды")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        # Шум поезда
        R = 2
        f_gr = 5000  # граничная частота
        f_disc = f_gr * 2  # 10000, частота дискретизации
        dt = 1 / f_disc  # 0.0001, шаг времени
        # так как у нас N=10000 и dt=0.0001, это значит, что длительность записи 1 секунда
        # данные были считаны 10000 раз с промежутком в 0.0001 секунды
        random_noise_data = Model.noise(N=N, R=R)
        random_noise = Model.harm(N=N, dt=dt)
        random_noise.y = random_noise_data.y

        m = 16  # настройки фильтра
        fc1 = 800  # настройки фильтра - начальная частота
        fc2 = 900  # настройки фильтра - конечная частота
        bpf = Processing.bpf(fc1=fc1, fc2=fc2, m=m, dt=dt)  # высчитываем данные фильтра
        packed_filter = Model.poly_harm(N=(m * 2 + 1), dt=dt)  # "упаковываем" данные фильтра
        packed_filter.y = bpf  # "упаковываем" данные фильтра

        train_noise = filtered = Processing.convol(random_noise, packed_filter)  # фильтруем случайный шум

        train_noise.N = N
        train_noise.x = train_noise.x[:N]  # обрезаем лишние данные
        train_noise.y = train_noise.y[:N]  # обрезаем лишние данные

        # spec_section = Analysis.spectre_fourier(Analysis.fourier(train_noise))
        #
        # plt.plot(spec_section.x, spec_section.y)
        # plt.xlabel("Частотный спектр отфильтрованного случайного шума ")
        # plt.show()
        #
        # print("Нажмите Enter для следующего графика...")
        # input()

        a = 0.001  # коэффициенты экспоненты
        b = 0.2  # коэффициенты экспоненты
        exp_trend = Model.trend(N=N, a=a, b=b, data_type=DataType.EXPONENTIAL)  # экспоненциальный тренд
        train_noise = Model.mult_model(train_noise, exp_trend)  # умножаем шум поезда на экспоненциальный тренд

        train_noise.y = train_noise.y * 15  # делаем шум поезда погромче

        plt.plot(train_noise.x, train_noise.y)
        plt.xlabel("Шум поезда")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        # складываем шум окружающей среды с шумом поезда
        model = Model.add_model(train_noise, outer_noise)
        model.y = model.y * 2  # делаем все вместе погромче

        plt.plot(model.x, model.y)
        plt.xlabel("Шум поезда + шум окружающей среды")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        # Записываем в файл
        InOut.write_wav("data/", data=model.y, rate=f_disc, file_name="train")

        # вычисляем спектры отрезков по 1000 каждый
        M = int(N / 10)  # 1000
        for i in range(10):
            section_data = copy.deepcopy(model)
            section_data.N = M
            start = i * M
            end = start + 1000
            section_data.x = section_data.x[0:M]
            section_data.y = section_data.y[start:end]

            spec_section = Analysis.spectre_fourier(Analysis.fourier(section_data))

            plt.plot(spec_section.x, spec_section.y)
            plt.xlabel("Частотный спектр отрезка " + str(i + 1))
            plt.show()

            print("Нажмите Enter для следующего графика...")
            input()

    elif i == 17:
        data = InOut.read_dat("data/v1x2.dat")
        plt.plot(np.arange(len(data)), data)
        plt.show()

        print("Прочитанные данные из файла")
        print("Нажмите Enter для следующего графика...")
        input()

        packed_data = Model.trend(N=len(data), a=1, b=1, data_type=DataType.LINEAR)
        packed_data.y = data
        non_trend_data = Processing.anti_trend_non_linear(packed_data)

        plt.plot(non_trend_data.x, non_trend_data.y)
        plt.show()

        print("Данные без тренда")
        print("Нажмите Enter для следующего графика...")
        input()

        packed_data = Model.harm(N=len(non_trend_data.y), dt=0.001)
        packed_data.y = non_trend_data.y
        spec = Analysis.spectre_fourier(Xn=Analysis.fourier(packed_data))

        plt.plot(spec.x, spec.y)
        plt.show()

        print("Спектр промежуточных данных (для определения настроек фильтра)")
        print("Нажмите Enter для следующего графика...")
        input()

        bsf = Processing.bsf(m=64, fc1=60, fc2=80, dt=0.001)
        packed_filter = Model.poly_harm(N=(64 * 2 + 1), dt=0.001)
        packed_filter.y = bsf

        non_trend_non_harm_data = filtered = Processing.convol(packed_data, packed_filter)
        non_trend_non_harm_data.x = non_trend_non_harm_data.x[100:1000]
        non_trend_non_harm_data.y = non_trend_non_harm_data.y[100:1000]
        non_trend_non_harm_data.N = 900

        plt.plot(non_trend_non_harm_data.x, non_trend_non_harm_data.y)
        plt.show()

        print("Выделенные случайные данные")
        print("Нажмите Enter для следующего графика...")
        input()

        spec = Analysis.spectre_fourier(Xn=Analysis.fourier(non_trend_non_harm_data))

        plt.plot(spec.x, spec.y)
        plt.show()

        print("Спектр случайных данных")
        print("Нажмите Enter для следующего графика...")
        input()

        Analysis.hist(non_trend_non_harm_data, 100)
        plt.show()
        print("Гистограмма случайных данных")
        print("Нажмите Enter для следующего графика...")
        input()

        plt.plot(packed_filter.x, packed_filter.y)
        plt.show()
        print("Фильтр bsf")
        print("Нажмите Enter для следующего графика...")
        input()

        spec = Analysis.spectre_fourier(Xn=Analysis.fourier(packed_filter))

        plt.plot(spec.x, spec.y)
        plt.show()
        print("Спектр фильтра bsf")
        print("Нажмите Enter для следующего графика...")
        input()

    elif i == 18:
        data = InOut.read_dat("data/v1x11.dat")

        packed_data_xy = Model.harm(N=len(data), dt=0.001)
        packed_data_xy.y = data

        plt.plot(packed_data_xy.x, packed_data_xy.y)
        plt.xlabel("Прочитанные данные из файла v1x11.dat")
        plt.show()

        print("Прочитанные данные из файла v1x11.dat")
        print("Нажмите Enter для следующего графика...")
        input()

        data = InOut.read_dat("data/v1y11.dat")

        packed_data_yx = Model.harm(N=len(data), dt=0.001)
        packed_data_yx.y = data

        plt.plot(packed_data_yx.x, packed_data_yx.y)
        plt.xlabel("Прочитанные данные из файла v1y11.dat")
        plt.show()

        print("Прочитанные данные из файла v1y11.dat")
        print("Нажмите Enter для следующего графика...")
        input()

        plt.subplot(211)
        plt.plot(packed_data_xy.x, packed_data_xy.y)
        plt.xlabel("Прочитанные данные из файла v1x11.dat")
        plt.subplot(212)
        plt.plot(packed_data_yx.x, packed_data_yx.y)
        plt.xlabel("Прочитанные данные из файла v1y11.dat")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        ccf = Analysis.ccf(packed_data_xy, packed_data_yx)

        plt.plot(packed_data_yx.x, ccf)
        plt.xlabel("Взаимнокорреляционная функция")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        spec_xy = Analysis.spectre_fourier(Xn=Analysis.fourier(packed_data_xy))

        plt.plot(spec_xy.x, spec_xy.y)
        plt.xlabel("Амплитудный спектр Фурье для v1x11.dat")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        spec_yx = Analysis.spectre_fourier(Xn=Analysis.fourier(packed_data_yx))

        plt.plot(spec_yx.x, spec_yx.y)
        plt.xlabel("Амплитудный спектр Фурье для v1y11.dat")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        plt.subplot(211)
        plt.plot(spec_xy.x[30:len(spec_xy.x)], spec_xy.y[30:len(spec_xy.x)])
        plt.xlabel("Амплитудный спектр Фурье для v1x11.dat")
        plt.subplot(212)
        plt.plot(spec_yx.x[30:len(spec_xy.x)], spec_yx.y[30:len(spec_xy.x)])
        plt.xlabel("Амплитудный спектр Фурье для v1y11.dat")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        ccf_spec = Analysis.ccf(spec_xy, spec_yx)

        plt.plot(spec_xy.x, ccf_spec)
        plt.xlabel("Взаимнокорреляционная функция между спектрами Фурье")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        plt.rcParams["figure.figsize"] = (9.6, 9.6)

        plt.subplot(311)
        plt.plot(spec_xy.x[30:len(spec_xy.x)], ccf_spec[30:len(spec_xy.x)])
        plt.xlabel("Взаимнокорреляционная функция между спектрами Фурье")
        plt.subplot(312)
        plt.plot(spec_xy.x[30:len(spec_xy.x)], spec_xy.y[30:len(spec_xy.x)])
        plt.xlabel("Амплитудный спектр Фурье для v1x11.dat")
        plt.subplot(313)
        plt.plot(spec_yx.x[30:len(spec_xy.x)], spec_yx.y[30:len(spec_xy.x)])
        plt.xlabel("Амплитудный спектр Фурье для v1y11.dat")
        plt.subplots_adjust(hspace=0.3)
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        packed_ccf = Model.harm(N=len(data), dt=0.001)
        packed_ccf.y = ccf

        spec_ccf = Analysis.spectre_fourier(Xn=Analysis.fourier(packed_ccf))

        plt.plot(spec_ccf.x, spec_ccf.y)
        plt.xlabel("Cпектр взаимнокорреляционной функции между данными")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        plt.subplot(311)
        plt.plot(spec_ccf.x[30:len(spec_ccf.x)], spec_ccf.y[30:len(spec_xy.x)])
        plt.xlabel("Cпектр взаимнокорреляционной функции между данными")
        plt.subplot(312)
        plt.plot(spec_xy.x[30:len(spec_xy.x)], spec_xy.y[30:len(spec_xy.x)])
        plt.xlabel("Амплитудный спектр Фурье для v1x11.dat")
        plt.subplot(313)
        plt.plot(spec_yx.x[30:len(spec_xy.x)], spec_yx.y[30:len(spec_xy.x)])
        plt.xlabel("Амплитудный спектр Фурье для v1y11.dat")
        plt.subplots_adjust(hspace=0.3)
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        plt.rcParams["figure.figsize"] = (9.6, 7.2)

        anti_tr_xy = Processing.anti_trend_non_linear(packed_data_xy)

        plt.plot(anti_tr_xy.x, anti_tr_xy.y)
        plt.xlabel("Данные v1x11.dat без тренда")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        # plt.plot(anti_tr_yx.x, anti_tr_yx.y)
        # plt.xlabel("Данные yx без тренда")
        # plt.show()

        # print("Нажмите Enter для следующего графика...")
        # input()

        ccf_2 = Analysis.ccf(anti_tr_xy, packed_data_yx)

        plt.plot(anti_tr_xy.x, ccf_2)
        plt.xlabel("Взаимнокорреляционная функция между данными без трендов")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        spec_xy = Analysis.spectre_fourier(Xn=Analysis.fourier(anti_tr_xy))

        plt.plot(spec_xy.x, spec_xy.y)
        plt.xlabel("Амплитудный спектр Фурье для данных v1x11.dat без тренда")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        # spec_yx = Analysis.spectre_fourier(Xn=Analysis.fourier(anti_tr_yx))

        # plt.plot(spec_yx.x, spec_yx.y)
        # plt.xlabel("Амплитудный спектр Фурье для данных v3yx3.dat без тренда")
        # plt.show()

        # print("Нажмите Enter для следующего графика...")
        # input()

        anti_tr_xy.y = ccf_2

        spec_ccf = Analysis.spectre_fourier(Xn=Analysis.fourier(anti_tr_xy))

        plt.plot(spec_ccf.x, spec_ccf.y)
        plt.xlabel("Амплитудный спектр Фурье для взаимнокорреляционной функции данных без трендов")
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        plt.rcParams["figure.figsize"] = (9.6, 9.6)
        plt.subplot(311)
        plt.plot(spec_ccf.x, spec_ccf.y)
        plt.xlabel("Амплитудный спектр Фурье для взаимнокорреляционной функции данных без трендов")
        plt.subplot(312)
        plt.plot(spec_xy.x, spec_xy.y)
        plt.xlabel("Амплитудный спектр Фурье для данных v1x11.dat без тренда")
        plt.subplot(313)
        plt.plot(spec_yx.x, spec_yx.y)
        plt.xlabel("Амплитудный спектр Фурье для данных v1y11.dat")
        plt.subplots_adjust(hspace=0.3)
        plt.show()

    else:
        exit(0)

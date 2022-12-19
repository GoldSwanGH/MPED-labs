from sys import exit
import matplotlib.pyplot as plt
import numpy as np

from classes.analysis import Analysis
from classes.data_type import DataType
from classes.model import Model
from classes.in_out import InOut
from classes.processing import Processing


while True:
    plt.rcParams["figure.figsize"] = (9.6, 7.2)  # 4:3 формат графиков по умолчанию (оставил), увеличил разрешение в 1.5 раза
    print("Введите номер задания (от 1 до 15) или 0 для выхода: ")
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
        harm_2 = Model.harm(N=1000, A0=100, f0=33)

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

        harm = Model.harm(dt=dt)
        polyharm = Model.poly_harm(dt=dt)

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

        harm = Model.harm(N=1024)
        spec = Analysis.spectre_fourier(Xn=Analysis.fourier(harm, window=24))
        plt.plot(spec.x, spec.y)
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        print("Амплитудный спектр Фурье для полигармонического процесса c окном 24")

        polyharm = Model.poly_harm(N=1024)
        spec = Analysis.spectre_fourier(Xn=Analysis.fourier(polyharm, window=24))
        plt.plot(spec.x, spec.y)
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        print("Амплитудный спектр Фурье для гармонического процесса c окном 124")

        harm = Model.harm(N=1024)
        spec = Analysis.spectre_fourier(Xn=Analysis.fourier(harm, window=124))
        plt.plot(spec.x, spec.y)
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        print("Амплитудный спектр Фурье для полигармонического процесса c окном 124")

        polyharm = Model.poly_harm(N=1024)
        spec = Analysis.spectre_fourier(Xn=Analysis.fourier(polyharm, window=124))
        plt.plot(spec.x, spec.y)
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        print("Амплитудный спектр Фурье для гармонического процесса c окном 224")

        harm = Model.harm(N=1024)
        spec = Analysis.spectre_fourier(Xn=Analysis.fourier(harm, window=224))
        plt.plot(spec.x, spec.y)
        plt.show()

        print("Нажмите Enter для следующего графика...")
        input()

        print("Амплитудный спектр Фурье для полигармонического процесса c окном 224")

        polyharm = Model.poly_harm(N=1024)
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

        InOut.write_dat("data/", data)

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
        pass

    elif i == 0:
        exit(0)

from sys import exit
import matplotlib.pyplot as plt
import numpy as np

from classes.analysis import Analysis
from classes.data_type import DataType
from classes.model import Model
from classes.processing import Processing


while True:
    print("Введите номер задания (от 1 до 13) или 0 для выхода: ")
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

        Analysis.spectre_fourier(Xn=Analysis.fourier(harm))

        print("Нажмите Enter для следующего графика...")
        input()

        print("Амплитудный спектр Фурье для полигармонического процесса")

        Analysis.spectre_fourier(Xn=Analysis.fourier(polyharm))

        print("Нажмите Enter для следующего графика...")
        input()

        print("Амплитудный спектр Фурье для гармонического процесса c окном 24")

        harm = Model.harm(N=1024)
        Analysis.spectre_fourier(Xn=Analysis.fourier(harm, window=24))

        print("Нажмите Enter для следующего графика...")
        input()

        print("Амплитудный спектр Фурье для полигармонического процесса c окном 24")

        polyharm = Model.poly_harm(N=1024)
        Analysis.spectre_fourier(Xn=Analysis.fourier(polyharm, window=24))

        print("Нажмите Enter для следующего графика...")
        input()

        print("Амплитудный спектр Фурье для гармонического процесса c окном 124")

        harm = Model.harm(N=1024)
        Analysis.spectre_fourier(Xn=Analysis.fourier(harm, window=124))

        print("Нажмите Enter для следующего графика...")
        input()

        print("Амплитудный спектр Фурье для полигармонического процесса c окном 124")

        polyharm = Model.poly_harm(N=1024)
        Analysis.spectre_fourier(Xn=Analysis.fourier(polyharm, window=124))

        print("Нажмите Enter для следующего графика...")
        input()

        print("Амплитудный спектр Фурье для гармонического процесса c окном 224")

        harm = Model.harm(N=1024)
        Analysis.spectre_fourier(Xn=Analysis.fourier(harm, window=224))

        print("Нажмите Enter для следующего графика...")
        input()

        print("Амплитудный спектр Фурье для полигармонического процесса c окном 224")

        polyharm = Model.poly_harm(N=1024)
        Analysis.spectre_fourier(Xn=Analysis.fourier(polyharm, window=224))

    elif i == 10:

        pass

    elif i == 11:
        pass

    elif i == 12:
        pass

    elif i == 13:
        pass

    elif i == 0:
        exit(0)

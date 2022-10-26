from sys import exit
import matplotlib.pyplot as plt

from classes.analysis import Analysis
from classes.data_type import DataType
from classes.model import Model
from classes.processing import Processing


while True:
    print("Введите номер задания (от 1 до 7) или 0 для выхода: ")
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
        non_lin_asc = Model.trend(N=10000, a=-0.01, b=10000, data_type=DataType.EXPONENTIAL)
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

    elif i == 0:
        exit(0)

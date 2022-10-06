from sys import exit
import matplotlib.pyplot as plt

from classes.analysis import Analysis
from classes.data_type import DataType
from classes.model import Model


while True:
    print("Введите номер задания (от 1 до 5) или 0 для выхода: ")
    i = int(input())

    match i:
        case 1:
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

        case 2:
            default_noise = Model.noise(N=1000, R=10)
            custom_noise = Model.my_noise(N=1000, R=10)

            plt.subplot(121)
            plt.plot(default_noise.x, default_noise.y, 'b.')

            plt.subplot(122)
            plt.plot(custom_noise.x, custom_noise.y, 'b.')

            plt.show()

        case 3:
            lin_asc = Model.trend(N=1000, a=-2, b=3, data_type=DataType.LINEAR)
            default_noise = Model.noise(N=1000, R=10)
            print()
            print("Тренд:")
            Analysis.statistics(lin_asc)
            print("Случайный шум:")
            Analysis.statistics(default_noise)

            lin_asc = Model.trend(N=10000, a=-2, b=3, data_type=DataType.LINEAR)
            default_noise = Model.noise(N=10000, R=10)
            print()
            print("Тренд:")
            Analysis.stationary(10, lin_asc)
            print("Случайный шум:")
            Analysis.stationary(10, default_noise)

        case 4:
            default_noise = Model.noise(N=1000, R=10)
            shifted_noise = Model.shift(default_noise, 20)

            impulsed_noise = Model.noise(N=1000, R=50)
            Model.impulse_noise(impulsed_noise)

            plt.subplot(221)
            plt.plot(default_noise.x, default_noise.y, 'b.')
            plt.subplot(222)
            plt.plot(shifted_noise.x, shifted_noise.y, 'b.')
            plt.subplot(223)
            plt.plot(impulsed_noise.x, impulsed_noise.y, 'b.')

            plt.show()

        case 5:
            print("Итерационное повышение f0")
            for i in range(12):
                harm = Model.harm(N=30, A0=100, f0=(33+(50*i)))
                plt.subplot(3, 4, i + 1)
                plt.plot(harm.x, harm.y)
            plt.show()

            print("Нажмите Enter для следующего графика...")
            input()

            polyharm = Model.poly_harm()
            plt.plot(polyharm.x, polyharm.y)
            plt.show()

        case 0:
            exit(0)

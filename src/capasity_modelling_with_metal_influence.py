import math
import numpy as np
import matplotlib.pyplot as plt

Q = 1.6 * math.pow(10, -19)
E = 10 * 8.85 * math.pow(10, -12)
ND = 7.7 * math.pow(10, 22)
K = 1.38 * math.pow(10, -23)
T = 300
VB = 0.09


def capacity(temperature_barrier_height, voltage):
    return 2 * (temperature_barrier_height - voltage - K * T / Q - VB) / (Q * E * ND)


def show_capacity():
    v = np.linspace(-30, 0, 1000)
    fig = plt.figure(figsize=(7, 4))
    ax = fig.add_subplot()

    ax.plot(v, capacity(1.28, v), label='TBH = 1.28 V, Pd ', color='b')
    ax.plot(v, capacity(1.54, v), label='TBH = 1.54 V, Ni ', color='k')
    ax.plot(v, capacity(1.59, v), label='TBH = 1.59 V, Pt ', color='r')
    ax.plot(v, capacity(1.97, v), label='TBH = 1.97 V, Au ', color='g')

    plt.xlim(-5, 3)
    plt.ylim(0, 1.2 * math.pow(10, 7))
    plt.xlabel("Напряжение, В")
    plt.ylabel("Емкость обедненного слоя, F^-2 см^4")
    plt.legend()
    plt.show()


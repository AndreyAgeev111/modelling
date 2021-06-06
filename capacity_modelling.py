import math
import numpy as np
import matplotlib.pyplot as plt

Q = 1.6 * math.pow(10, -19)
E = 10 * 8.85 * math.pow(10, -12)
ND = 7.7 * math.pow(10, 22)
VB = 0.71
K = 1.38 * math.pow(10, -23)


def capacity(temperature, voltage):
    return 2 * (VB - voltage - K * temperature / Q) / (Q * E * ND)


def showCapacity():
    v = np.linspace(-30, 0, 1000)
    plt.plot(v, capacity(298, v))

    plt.xlim(-30, 0.71)
    plt.xlabel("Напряжение, В")
    plt.ylabel("Емкость обдненного слоя, F^-2 см^4")

    plt.show()


def testCapacity():
    print('Значения обратного квадрата емкости в точках  V = -30 В и V = 0.71 В:',
          ' '.join([str(capacity(298, -30)), str(capacity(298, 0.71))]))

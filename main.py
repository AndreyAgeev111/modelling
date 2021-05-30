import math
import numpy as np
import matplotlib.pyplot as plt

A = 33.1
Q = 1.6 * math.pow(10, -19)
POTENTIAL = 0.86
K = 1.38 * math.pow(10, -23)
N = 1.03
R = 159.2


def saturationCurrentDensity(temperature):
    return A * math.pow(temperature, 2) * np.exp(
        -Q * POTENTIAL / temperature / K)


def currentDensity(temperature, voltage):
    return saturationCurrentDensity(temperature) * \
           (np.exp(Q * voltage / N / K / temperature) - 1)


def upgradeCurrentDensity(temperature, voltage):
    return saturationCurrentDensity(temperature) * \
           (np.exp(Q *
                   (voltage - currentDensity(temperature, voltage) * R) / N / K / temperature) - 1)


def showUpgradeCurrentDensity():
    v = np.linspace(0, 0.6, 100)
    plt.plot(v, upgradeCurrentDensity(298, v))
    plt.ylim(0, 8 * math.pow(10, -5))

    plt.show()


def testCurrentDensity():
    testV = np.linspace(0, 0.6, 7)
    for vol in testV:
        print('Ток прямого смещения и ток прямого смещения с поправкой:',
              " ".join([str(currentDensity(298, vol)), str(upgradeCurrentDensity(298, vol))]))
    plt.plot(testV, currentDensity(298, testV))
    plt.plot(testV, upgradeCurrentDensity(298, testV))
    plt.ylim(0, 8 * math.pow(10, -5))

    plt.show()


if __name__ == "__main__":
    showUpgradeCurrentDensity()
    testCurrentDensity()
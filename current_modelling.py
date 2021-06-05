import math
import numpy as np
import matplotlib.pyplot as plt
import array

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


def upgradeSomeCurrent(temperature, voltage):
    startCurrent = 0
    currentValues = array.array('f', [])

    for v in range(len(voltage)):
        current = saturationCurrentDensity(temperature) * (np.exp(
            Q * (voltage[v] - startCurrent * R) / N / K / temperature) - 1)
        currentValues.append(current)
        startCurrent = current

    return currentValues


def sortedUpgradeCurrentDensity(temperature, voltage):
    return sorted(upgradeSomeCurrent(temperature, voltage))


def showUpgradeCurrentDensity():
    v = np.linspace(0, 0.6, 100)
    plt.plot(v, sortedUpgradeCurrentDensity(298, v))
    plt.ylim(0, 8 * math.pow(10, -5))
    plt.show()


def testCurrentDensity():
    testV = np.linspace(0, 0.6, 7)
    plt.plot(testV, currentDensity(298, testV))
    plt.plot(testV, upgradeSomeCurrent(298, testV))
    plt.ylim(0, 8 * math.pow(10, -5))

    plt.show()

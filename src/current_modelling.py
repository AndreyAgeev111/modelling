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
    currentValues = upgradeSomeCurrent(temperature, voltage)
    lengthOfArray = len(currentValues)
    for current in range(lengthOfArray - 1):
        if currentValues[current] > currentValues[(current + 1)]:
            continue
        else:
            currentValues[current] = (currentValues[current - 1] + currentValues[current + 1]) / 2

    if currentValues[lengthOfArray - 1] < currentValues[lengthOfArray - 2]:
        currentValues[lengthOfArray - 1] = 2 * currentValues[lengthOfArray - 2] - \
                                           currentValues[lengthOfArray - 3]
    currentValues[0] = 0
    return currentValues


def showUpgradeCurrentDensity():
    v = np.linspace(0, 0.6, 10000)

    plt.plot(v, sortedUpgradeCurrentDensity(298, v), label='T = 298 K')
    plt.plot(v, sortedUpgradeCurrentDensity(323, v), label='T = 323 K')
    plt.plot(v, sortedUpgradeCurrentDensity(373, v), label='T = 373 K')
    plt.plot(v, sortedUpgradeCurrentDensity(423, v), label='T = 423 K')

    plt.ylim(0, 8 * math.pow(10, 0))
    plt.xlabel("Напряжение, В")
    plt.ylabel("Плотность тока J, А / см^2")
    plt.legend()
    plt.show()


def someTestValues(temperature):
    v = np.linspace(0, 0.6, 6000)
    currentValues = sortedUpgradeCurrentDensity(temperature, v)

    # точки V = 0, 0.1, 0.2 ... 0.6
    for numb in range(6):
        print("Значение плотности тока для температуры " + str(temperature) + "К: " + str(currentValues[numb * 1000]))
    print("Значение плотности тока для температуры " + str(temperature) + "К: " + str(currentValues[5999]))

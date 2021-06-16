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
S = 4 * math.pi * math.pow(10, -4)


def saturation_current_density(temperature):
    return A * math.pow(temperature, 2) * np.exp(
        -Q * POTENTIAL / temperature / K)


def get_oscillation_index(temperature, voltage):
    currentValues = current_density(temperature, voltage)
    for current in range(len(currentValues) - 1):
        if currentValues[current] > currentValues[current + 1]:
            return current


def current_density(temperature, voltage):
    startCurrent = 0
    currentValues = array.array('f', [])

    for v in range(len(voltage)):
        current = saturation_current_density(temperature) * (np.exp(
            Q * (voltage[v] - startCurrent * R * S) / N / K / temperature) - 1)
        currentValues.append(current)
        startCurrent = current

    return currentValues


def sort_current_density(temperature, voltage):
    oscillationIndex = get_oscillation_index(temperature, voltage)
    currentValues = current_density(temperature, voltage)
    delta = currentValues[oscillationIndex] - currentValues[oscillationIndex - 1]

    for current in range(oscillationIndex, len(currentValues)):
        currentValues[current] = currentValues[current - 1] + delta

    return currentValues


def show_upgrade_current_density():
    v = np.linspace(0, 0.6, 10000)

    plt.plot(v, sort_current_density(298, v), label='T = 298 K')
    plt.plot(v, sort_current_density(323, v), label='T = 323 K')
    plt.plot(v, sort_current_density(373, v), label='T = 373 K')
    plt.plot(v, sort_current_density(423, v), label='T = 423 K')

    plt.ylim(0, 3 * math.pow(10, 0))
    plt.xlabel("Напряжение, В")
    plt.ylabel("Плотность тока J, А / см^2")
    plt.legend()
    plt.show()


def some_test_values(temperature):
    v = np.linspace(0, 0.6, 6000)
    currentValues = sort_current_density(temperature, v)
    # точки V = 0, 0.1, 0.2 ... 0.6
    for numb in range(6):
        print("Значение плотности тока для температуры " + str(temperature) + "К: " + str(currentValues[numb * 1000]))
    print("Значение плотности тока для температуры " + str(temperature) + "К: " + str(currentValues[5999]))

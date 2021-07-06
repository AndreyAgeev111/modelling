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
    current_values = current_density(temperature, voltage)
    for current in range(len(current_values) - 1):
        if current_values[current] > current_values[current + 1]:
            return current


def current_density(temperature, voltage):
    start_current = 0
    current_values = array.array('f', [])

    for v in range(len(voltage)):
        current = saturation_current_density(temperature) * (np.exp(
            Q * (voltage[v] - start_current * R * S) / N / K / temperature) - 1)
        current_values.append(current)
        start_current = current

    return current_values


def sort_current_density(temperature, voltage):
    oscillation_index = get_oscillation_index(temperature, voltage)
    current_values = current_density(temperature, voltage)
    delta = current_values[oscillation_index] - current_values[oscillation_index - 1]

    for current in range(oscillation_index, len(current_values)):
        current_values[current] = current_values[current - 1] + delta

    return current_values


def show_upgrade_current_density():
    v = np.linspace(0, 0.6, 10000)

    fig = plt.figure(figsize=(7, 4))
    ax = fig.add_subplot()
    ax.plot(v, sort_current_density(298, v), label='T = 298 K')
    ax.plot(v, sort_current_density(323, v), label='T = 323 K')
    ax.plot(v, sort_current_density(373, v), label='T = 373 K')
    ax.plot(v, sort_current_density(423, v), label='T = 423 K')

    ax.set_yscale('log')
    plt.xlabel("Напряжение, В")
    plt.ylabel("Плотность тока J, А / см^2")
    plt.legend()
    plt.show()


def some_test_values(temperature):
    v = np.linspace(0, 0.6, 6000)
    current_values = sort_current_density(temperature, v)
    # точки V = 0, 0.1, 0.2 ... 0.6
    for numb in range(6):
        print("Значение плотности тока для температуры " + str(temperature) + "К: " + str(current_values[numb * 1000]))
    print("Значение плотности тока для температуры " + str(temperature) + "К: " + str(current_values[5999]))

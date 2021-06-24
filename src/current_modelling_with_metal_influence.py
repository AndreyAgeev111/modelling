import math
import numpy as np
import matplotlib.pyplot as plt
import array

A = 33.1
Q = 1.6 * math.pow(10, -19)
K = 1.38 * math.pow(10, -23)
N = 1.03
R = 159.2
S = 4 * math.pi * math.pow(10, -4)
T = 300


def saturation_current_density(temperature_barrier_height):
    return A * S * math.pow(T, 2) * np.exp(
        -Q * temperature_barrier_height / T / K)


def get_oscillation_index(temperature_barrier_height, voltage):
    currentValues = current_density(temperature_barrier_height, voltage)
    for current in range(len(currentValues) - 1):
        if currentValues[current] > currentValues[current + 1]:
            print(current)
            return current


def current_density(temperature_barrier_height, voltage):
    startCurrent = 0
    currentValues = array.array('f', [])

    for v in range(len(voltage)):
        current = saturation_current_density(temperature_barrier_height) * (np.exp(
            Q * (voltage[v] - startCurrent * R * S) / N / K / T) - 1)
        currentValues.append(current)
        startCurrent = current

    return currentValues


def sort_current_density(temperature_barrier_height, voltage):
    oscillationIndex = get_oscillation_index(temperature_barrier_height, voltage)
    currentValues = current_density(temperature_barrier_height, voltage)
    delta = currentValues[oscillationIndex] - currentValues[oscillationIndex - 1]

    for current in range(oscillationIndex, len(currentValues)):
        currentValues[current] = currentValues[current - 1] + delta

    return currentValues


def show_upgrade_current_density():
    v = np.linspace(-3, 1.5, 10000)

    fig = plt.figure(figsize=(7, 4))
    ax = fig.add_subplot()
    ax.plot(v, sort_current_density(1.29, v), label='TBH = 1.29 V')
    ax.plot(v, sort_current_density(1.5, v), label='TBH = 1.5 V')
    ax.plot(v, sort_current_density(1.53, v), label='TBH = 1.53 V')
    ax.plot(v, sort_current_density(1.62, v), label='TBH = 1.62 V')

    ax.set_yscale('log')
    plt.xlabel("Напряжение, В")
    plt.ylabel("Плотность тока J, А / см^2")
    plt.legend()
    plt.show()

import math
import numpy as np
import matplotlib.pyplot as plt
import array

A = 41
Q = 1.6 * math.pow(10, -19)
K = 1.38 * math.pow(10, -23)
R = 159.2
S = 4 * math.pi * math.pow(10, -4)
T = 300


def saturation_current_density(temperature_barrier_height):
    return A * math.pow(T, 2) * np.exp(
        -Q * temperature_barrier_height / T / K)


def get_oscillation_index(temperature_barrier_height, n, voltage):
    current_values = current_density(temperature_barrier_height, n, voltage)
    for current in range(len(current_values) - 1):
        if current_values[current] > current_values[current + 1]:
            return current


def current_density(temperature_barrier_height, n, voltage):
    start_current = 0
    current_values = array.array('f', [])

    for v in range(len(voltage)):
        current = saturation_current_density(temperature_barrier_height) * (np.exp(
            Q * (voltage[v] - start_current * R * S) / n / K / T) - 1)
        current_values.append(current)
        start_current = current

    return current_values


def sort_current_density(temperature_barrier_height, n, voltage):
    oscillation_index = get_oscillation_index(temperature_barrier_height, n, voltage)
    current_values = current_density(temperature_barrier_height, n, voltage)
    delta = current_values[oscillation_index] - current_values[oscillation_index - 1]

    for current in range(oscillation_index, len(current_values)):
        current_values[current] = current_values[current - 1] + delta
    return current_values


def show_upgrade_current_density():
    v = np.linspace(-3, 2, 10000)

    fig = plt.figure(figsize=(7, 4))
    ax = fig.add_subplot()
    ax.plot(v, sort_current_density(1.27, 1.05, v), label='TBH = 1.27 V, n = 1.05, Pd ', color='b')
    ax.plot(v, sort_current_density(1.54, 1.04, v), label='TBH = 1.54 V, n = 1.04, Ni', color='k')
    ax.plot(v, sort_current_density(1.58, 1.03, v), label='TBH = 1.58 V, n = 1.03, Pt', color='r')
    ax.plot(v, sort_current_density(1.71, 1.09, v), label='TBH = 1.71 V, n = 1.09, Au', color='g')

    ax.set_yscale('log')
    ax.set_ylim([math.pow(10, -8), math.pow(10, 0)])
    plt.xlabel("Напряжение, В")
    plt.ylabel("Плотность тока J, А / см^2")
    plt.legend()
    plt.show()

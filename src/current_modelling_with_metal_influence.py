import math
import numpy as np
import matplotlib.pyplot as plt
import array

A = 41
Q = 1.6 * math.pow(10, -19)
K = 1.38 * math.pow(10, -23)
R = 159.2
S = 4 * math.pi * math.pow(10, -4)


def saturation_current_density(temperature_barrier_height, temperature):
    return A * math.pow(temperature, 2) * np.exp(
        -Q * temperature_barrier_height / temperature / K)


def get_oscillation_index(temperature_barrier_height, n, voltage, temperature):
    current_values = current_density(temperature_barrier_height, n, voltage, temperature)
    for current in range(len(current_values) - 1):
        if current_values[current] > current_values[current + 1]:
            return current


def current_density(temperature_barrier_height, n, voltage, temperature):
    start_current = 0
    current_values = array.array('f', [])

    for v in range(len(voltage)):
        current = saturation_current_density(temperature_barrier_height, temperature) * (np.exp(
            Q * (voltage[v] - start_current * R * S) / n / K / temperature) - 1)
        current_values.append(current)
        start_current = current

    return current_values


def sort_current_density(temperature_barrier_height, n, voltage, temperature):
    oscillation_index = get_oscillation_index(temperature_barrier_height, n, voltage, temperature)
    current_values = current_density(temperature_barrier_height, n, voltage, temperature)
    delta = current_values[oscillation_index] - current_values[oscillation_index - 1]

    for current in range(oscillation_index, len(current_values)):
        current_values[current] = current_values[current - 1] + delta
    return current_values


def show_upgrade_current_density():
    v = np.linspace(0, 3, 10000)
    print(v[463])
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot()
    ax.plot(v, sort_current_density(1, 1.05, v, 300), label='Mo', ls=':', lw='2')
    ax.plot(v, sort_current_density(1.27, 1.09, v, 300), label='Au', ls='-.', lw='2')
    ax.plot(v, sort_current_density(1.45, 1.04, v, 300), label='Pt', ls='--', lw='2')
    ax.plot(v, sort_current_density(1.69, 1.04, v, 300), label='Ag', ls='solid', lw='2')

    ax.set_yscale('log')
    ax.grid()
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(13)
        label.set_fontweight('bold')
    # ax.set_title('Al, TBH = 1.51 V, n = 1.02')
    # ax.set_xlim([0.9, 1.2])
    # ax.set_ylim([math.pow(10, -1), math.pow(10, 1)])
    ax.set_ylim([math.pow(10, -8), math.pow(10, 2)])
    ax.set_xlim([0, 3])
    plt.xlabel("Напряжение, В", fontsize=15, fontweight='heavy', name='Arial')
    plt.ylabel("Плотность тока J, А / см^2", fontsize=15, fontweight='heavy', name='Arial')
    plt.legend(loc='lower right', title='T = 300 K', fontsize=15, title_fontsize=14)
    plt.show()

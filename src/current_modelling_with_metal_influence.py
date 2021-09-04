import math
import numpy as np
import matplotlib.pyplot as plt
import array
import csv

A = 33.63
Q = 1.6 * math.pow(10, -19)
K = 1.38 * math.pow(10, -23)
R = 159.2
S = 6.25 * math.pi * math.pow(10, -4)


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


def csv_dict_reader(file_obj, column):
    reader = csv.DictReader(file_obj, delimiter=';')
    vol = []
    for line in reader:
        num = float(line[column])
        vol.append(num)
    return vol


def show_upgrade_current_density():
    v = np.linspace(0, 3, 1000000)
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot()

    with open("../csv/Ti.csv") as f_obj:
        vol = csv_dict_reader(f_obj, "V")
    with open("../csv/Ti.csv") as f_obj:
        current = csv_dict_reader(f_obj, "I")

    ax.plot(v, sort_current_density(0.83, 1.15, v, 300), label='T = 300 K')
    ax.plot(vol, current, label='Данные из статьи')

    ax.set_yscale('log')
    ax.grid()
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(11)
        label.set_fontweight('bold')
    ax.set_title('Ti, TBH = 0.83 V, n = 1.15', fontsize=14, fontweight='heavy', name='Arial')
    # ax.set_ylim([0, math.pow(10, 2)])
    # ax.set_xlim([0, 3])
    plt.xlabel("Напряжение, В", fontsize=14, fontweight='heavy', name='Arial')
    plt.ylabel("Плотность тока J, А / см^2", fontsize=14, fontweight='heavy', name='Arial')
    plt.legend(loc='lower right', fontsize=14, title_fontsize=13)
    plt.show()

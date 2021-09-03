import math
import numpy as np
import matplotlib.pyplot as plt
import array
import csv

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


def csv_dict_reader_voltage(file_obj):
    reader = csv.DictReader(file_obj, delimiter=';')
    vol = []
    for line in reader:
        num = float(line["V"])
        vol.append(num)
    return vol


def csv_dict_reader_current(file_obj):
    reader = csv.DictReader(file_obj, delimiter=';')
    current = []
    for line in reader:
        num = float(line["I"])
        current.append(num)
    return current


def show_upgrade_current_density():
    v = np.linspace(0, 3, 10000)
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot()

    with open("../csv/Ru.csv") as f_obj:
        vol = csv_dict_reader_voltage(f_obj)
    with open("../csv/Ru.csv") as f_obj:
        current = csv_dict_reader_current(f_obj)

    ax.plot(v, sort_current_density(1.27, 1.02, v, 300), label='T = 300 K')
    ax.plot(v, sort_current_density(1.27, 1.02, v, 323), label='T = 323 K')
    ax.plot(v, sort_current_density(1.27, 1.02, v, 343), label='T = 343 K')
    ax.plot(v, sort_current_density(1.27, 1.02, v, 363), label='T = 363 K')
    ax.plot(v, sort_current_density(1.27, 1.02, v, 383), label='T = 383 K')
    ax.plot(v, sort_current_density(1.27, 1.02, v, 403), label='T = 403 K')
    ax.plot(v, sort_current_density(1.27, 1.02, v, 423), label='T = 423 K')
    ax.plot(vol, current, label='Данные из статьи', linewidth='5')

    ax.set_yscale('log')
    ax.grid()
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(11)
        label.set_fontweight('bold')
    ax.set_title('Ru, TBH = 1.27 V, n = 1.02', fontsize=14, fontweight='heavy', name='Arial')
    # ax.set_ylim([0, math.pow(10, 2)])
    # ax.set_xlim([0, 3])
    plt.xlabel("Напряжение, В", fontsize=14, fontweight='heavy', name='Arial')
    plt.ylabel("Плотность тока J, А / см^2", fontsize=14, fontweight='heavy', name='Arial')
    plt.legend(loc='lower right', fontsize=14, title_fontsize=13)
    plt.show()

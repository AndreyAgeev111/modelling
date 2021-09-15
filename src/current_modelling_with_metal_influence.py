import math
import numpy as np
import matplotlib.pyplot as plt
import array
import csv

A = 33.63
Q = 1.6 * math.pow(10, -19)
K = 1.38 * math.pow(10, -23)
S = 6.25 * math.pi * math.pow(10, -8)
L = math.pow(10, -4)
RELATIVE_RESISTANCE = 0.7427


def get_resistance(relative_resistance):
    return relative_resistance * L / S


def saturation_current_density(temperature_barrier_height, temperature):
    return A * math.pow(temperature, 2) * np.exp(
        -Q * temperature_barrier_height / temperature / K)


def get_oscillation_index(temperature_barrier_height, n, voltage, temperature, relative_resistance):
    current_values = current_density(temperature_barrier_height, n, voltage, temperature, relative_resistance)
    for current in range(len(current_values) - 1):
        if current_values[current] > current_values[current + 1]:
            return current


def current_density(temperature_barrier_height, n, voltage, temperature, relative_resistance):
    start_current = 0
    current_values = array.array('f', [])

    for v in range(len(voltage)):
        current = saturation_current_density(temperature_barrier_height, temperature) * (np.exp(
            Q * (voltage[v] - start_current * get_resistance(relative_resistance) * S * math.pow(10, 4)) / n / K /
            temperature) - 1)
        current_values.append(current)
        start_current = current

    return current_values


def sort_current_density(temperature_barrier_height, n, voltage, temperature, relative_resistance):
    oscillation_index = get_oscillation_index(temperature_barrier_height, n, voltage, temperature, relative_resistance)
    current_values = current_density(temperature_barrier_height, n, voltage, temperature, relative_resistance)
    delta = current_values[oscillation_index] - current_values[oscillation_index - 1]

    for current in range(oscillation_index, len(current_values)):
        current_values[current] = current_values[current - 1] + delta / 2
    return current_values


def csv_dict_reader(file_obj, column):
    reader = csv.DictReader(file_obj, delimiter=';')
    vol = []
    for line in reader:
        num = float(line[column])
        vol.append(num)
    return vol


# Запись данных для последующего анализа для аппроксимации
def csv_dict_writer(file_obj, temperature_barrier_height, relative_resistance):
    v = np.linspace(0, 3, 1000000)
    current_values = sort_current_density(temperature_barrier_height, 1.02, v, 300, relative_resistance)

    names = ["V", "I"]
    file_writer = csv.DictWriter(file_obj, delimiter=",",
                                 lineterminator="\r", fieldnames=names)
    file_writer.writeheader()
    for i in range(len(v)):
        if i % 500 == 0:
            file_writer.writerow({"V": str(v[i]), "I": str(current_values[i])})


def calculate_STD(file_obj, temperature_barrier_height, n):
    theory_data_voltage = np.linspace(0, 3, 500000)
    theory_data_current = sort_current_density(temperature_barrier_height, n, theory_data_voltage, 300, 0.7427)

    with open(file_obj) as f_obj:
        exp_data_voltage = csv_dict_reader(f_obj, "V")
    with open(file_obj) as f_obj:
        exp_data_current = csv_dict_reader(f_obj, "I")

    relative_square_difference = []
    for i in range(len(exp_data_voltage)):
        relative_square_difference.append(
            ((exp_data_current[i] - np.interp(exp_data_voltage[i], theory_data_voltage, theory_data_current)) ** 2) /
            exp_data_current[i] ** 2)

    STD = (sum(relative_square_difference) / len(relative_square_difference)) ** 0.5
    print("STD = " + str(STD))

    plt.plot(exp_data_voltage[2:], relative_square_difference[2:])
    plt.ylabel('Square difference')
    plt.xlabel('Applied voltage (V)')
    plt.title('Ru')
    plt.show()

    return 0


def get_result_of_search(n, start_temperature_height, end_temperature_height, length_of_interval, relative_resistance,
                         accuracy_index, file_obj):
    v = np.linspace(0, 3, 500000)
    end_current_values = []
    barrier_heights = []
    barrier_height = start_temperature_height
    for i in range(length_of_interval):
        barrier_heights.append(barrier_height)
        barrier_height += (end_temperature_height - start_temperature_height) / (length_of_interval - 1)
        current_values = sort_current_density(barrier_heights[i], n, v, 300, relative_resistance)
        end_current_values.append(current_values[len(v) - 1])
    names = ["TBH", "I"]
    file_writer = csv.DictWriter(file_obj, delimiter=",",
                                 lineterminator="\r", fieldnames=names)
    file_writer.writeheader()
    for i in range(len(end_current_values)):
        file_writer.writerow({"TBH": str(barrier_heights[i]), "I": str(end_current_values[i])})

    for i in range(len(end_current_values)):
        if end_current_values[i] < accuracy_index:
            print(end_current_values[i])
            print(barrier_heights[i])
            print(end_current_values)
            break


def show_upgrade_current_density():
    v = np.linspace(0, 3, 1000000)
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot()

    with open("../csv/Ag.csv") as f_obj:
        vol = csv_dict_reader(f_obj, "V")
    with open("../csv/Ag.csv") as f_obj:
        current = csv_dict_reader(f_obj, "I")
    with open("../csv/Ag_model.csv", "w") as f_obj:
        csv_dict_writer(f_obj, 1.72, 0.16)
    with open("../csv/V_alpha_model.csv", "w") as f_obj:
        csv_dict_writer(f_obj, 0.68, 0.15)

    ax.plot(v, sort_current_density(0.87, 1.1, v, 300, 0.15), label='Nb')
    ax.plot(v, sort_current_density(0.8, 1.1, v, 300, 0.15), label='Ta')
    ax.plot(v, sort_current_density(0.72, 1.1, v, 300, 0.193), label='Re')
    ax.plot(v, sort_current_density(0.7, 1.1, v, 300, 0.405), label='Sb')
    ax.plot(v, sort_current_density(0.5, 1.1, v, 300, 0.27), label='Cr')
    ax.plot(v, sort_current_density(1.72, 1.02, v, 300, 0.15), label='V')
    ax.plot(vol, current, label='Данные из статьи')

    ax.set_yscale('log')
    ax.grid()
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(11)
        label.set_fontweight('bold')
    # ax.set_title('Pd, TBH = 1.22 V, n = 1.05', fontsize=14, fontweight='heavy', name='Arial')
    plt.xlabel("Напряжение, В", fontsize=14, fontweight='heavy', name='Arial')
    plt.ylabel("Плотность тока J, А / см^2", fontsize=14, fontweight='heavy', name='Arial')
    plt.legend(loc='lower right', fontsize=14, title="T = 300 K", title_fontsize=13)
    plt.show()

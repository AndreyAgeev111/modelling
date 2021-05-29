import math
import numpy as np
import matplotlib.pyplot as plt


def saturationCurrentDensity(temperature):
    return 33.1 * math.pow(temperature, 2) * np.exp(
        -1.6 * math.pow(10, 4) * 0.86 / temperature / 1.38)


def currentDensity(temperature, voltage):
    return saturationCurrentDensity(temperature) * \
           (np.exp(1.6 * math.pow(10, 4) * voltage / 1.03 / 1.38 / temperature) - 1)


def upgradeCurrentDensity(temperature, voltage):
    return saturationCurrentDensity(temperature) * \
           (np.exp(1.6 * math.pow(10, 4) *
                   (voltage - currentDensity(temperature, voltage) * 159.2) / 1.03 / 1.38 / temperature) - 1)


testV = np.linspace(0, 0.6, 7)
for vol in testV:
    print('Ток прямого смещения и ток прямого смещения с поправкой:',
          " ".join([str(currentDensity(298, vol)), str(upgradeCurrentDensity(298, vol))]))

v = np.linspace(0, 0.6, 100)
plt.plot(v, currentDensity(298, v))
plt.plot(v, upgradeCurrentDensity(298, v))


# plt.plot(v, upgradeCurrentDensity(323, v))
# plt.plot(v, upgradeCurrentDensity(373, v))
# plt.plot(v, upgradeCurrentDensity(423, v))

plt.show()

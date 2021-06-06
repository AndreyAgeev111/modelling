import current_modelling
import capacity_modelling

if __name__ == "__main__":
    # ВАХ диода Шоттки
    current_modelling.showUpgradeCurrentDensity()
    current_modelling.someTestValues(298)

    # Зависимость квадрата 1/С к напряжению диода Шоттки
    capacity_modelling.showCapacity()
    capacity_modelling.testCapacity()

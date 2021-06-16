from src import capacity_modelling, current_modelling

if __name__ == "__main__":
    # ВАХ диода Шоттки
    current_modelling.show_upgrade_current_density()
    current_modelling.some_test_values(298)

    # Зависимость квадрата 1/С к напряжению диода Шоттки
    capacity_modelling.showCapacity()
    capacity_modelling.testCapacity()

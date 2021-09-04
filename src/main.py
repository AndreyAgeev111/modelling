from src import capacity_modelling, current_modelling, current_modelling_with_metal_influence, \
    capasity_modelling_with_metal_influence

if __name__ == "__main__":
    # ВАХ диода Шоттки
    # current_modelling.show_upgrade_current_density()
    # current_modelling.some_test_values(298)

    # Зависимость квадрата 1/С к напряжению диода Шоттки
    # capacity_modelling.show_capacity()
    # capacity_modelling.test_capacity()

    # Зависимость плотности тока от материала контакта
    current_modelling_with_metal_influence.show_upgrade_current_density()

    # Зависимость квадрата 1/С к напряжению диода Шоттки от материала контакта
    # capasity_modelling_with_metal_influence.show_capacity()

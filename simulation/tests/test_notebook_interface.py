"""
Tests running complete trees via the notebook interface
"""

import simulation.notebook_interface as notebook_interface
import simulation.behavior_tree as behavior_tree
behavior_tree.load_settings_from_file('simulation/tests/BT_TEST_SETTINGS.yaml')

def test_idle():
    """
    Basic tests with just idle actions
    """
    environment = notebook_interface.Environment()

    assert environment.get_fitness(['idle']) == -0.1

    assert environment.get_fitness(['s(', 'idle', 'idle', ')']) == -0.3

    assert environment.get_fitness(['f(', 'idle', 'idle', ')']) == -0.3

def test_charge_and_light():
    """
    Simple tree with just charging and picking light objects
    """
    environment = notebook_interface.Environment(verbose=True)

    individual = ['s(', 'f(', 's(', 'battery level < 90', 'at station CHARGE1', 'charge', ')', \
                              'battery level > 50', 's(', 'move to CHARGE1', 'charge', ')', ')', \
                        'f(', 'carried weight > 0', 's(', 'move to CONVEYOR_LIGHT', 'f(', 'pick', 'idle', ')', ')', ')', \
                        'move to DELIVERY', 'place', ')']

    notebook_interface.plot_individual('', 'test', individual)

    assert environment.get_fitness(individual) > 0.0

def test_charge_and_heavy():
    """
    Simple tree with just charging and picking heavy objects
    """
    environment = notebook_interface.Environment(verbose=True)

    individual = ['s(', 'f(', 's(', 'battery level < 90', 'at station CHARGE1', 'charge', ')', \
                              'battery level > 50', 's(', 'move to CHARGE1', 'charge', ')', ')', \
                        'f(', 'carried weight > 0', 's(', 'move to CONVEYOR_HEAVY', 'f(', 'pick', 'idle', ')', ')', ')', \
                        'move to DELIVERY', 'place', ')']

    notebook_interface.plot_individual('', 'test', individual)

    assert environment.get_fitness(individual) > 0.0

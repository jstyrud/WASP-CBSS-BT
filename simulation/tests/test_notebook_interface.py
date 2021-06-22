"""
Tests running complete trees via the notebook interface
"""

import simulation.notebook_interface as notebook_interface
import simulation.behavior_tree as behavior_tree
import simulation.fitness_function as fitness_function
behavior_tree.load_settings_from_file('simulation/tests/BT_TEST_SETTINGS.yaml')

def test_idle():
    """
    Basic tests with just idle actions
    """
    fitness_coeff = fitness_function.Coefficients()
    fitness_coeff.blocked_heavy = 0.0
    fitness_coeff.blocked_light = 0.0
    environment = notebook_interface.Environment(fitness_coeff=fitness_coeff)

    assert environment.get_fitness(['idle']) == fitness_coeff.length

    assert environment.get_fitness(['s(', 'idle', 'idle', ')']) == round(fitness_coeff.length * 3, 10)

    assert environment.get_fitness(['f(', 'idle', 'idle', ')']) == round(fitness_coeff.length * 3, 10)

def test_charge_and_light():
    """
    Simple tree with just charging and picking light objects
    """
    environment = notebook_interface.Environment(verbose=True)

    individual = ['s(', 'f(', 's(', 'battery level < 90', 'at station CHARGE1', 'charge', ')', \
                              'battery level > 50', 's(', 'move to CHARGE1', 'charge', ')', ')', \
                        'f(', 'carried weight > 0', \
                              's(', 'move to CONVEYOR_LIGHT', 'f(', 'pick', 'idle', ')', ')', ')', \
                        'move to DELIVERY', 'place', ')']

    notebook_interface.plot_individual('', 'test', individual)

    assert environment.get_fitness(individual, show_world=False) > 0.0

def test_charge_and_heavy():
    """
    Simple tree with just charging and picking heavy objects
    """
    environment = notebook_interface.Environment(verbose=True)

    individual = ['s(', 'f(', 's(', 'battery level < 90', 'at station CHARGE1', 'charge', ')', \
                              'battery level > 50', 's(', 'move to CHARGE1', 'charge', ')', ')', \
                        'f(', 'carried weight > 0', \
                              's(', 'move to CONVEYOR_HEAVY', 'f(', 'pick', 'idle', ')', ')', ')', \
                        'move to DELIVERY', 'place', ')']

    notebook_interface.plot_individual('', 'test', individual)

    assert environment.get_fitness(individual, show_world=False) > 0.0

def test_minimal():
    """
    Testing a minimal useful tree
    """
    environment = notebook_interface.Environment(seed=0, verbose=True)

    individual = ['sm(', 'move to CONVEYOR_HEAVY', 'pick', 'move to DELIVERY', 'place', ')']

    notebook_interface.plot_individual('', 'test', individual)

    assert environment.get_fitness(individual, show_world=False) > 0.0

def test_step():
    """
    Test stepping instead of running
    """
    environment = notebook_interface.Environment(seed=0, verbose=True)

    individual = ['sm(', 'move to CONVEYOR_HEAVY', 'move to DELIVERY', 'place', ')']

    environment.get_fitness(individual, max_ticks=100, show_world=False)
    state = environment.world_interface.state

    environment = notebook_interface.Environment(seed=0, verbose=True)
    for _ in range(100):
        environment.step(individual)

    assert state == environment.world_interface.state

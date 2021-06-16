"""
A simple simulation environment for running behavior trees
"""

#Imports that define the environment
from simulation.py_trees_interface import PyTree
import simulation.behaviors as behaviors
import simulation.conveyor_kitting as sm
import simulation.fitness_function as fitness_function

class Environment():
    """ Class defining the environment in which the individual operates """
    def __init__(self, seed=0, verbose=False, fitness_coeff=None):
        self.seed = seed
        self.verbose = verbose
        self.fitness_coeff = fitness_coeff

    def get_fitness(self, individual, show_world=False, tick_period=0.5):
        """ Run the simulation and return the fitness """
        world_interface = sm.Simulation(seed=self.seed)
        pytree = PyTree(individual[:], behaviors=behaviors, world_interface=world_interface, verbose=self.verbose)

        # run the Behavior Tree
        ticks, _ = pytree.run_bt(show_world=show_world, tick_period=tick_period)

        return fitness_function.compute_fitness(world_interface, pytree, ticks, self.fitness_coeff)

def plot_individual(path, plot_name, individual):
    """ Saves a graphical representation of the individual """
    pytree = PyTree(individual[:], behaviors=behaviors)
    pytree.save_fig(path, name=plot_name)

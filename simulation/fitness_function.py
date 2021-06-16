"""
Task dependent fitness function
"""

from dataclasses import dataclass

@dataclass
class Coefficients:
    """
    Coefficients for tuning the fitness function
    """
    delivered_heavy: float = 2.0
    delivered_light: float = 1.0
    depth: float = 0.0
    length: float = -0.1
    ticks: float = 0.0
    failed: float = -50.0
    timeout: float = 0.0

def compute_fitness(world_interface, behavior_tree, ticks, coeff=None, verbose=False):
    # pylint: disable=too-many-arguments
    """ Retrieve values and compute fitness """

    if coeff is None:
        coeff = Coefficients()

    depth = behavior_tree.depth
    length = behavior_tree.length

    fitness = coeff.length * length + \
              coeff.depth * depth + \
              coeff.ticks * ticks
    if verbose:
        print("Fitness from length, depth, ticks:", fitness)

    fitness += coeff.delivered_heavy * world_interface.state.delivered_heavy
    fitness += coeff.delivered_light * world_interface.state.delivered_light
    if verbose:
        print("Fitness after deliveries:", fitness)

    if behavior_tree.failed:
        fitness += coeff.failed
        if verbose:
            print("Failed: ", fitness)
    if behavior_tree.timeout:
        fitness += coeff.timeout
        if verbose:
            print("Timed out: ", fitness)

    fitness = round(fitness, 10) #Just to ensure that binary approximation doesn't affect fitness ranking
    return fitness

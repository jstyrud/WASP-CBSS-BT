"""
Simulation of a robot performing kitting from two conveyors
"""
import random
from dataclasses import dataclass
from enum import IntEnum

MAX_BATTERY = 100
MAX_WEIGHT = 10
HEAVY_WEIGHT = 3
LIGHT_WEIGHT = 1

@dataclass
class RobotPos:
    """
    Robot position
    """
    x: float = 0
    y: float = 0

@dataclass
class WorldState:
    """
    The complete world state:
    """
    robot_pos: RobotPos = (0, 0)
    battery_level: int = MAX_BATTERY
    carried_weight: int = 0
    carried_light: int = 0
    carried_heavy: int = 0
    cnv_n_light: int = 0 #Number of light objects currently on conveyor
    cnv_n_heavy: int = 0 #Number of heavy objects currently on conveyor

class Stations(IntEnum):
    """ Indices for robot stations """
    CHARGE1 = 0
    CHARGE2 = 1
    CONVEYOR_HEAVY = 2
    CONVEYOR_LIGHT = 3
    DELIVERY = 4

def get_station_from_string(string):
    """ Returns station index from string """
    if 'CHARGE1' in string:
        return Stations.CHARGE1
    if 'CHARGE2' in string:
        return Stations.CHARGE2
    if 'CONVEYOR_HEAVY' in string:
        return Stations.CONVEYOR_HEAVY
    if 'CONVEYOR_LIGHT' in string:
        return Stations.CONVEYOR_LIGHT
    if 'DELIVERY' in string:
        return Stations.DELIVERY
    else:
        return -1

def get_pose(station):
    """
    Returns pose of given station
    """
    if station == Stations.CHARGE1:
        return (2, 7.5)
    if station == Stations.CHARGE2:
        return (23, 12)
    if station == Stations.CONVEYOR_HEAVY:
        return (12, 12)
    if station == Stations.CONVEYOR_LIGHT:
        return (12, 3)
    if station == Stations.DELIVERY:
        return (21, 7.5)
    print("ERROR, invalid station")
    return (0, 0)

class PathPlanner:
    """
    Super simple silly path planner
    """

    def move_towards(self, station, state):
        """
        Moves towards given station
        """
        if state.robot_pos != get_pose(station):
            state.robot_pos = get_pose(station)

class Simulation:
    """

    """
    def __init__(self, seed=0):
        self.state = WorldState()
        self.path_planner = PathPlanner()
        random.seed(seed)

    def step(self):
        """
        Step the simulation one timestep
        """

        #Randomly add objects on conveyor
        #Deplete battery
        self.state.battery_level -= 1

    def at_station(self, station):
        """ Checks if robot is currently at given station """
        return self.state.robot_pos == get_pose(station)

    def idle(self):
        """
        Robot does nothing
        """
        self.step()

    def charge(self):
        """
        Robot attemps to charge at station
        """
        if self.state.robot_pos == get_pose(Stations.CHARGE1) or \
           self.state.robot_pos == get_pose(Stations.CHARGE2):
            self.state.battery_level += 10
            self.step()
            self.state.battery_level = min(MAX_BATTERY, self.state.battery_level)

            return True
        return False

    def moveto(self, station):
        """
        Moves robot towards given position
        """
        if self.state.battery_level > 0:
            self.path_planner.move_towards(station, self.state)
            self.step()
            return True
        return False

    def pick(self):
        """
        Picks up an object if possible
        """
        if self.state.battery_level > 0:
            if self.state.robot_pos == get_pose(Stations.CONVEYOR_HEAVY) and \
                self.state.cnv_n_heavy > 0 and \
                self.state.carried_weight + HEAVY_WEIGHT <= MAX_WEIGHT:

                self.state.carried_weight += HEAVY_WEIGHT
                self.state.carried_heavy += 1
                self.state.cnv_n_heavy -= 1
                self.state.battery_level -= 1
                self.step()
                return True
            if self.state.robot_pos == get_pose(Stations.CONVEYOR_LIGHT) and \
                self.state.cnv_n_light > 0 and \
                self.state.carried_weight + LIGHT_WEIGHT <= MAX_WEIGHT:

                self.state.carried_weight += LIGHT_WEIGHT
                self.state.carried_light += 1
                self.state.cnv_n_light -= 1
                self.state.battery_level -= 1
                self.step()
                return True
        return False

    def place(self):
        """
        Places objects if possible
        """
        if self.state.battery_level > 0:
            if self.state.robot_pos == get_pose(Stations.DELIVERY):
                for _ in range(self.state.carried_light):
                    self.state.carried_light -= 1
                    self.state.carried_weight -= LIGHT_WEIGHT

                for _ in range(self.state.carried_heavy):
                    self.state.carried_heavy -= 1
                    self.state.carried_weight -= HEAVY_WEIGHT
                self.state.battery_level -= 1
                self.step()
                return True
        return False

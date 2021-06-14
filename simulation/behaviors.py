# pylint: disable=duplicate-code
"""
Implementing various py trees behaviors
For duplo brick handling in a state machine env
"""
import re
import py_trees as pt

import simulation.conveyor_kitting as sm

def get_node_from_string(string, world_interface, verbose=False):
    # pylint: disable=too-many-branches
    """
    Returns a py trees behavior or composite given the string
    """
    has_children = False

    if 'at station ' in string:
        node = AtStation(string, world_interface, string[11:])
    elif 'battery level >' in string:
        node = BatteryLevel(string, world_interface, re.findall(r'\d+', string))
    elif 'carried weight >' in string:
        node = CarriedWeight(string, world_interface, re.findall(r'\d+', string))
    elif 'carried light >' in string:
        node = CarriedLight(string, world_interface, re.findall(r'\d+', string))
    elif 'carried heavy >' in string:
        node = CarriedHeavy(string, world_interface, re.findall(r'\d+', string))
    elif 'conveyor light >' in string:
        node = ConveyorLight(string, world_interface, re.findall(r'\d+', string))
    elif 'conveyor heavy >' in string:
        node = ConveyorHeavy(string, world_interface, re.findall(r'\d+', string))

    elif 'idle' in string:
        node = Idle(string, verbose)
    elif 'charge' in string:
        node = Charge(string, world_interface, verbose)
    elif 'move to' in string:
        node = MoveTo(string, world_interface, string[7:], verbose)
    elif 'pick' in string:
        node = Pick(string, world_interface, verbose)
    elif 'place' in string:
        node = Place(string, world_interface, verbose=verbose)

    elif string == 'f(':
        node = pt.composites.Selector('Fallback')
        has_children = True
    elif string == 's(':
        node = pt.composites.Selector('Selector', memory=False)
        has_children = True
    elif string == 'p(':
        node = pt.composites.Parallel(
            name="Parallel",
            policy=pt.common.ParallelPolicy.SuccessOnAll(synchronise=False))
        has_children = True
    elif string == 'nonpytreesbehavior':
        return False
    else:
        raise Exception("Unexpected character", string)
    return node, has_children

class AtStation(pt.behaviour.Behaviour):
    """
    Check if robot is at given station
    """
    def __init__(self, name, world_interface, station):
        self.world_interface = world_interface
        self.station = sm.get_station_from_string(station)
        super(AtStation, self).__init__(name)

    def update(self):
        if self.world_interface.at_station(self.station):
            return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE

class BatteryLevel(pt.behaviour.Behaviour):
    """
    Checks battery level
    """
    def __init__(self, name, world_interface, value):
        self.world_interface = world_interface
        self.value = int(value[0])
        super(BatteryLevel, self).__init__(name)

    def update(self):
        if self.world_interface.state.battery_level > self.value:
            return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE

class CarriedWeight(pt.behaviour.Behaviour):
    """
    Check the currently carried weight
    """
    def __init__(self, name, world_interface, value):
        self.world_interface = world_interface
        self.value = int(value[0])
        super(CarriedWeight, self).__init__(name)

    def update(self):
        if self.world_interface.state.carried_weight > self.value:
            return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE

class CarriedLight(pt.behaviour.Behaviour):
    """
    Check the currently carried number of light objects
    """
    def __init__(self, name, world_interface, value):
        self.world_interface = world_interface
        self.value = int(value[0])
        super(CarriedLight, self).__init__(name)

    def update(self):
        if self.world_interface.state.carried_light > self.value:
            return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE

class CarriedHeavy(pt.behaviour.Behaviour):
    """
    Check the currently carried number of heavy objects
    """
    def __init__(self, name, world_interface, value):
        self.world_interface = world_interface
        self.value = int(value[0])
        super(CarriedHeavy, self).__init__(name)

    def update(self):
        if self.world_interface.state.carried_heavy > self.value:
            return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE

class ConveyorLight(pt.behaviour.Behaviour):
    """
    Check the current number of light objects on conveyor
    """
    def __init__(self, name, world_interface, value):
        self.world_interface = world_interface
        self.value = int(value[0])
        super(ConveyorLight, self).__init__(name)

    def update(self):
        if self.world_interface.state.cnv_n_light > self.value:
            return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE

class ConveyorHeavy(pt.behaviour.Behaviour):
    """
    Check the current number of heavy objects on conveyor
    """
    def __init__(self, name, world_interface, value):
        self.world_interface = world_interface
        self.value = int(value[0])
        super(ConveyorHeavy, self).__init__(name)

    def update(self):
        if self.world_interface.state.cnv_n_heavy > self.value:
            return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE

class SmBehavior(pt.behaviour.Behaviour):
    """
    Class template for state machine behaviors
    """
    def __init__(self, name, world_interface, verbose=False):
        self.world_interface = world_interface
        self.state = None
        self.verbose = verbose
        super(SmBehavior, self).__init__(name)

    def update(self):
        if self.verbose and self.state == pt.common.Status.RUNNING:
            print(self.name, ":", self.state)

    def success(self):
        """ Set state success """
        self.state = pt.common.Status.SUCCESS
        if self.verbose:
            print(self.name, ": SUCCESS")

    def failure(self):
        """ Set state failure """
        self.state = pt.common.Status.FAILURE
        if self.verbose:
            print(self.name, ": FAILURE")

class Idle(SmBehavior):
    """
    Do nothing
    """
    def __init__(self, name, verbose=False):
        super(Idle, self).__init__(name, world_interface=None, verbose=verbose)

    def initialise(self):
        self.state = None

    def update(self):
        super(Idle, self).update()
        if self.state is None:
            self.state = pt.common.Status.RUNNING

        return self.state

class Charge(SmBehavior):
    """
    Charge robot
    """
    def initialise(self):
        if self.world_interface.state.battery_level >= sm.MAX_BATTERY:
            self.success()
        else:
            self.state = None

    def update(self):
        super(Charge, self).update()
        if self.state is None:
            self.state = pt.common.Status.RUNNING
        if self.state is pt.common.Status.RUNNING:
            if self.world_interface.charge():
                if self.world_interface.state.battery_level >= sm.MAX_BATTERY:
                    self.success()
            else:
                self.failure()
        return self.state

class MoveTo(SmBehavior):
    """
    Move towards station
    """
    def __init__(self, name, world_interface, station, verbose=False):
        self.station = sm.get_station_from_string(station)
        super(MoveTo, self).__init__(name, world_interface, verbose)

    def initialise(self):
        if self.world_interface.at_station(self.station):
            self.success()
        else:
            self.state = None

    def update(self):
        super(MoveTo, self).update()
        if self.state is None:
            self.state = pt.common.Status.RUNNING
        if self.state is pt.common.Status.RUNNING:
            if self.world_interface.moveto(self.station):
                if self.world_interface.at_station(self.station):
                    self.success()
            else:
                self.failure()
        return self.state

class Pick(SmBehavior):
    """
    Pick up an object
    """
    def initialise(self):
        self.state = None

    def update(self):
        super(Pick, self).update()
        if self.state is None:
            self.state = pt.common.Status.RUNNING
        if self.state is pt.common.Status.RUNNING:
            if self.world_interface.pick():
                self.success()
            else:
                self.failure()
        return self.state

class Place(SmBehavior):
    """
    Places all objects held at current position
    """
    def initialise(self):
        self.state = None

    def update(self):
        super(Place, self).update()

        if self.state is None:
            self.state = pt.common.Status.RUNNING
        if self.state is pt.common.Status.RUNNING:
            if self.world_interface.place():
                self.success()
            else:
                self.failure()
        return self.state

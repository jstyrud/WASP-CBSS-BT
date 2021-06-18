"""
Unit test for behaviors.py
"""
import py_trees as pt
import simulation.conveyor_kitting as simulation
import simulation.behaviors as behaviors

def test_at_station():
    """ Tests at station behavior """
    sm = simulation.Simulation()
    behavior, _ = behaviors.get_node_from_string("at station CHARGE1", sm)
    sm.state.robot_pos = simulation.get_pos(simulation.Stations.CHARGE1)
    behavior.initialise()
    assert behavior.update() == pt.common.Status.SUCCESS

    behavior, _ = behaviors.get_node_from_string("at station CHARGE2", sm)
    sm.state.robot_pos = simulation.get_pos(simulation.Stations.CHARGE2)
    behavior.initialise()
    assert behavior.update() == pt.common.Status.SUCCESS

    behavior, _ = behaviors.get_node_from_string("at station CONVEYOR_HEAVY", sm)
    sm.state.robot_pos = simulation.get_pos(simulation.Stations.CONVEYOR_HEAVY)
    behavior.initialise()
    assert behavior.update() == pt.common.Status.SUCCESS

    behavior, _ = behaviors.get_node_from_string("at station CONVEYOR_LIGHT", sm)
    sm.state.robot_pos = simulation.get_pos(simulation.Stations.CONVEYOR_LIGHT)
    behavior.initialise()
    assert behavior.update() == pt.common.Status.SUCCESS

    behavior, _ = behaviors.get_node_from_string("at station DELIVERY", sm)
    behavior.initialise()
    assert behavior.update() == pt.common.Status.FAILURE
    sm.state.robot_pos = simulation.get_pos(simulation.Stations.DELIVERY)
    assert behavior.update() == pt.common.Status.SUCCESS

def test_battery_level():
    """ Tests battery level behavior """
    sm = simulation.Simulation()
    behavior, _ = behaviors.get_node_from_string("battery level > 50", sm)

    sm.state.battery_level = 51
    assert behavior.update() == pt.common.Status.SUCCESS

    sm.state.battery_level = 50
    assert behavior.update() == pt.common.Status.FAILURE

    behavior, _ = behaviors.get_node_from_string("battery level < 50", sm)
    assert behavior.update() == pt.common.Status.FAILURE

    sm.state.battery_level = 49
    assert behavior.update() == pt.common.Status.SUCCESS

def test_carried_weight():
    """ Tests carried weight behavior """
    sm = simulation.Simulation()
    behavior, _ = behaviors.get_node_from_string("carried weight > 5", sm)

    sm.state.carried_weight = 6
    assert behavior.update() == pt.common.Status.SUCCESS

    sm.state.carried_weight = 5
    assert behavior.update() == pt.common.Status.FAILURE

    behavior, _ = behaviors.get_node_from_string("carried weight < 5", sm)
    assert behavior.update() == pt.common.Status.FAILURE

    sm.state.carried_weight = 4
    assert behavior.update() == pt.common.Status.SUCCESS

def test_carried_light():
    """ Tests carried light behavior """
    sm = simulation.Simulation()
    behavior, _ = behaviors.get_node_from_string("carried light > 5", sm)

    sm.state.carried_light = 6
    assert behavior.update() == pt.common.Status.SUCCESS

    sm.state.carried_light = 5
    assert behavior.update() == pt.common.Status.FAILURE

    behavior, _ = behaviors.get_node_from_string("carried light < 5", sm)
    assert behavior.update() == pt.common.Status.FAILURE

    sm.state.carried_light = 4
    assert behavior.update() == pt.common.Status.SUCCESS

def test_carried_heavy():
    """ Tests carried heavy behavior """
    sm = simulation.Simulation()
    behavior, _ = behaviors.get_node_from_string("carried heavy > 5", sm)

    sm.state.carried_heavy = 6
    assert behavior.update() == pt.common.Status.SUCCESS

    sm.state.carried_heavy = 5
    assert behavior.update() == pt.common.Status.FAILURE

    behavior, _ = behaviors.get_node_from_string("carried heavy < 5", sm)
    assert behavior.update() == pt.common.Status.FAILURE

    sm.state.carried_heavy = 4
    assert behavior.update() == pt.common.Status.SUCCESS

def test_conveyor_light():
    """ Tests conveyor light behavior """
    sm = simulation.Simulation()
    behavior, _ = behaviors.get_node_from_string("conveyor light > 5", sm)

    sm.state.cnv_n_light = 6
    assert behavior.update() == pt.common.Status.SUCCESS

    sm.state.cnv_n_light = 5
    assert behavior.update() == pt.common.Status.FAILURE

    behavior, _ = behaviors.get_node_from_string("conveyor light < 5", sm)
    assert behavior.update() == pt.common.Status.FAILURE

    sm.state.cnv_n_light = 4
    assert behavior.update() == pt.common.Status.SUCCESS

def test_conveyor_heavy():
    """ Tests conveyor heavy behavior """
    sm = simulation.Simulation()
    behavior, _ = behaviors.get_node_from_string("conveyor heavy > 5", sm)

    sm.state.cnv_n_heavy = 6
    assert behavior.update() == pt.common.Status.SUCCESS

    sm.state.cnv_n_heavy = 5
    assert behavior.update() == pt.common.Status.FAILURE

    behavior, _ = behaviors.get_node_from_string("conveyor heavy < 5", sm)
    assert behavior.update() == pt.common.Status.FAILURE

    sm.state.cnv_n_heavy = 4
    assert behavior.update() == pt.common.Status.SUCCESS

def test_idle():
    """ Tests idle behavior """
    sm = simulation.Simulation()
    behavior, _ = behaviors.get_node_from_string("idle", sm)
    behavior.initialise()
    assert behavior.update() == pt.common.Status.RUNNING

def test_charge():
    """ Tests charge behavior """
    sm = simulation.Simulation()
    behavior, _ = behaviors.get_node_from_string("charge", sm)
    sm.state.robot_pos = simulation.get_pos(simulation.Stations.CHARGE1)
    sm.state.battery_level = 5
    behavior.initialise()
    for _ in range(5):
        assert behavior.update() == pt.common.Status.RUNNING
        sm.ready_for_action = True
    for _ in range(10):
        behavior.update()
        sm.ready_for_action = True
    assert behavior.update() == pt.common.Status.SUCCESS

def test_moveto():
    """ Tests moveto behavior """
    sm = simulation.Simulation()
    behavior, _ = behaviors.get_node_from_string("move to CHARGE1", sm)
    behavior.initialise()
    for _ in range(10):
        behavior.update()
        sm.ready_for_action = True
    assert sm.state.robot_pos == simulation.get_pos(simulation.Stations.CHARGE1)

    sm.state.battery_level = simulation.MAX_BATTERY
    behavior, _ = behaviors.get_node_from_string("move to CHARGE2", sm)
    behavior.initialise()
    for _ in range(10):
        behavior.update()
        sm.ready_for_action = True
    assert sm.state.robot_pos == simulation.get_pos(simulation.Stations.CHARGE2)

    sm.state.battery_level = simulation.MAX_BATTERY
    behavior, _ = behaviors.get_node_from_string("move to CONVEYOR_HEAVY", sm)
    behavior.initialise()
    for _ in range(10):
        behavior.update()
        sm.ready_for_action = True
    assert sm.state.robot_pos == simulation.get_pos(simulation.Stations.CONVEYOR_HEAVY)

    sm.state.battery_level = simulation.MAX_BATTERY
    behavior, _ = behaviors.get_node_from_string("move to CONVEYOR_LIGHT", sm)
    behavior.initialise()
    for _ in range(10):
        behavior.update()
        sm.ready_for_action = True
    assert sm.state.robot_pos == simulation.get_pos(simulation.Stations.CONVEYOR_LIGHT)

    sm.state.battery_level = simulation.MAX_BATTERY
    behavior, _ = behaviors.get_node_from_string("move to DELIVERY", sm)
    behavior.initialise()
    for _ in range(10):
        behavior.update()
        sm.ready_for_action = True
    assert sm.state.robot_pos == simulation.get_pos(simulation.Stations.DELIVERY)


def test_pick():
    """ Tests pick behavior """
    sm = simulation.Simulation()
    behavior, _ = behaviors.get_node_from_string("pick", sm)
    behavior.initialise()
    sm.state.robot_pos = simulation.get_pos(simulation.Stations.CONVEYOR_HEAVY)
    sm.state.cnv_n_heavy = 5
    behavior.update()
    sm.ready_for_action = True
    assert behavior.update() == pt.common.Status.SUCCESS
    sm.ready_for_action = True
    assert sm.state.cnv_n_heavy == 4
    assert sm.state.carried_heavy == 1
    assert sm.state.carried_weight == simulation.HEAVY_WEIGHT

    behavior.initialise()
    sm.state.robot_pos = simulation.get_pos(simulation.Stations.CONVEYOR_LIGHT)
    sm.state.cnv_n_heavy = 0
    assert behavior.update() == pt.common.Status.FAILURE
    sm.ready_for_action = True
    behavior.initialise()
    sm.state.cnv_n_light = 4
    behavior.update()
    sm.ready_for_action = True
    assert behavior.update() == pt.common.Status.SUCCESS
    assert sm.state.cnv_n_light == 3
    assert sm.state.carried_light == 1
    assert sm.state.carried_weight == simulation.LIGHT_WEIGHT + simulation.HEAVY_WEIGHT

def test_place():
    """ Tests place behavior """
    sm = simulation.Simulation()
    behavior, _ = behaviors.get_node_from_string("place", sm)
    behavior.initialise()
    sm.state.robot_pos = simulation.get_pos(simulation.Stations.CHARGE1)
    sm.state.carried_heavy = 1
    sm.state.carried_light = 1
    sm.state.carried_weight = simulation.HEAVY_WEIGHT + simulation.LIGHT_WEIGHT

    assert behavior.update() == pt.common.Status.FAILURE

    behavior.initialise()
    sm.state.robot_pos = simulation.get_pos(simulation.Stations.DELIVERY)
    behavior.update()
    assert behavior.update() == pt.common.Status.SUCCESS
    assert sm.state.carried_heavy == 0
    assert sm.state.carried_light == 0
    assert sm.state.delivered_heavy == 1
    assert sm.state.delivered_light == 1
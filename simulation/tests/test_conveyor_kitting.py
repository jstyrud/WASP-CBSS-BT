"""
Testing simulation of a robot performing kitting from two conveyors
"""
import simulation.conveyor_kitting as simulation

def test_moveto():
    """
    Tests moveto function
    """
    sim = simulation.Simulation()
    for _ in range(10):
        sim.moveto(simulation.Stations.CHARGE1)
    assert sim.state.robot_pos == simulation.get_pose(simulation.Stations.CHARGE1)

    for _ in range(10):
        sim.moveto(simulation.Stations.CHARGE2)
    assert sim.state.robot_pos == simulation.get_pose(simulation.Stations.CHARGE2)

    for _ in range(10):
        sim.moveto(simulation.Stations.CONVEYOR_LIGHT)
    assert sim.state.robot_pos == simulation.get_pose(simulation.Stations.CONVEYOR_LIGHT)

    for _ in range(10):
        sim.moveto(simulation.Stations.CONVEYOR_HEAVY)
    assert sim.state.robot_pos == simulation.get_pose(simulation.Stations.CONVEYOR_HEAVY)

    for _ in range(10):
        sim.moveto(simulation.Stations.DELIVERY)
    assert sim.state.robot_pos == simulation.get_pose(simulation.Stations.DELIVERY)

def test_charge():
    """
    Tests charge function
    """
    sim = simulation.Simulation()

    for _ in range(10):
        sim.moveto(simulation.Stations.CHARGE1)
    sim.state.battery_level = 5
    for _ in range(20):
        sim.charge()
    assert sim.state.battery_level == simulation.MAX_BATTERY

def test_pick():
    """
    Tests pick function
    """
    sim = simulation.Simulation()
    for _ in range(10):
        sim.moveto(simulation.Stations.CONVEYOR_LIGHT)
    sim.state.cnv_n_light += 1
    assert sim.pick() == True
    assert sim.state.carried_light == 1

    for _ in range(10):
        sim.moveto(simulation.Stations.CONVEYOR_HEAVY)
    sim.state.cnv_n_heavy += 1
    assert sim.pick() == True
    assert sim.state.carried_heavy == 1

def test_place():
    """
    Tests place function
    """
    sim = simulation.Simulation()
    for _ in range(10):
        sim.moveto(simulation.Stations.CONVEYOR_LIGHT)
    sim.state.cnv_n_light += 1
    assert sim.pick()
    assert sim.state.carried_light == 1

    for _ in range(10):
        sim.moveto(simulation.Stations.CONVEYOR_HEAVY)
    sim.state.cnv_n_heavy += 1
    assert sim.pick()
    assert sim.state.carried_heavy == 1

    for _ in range(10):
        sim.moveto(simulation.Stations.DELIVERY)
    assert sim.place()
    assert sim.state.carried_light == 0
    assert sim.state.carried_heavy == 0

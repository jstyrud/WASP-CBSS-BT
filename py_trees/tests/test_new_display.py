#!/usr/bin/env python3
#
# License: BSD
#   https://raw.githubusercontent.com/splintered-reality/py_trees/devel/LICENSE
#
##############################################################################
# Documentation
##############################################################################

"""
.. argparse::
   :module: py_trees.demos.pick_up_where_you_left_off
   :func: command_line_argument_parser
   :prog: py-trees-demo-pick-up-where-you-left-off
.. graphviz:: dot/pick_up_where_you_left_off.dot
.. image:: images/pick_up_where_you_left_off.gif
"""

##############################################################################
# Imports
##############################################################################

import argparse
import functools
import py_trees
import sys
import time

import py_trees.console as console

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
log_path = os.path.join(dir_path, 'logs')

##############################################################################
# Classes
##############################################################################

def pre_tick_handler(behaviour_tree):
    """
    This prints a banner and will run immediately before every tick of the tree.
    Args:
        behaviour_tree (:class:`~py_trees.trees.BehaviourTree`): the tree custodian
    """
    print("\n--------- Run %s ---------\n" % behaviour_tree.count)



def post_tick_handler(snapshot_visitor, behaviour_tree):
    """
    Prints an ascii tree with the current snapshot status.
    """
    print(
        "\n" + py_trees.display.unicode_tree(
            root=behaviour_tree.root,
            visited=snapshot_visitor.visited,
            previously_visited=snapshot_visitor.previously_visited
        )
    )
    name_ = 'root' + str(behaviour_tree.count)
    py_trees.display.render_dot_tree(behaviour_tree.root, name=name_, target_directory=log_path, static=False)


def create_root():
    task_one = py_trees.behaviours.Count(
        name="Task 1",
        fail_until=0,
        running_until=2,
        success_until=10
    )
    task_two = py_trees.behaviours.Count(
        name="Task 2",
        fail_until=0,
        running_until=2,
        success_until=10
    )
    high_priority_interrupt = py_trees.decorators.RunningIsFailure(
        child=py_trees.behaviours.Periodic(
            name="High Priority",
            n=3
        )
    )
    piwylo = py_trees.idioms.pick_up_where_you_left_off(
        name="Pick Up\nWhere You\nLeft Off",
        tasks=[task_one, task_two]
    )
    root = py_trees.composites.Selector(name="Root")
    root.add_children([high_priority_interrupt, piwylo])

    return root

##############################################################################
# Main
##############################################################################


def main():
    """
    Entry point for the demo script.
    """
    py_trees.logging.level = py_trees.logging.Level.DEBUG
    root = create_root()

    ####################
    # Tree Stewardship
    ####################
    behaviour_tree = py_trees.trees.BehaviourTree(root)
    behaviour_tree.add_pre_tick_handler(pre_tick_handler)
    behaviour_tree.visitors.append(py_trees.visitors.DebugVisitor())
    snapshot_visitor = py_trees.visitors.SnapshotVisitor()
    behaviour_tree.add_post_tick_handler(functools.partial(post_tick_handler, snapshot_visitor))
    behaviour_tree.visitors.append(snapshot_visitor)
    behaviour_tree.setup(timeout=15)
    py_trees.display.render_dot_tree(behaviour_tree.root, name='static', target_directory=log_path)


    for unused_i in range(1, 11):
        behaviour_tree.tick()

    print("\n")


if __name__ == '__main__':
    main()
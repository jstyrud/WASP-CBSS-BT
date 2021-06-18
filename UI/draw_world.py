#!/usr/bin/env python3
"""
Class to print the state of the world
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
from matplotlib.patches import RegularPolygon, Rectangle
from celluloid import Camera

class Object:
    """ Class for graphical objects parameters """
    def __init__(self, x, y, l, h, line='black', fill='white'):
        """
        Initialize the object with origin, dimension and graphical properties.
        """
        self.origin = (x, y)
        self.length = l
        self.height = h
        self.line = line
        self.fill = fill

    def set_origin(self, x, y):
        """
        Function to set the pose of an object.
        """
        self.origin = (x, y)

class WorldUI:
    """ User Interface that allows prints the world state """

    def __init__(self):
        """
        Initialize the static objects in the world.
        """
        self.figure, self.axes = plt.subplots(nrows=1, ncols=2, figsize=(12,6), gridspec_kw={'width_ratios': [3, 1]})
        self.map_ax = self.axes[0]
        self.table_ax = self.axes[1]
        self.camera = Camera(self.figure)

        title_text = 'World State'
        # Add title
        plt.suptitle(title_text)

        # initialize Map object
        self.map = Object(x=0, y=0, l=25, h=15, line='black', fill='white')
        # initialize Conveyors (L: light objects, H: heavy objects)
        self.conv_l = Object(x=1, y=2, l=10, h=2, line='black', fill='gainsboro')
        self.conv_h = Object(x=1, y=11, l=10, h=2, line='black', fill='gainsboro')
        # initialize Delivery
        self.delivery = Object(x=22, y=5, l=3, h=5, line='red', fill='gainsboro')
        # initialize Charging stations (C: near conveyors, D: near delivery)
        self.charge_c = Object(x=0, y=6.5, l=1, h=2, line='black', fill='limegreen')
        self.charge_d = Object(x=24, y=11, l=1, h=2, line='black', fill='limegreen')
        # initialize the Item objects (L: light objects, H: heavy objects)
        self.item_l = Object(x=0, y=0, l=0.5, h=0.5, line='red', fill='red')
        self.item_h = Object(x=0, y=0, l=0.5, h=1, line='blue', fill='blue')

    def reset_world(self):
        """
        Reset the world with static objects and robot in home position.
        """
        # add the Map
        self.map_ax.add_patch(Rectangle(self.map.origin, self.map.length, self.map.height, \
            edgecolor=self.map.line, facecolor=self.map.fill))

        # add the Conveyors:
        # - main gray band
        # - black entry point
        # - black band lines
        # - label
        self.axes.add_patch(Rectangle(self.conv_l.origin, self.conv_l.length, self.conv_l.height, \
                                      edgecolor=self.conv_l.line, facecolor=self.conv_l.fill))
        self.axes.add_patch(Rectangle((self.conv_l.origin[0]-1, self.conv_l.origin[1]-1), 1, 4, \
            edgecolor='black', facecolor='black'))
        for i in range(self.conv_l.length):
            x_points = [self.conv_l.origin[0]+i, self.conv_l.origin[0]+i]
            y_points = [self.conv_l.origin[1], self.conv_l.origin[1]+self.conv_l.height]
            line = lines.Line2D(x_points, y_points, color='black', axes=self.axes)
            self.axes.add_line(line)
        self.axes.text(self.conv_l.origin[0]+0.5, self.conv_l.origin[1]-1.5, 'Conveyor LIGHT')

        self.axes.add_patch(Rectangle(self.conv_h.origin, self.conv_h.length, self.conv_h.height,  \
                                      edgecolor=self.conv_h.line, facecolor=self.conv_h.fill))
        self.axes.add_patch(Rectangle((self.conv_h.origin[0]-1, self.conv_h.origin[1]-1), 1, 4, \
            edgecolor='black', facecolor='black'))
        for i in range(self.conv_h.length):
            x_points = [self.conv_h.origin[0]+i, self.conv_h.origin[0]+i]
            y_points = [self.conv_h.origin[1], self.conv_h.origin[1]+self.conv_h.height]
            line = lines.Line2D(x_points, y_points, color='black', axes=self.axes)
            self.axes.add_line(line)
        self.axes.text(self.conv_h.origin[0]+0.5, self.conv_h.origin[1]+self.conv_h.height+1, 'Conveyor HEAVY')

        # add the Delivery area
        self.map_ax.add_patch(Rectangle(self.delivery.origin, self.delivery.length, self.delivery.height,  \
            edgecolor=self.delivery.line, facecolor=self.delivery.fill))
        self.map_ax.text(self.delivery.origin[0]-0.5, self.delivery.origin[1]-1, 'Delivery')

        # add the Chargin stations
        self.axes.add_patch(Rectangle(self.charge_c.origin, self.charge_c.length, self.charge_c.height, \
            edgecolor=self.charge_c.line, facecolor=self.charge_c.fill))
        self.axes.text(self.charge_c.origin[0]-0.5, self.charge_c.origin[1]-1, 'Charge 1')
        self.axes.add_patch(Rectangle(self.charge_d.origin, self.charge_d.length, self.charge_d.height, \
            edgecolor=self.charge_d.line, facecolor=self.charge_d.fill))
        self.axes.text(self.charge_d.origin[0]-2, self.charge_d.origin[1]+2.5, 'Charge 2')

    def add_robot(self, pose):
        """
        Add the robot in the UI.
        """
        self.map_ax.add_patch(RegularPolygon(pose, 8, radius=1, orientation=math.pi/8, \
            edgecolor='black', facecolor='paleturquoise'))
        self.map_ax.text(pose[0]-0.4, pose[1]-0.2, 'R', fontweight='bold')


    def add_items(self, n_light, n_heavy):
        """
        Add the heavy and light items to the conveyor
        """
        self.reset_world()
        origin_lx = self.conv_l.origin[0] + self.conv_l.length - self.item_l.length*1.5
        origin_ly = self.conv_l.origin[1] + 0.5*(self.conv_l.height - self.item_l.height)
        for i in range(n_light):
            self.item_l.set_origin(origin_lx - i, origin_ly)
            self.axes.add_patch(Rectangle(self.item_l.origin, self.item_l.length, self.item_l.height, \
                edgecolor=self.item_l.line, facecolor=self.item_l.fill))

        origin_hx = self.conv_h.origin[0] + self.conv_h.length - self.item_h.length*1.5
        origin_hy = self.conv_h.origin[1] + 0.5*(self.conv_h.height - self.item_h.height)
        for i in range(n_heavy):
            self.item_h.set_origin(origin_hx - i, origin_hy)
            self.axes.add_patch(Rectangle(self.item_h.origin, self.item_h.length, self.item_h.height, \
                edgecolor=self.item_h.line, facecolor=self.item_h.fill))


    def add_state(self, world_state):
        """
        Add the world state in the UI.
        It assumes that the world state has a field Robot with its pose.
        It assumes that the world state has fields Nr. of Heavy/Light objects in the conveyors.
        """
        self.add_items(world_state.cnv_n_light, world_state.cnv_n_heavy)
        self.add_robot((world_state.robot_pos.x, world_state.robot_pos.y))


    def save_world(self, name):
        """
        Save the world with added patches to file.
        """
        self.map_ax.plot()
        path = name + '.svg'
        self.figure.savefig(path)
        plt.close(self.figure)


    def add_table(self, world_state):
        """
        Plot a table summing up the world state.
        """
        
        headers = ['robot pose', 'battery lv', 'carried weight', 'carried light', 'carried heavy', \
            'heavy in conveyor', 'light in conveyor', 'delivered heavy', 'delivered light']
        robot_pos = (world_state.robot_pos.x, world_state.robot_pos.x)
        values = [robot_pos, world_state.battery_level, world_state.carried_weight, \
            world_state.carried_light, world_state.carried_heavy, world_state.cnv_n_light, \
            world_state.cnv_n_heavy, world_state.delivered_heavy, world_state.delivered_light]

        cell_text = []
        for val in values:
            cell_text.append([str(val)])

        rcolors = plt.cm.BuPu(np.full(len(headers), 0.1))
        #Add a table at the bottom of the axes
        the_table = plt.table(cellText=cell_text,
                            rowLabels=headers,
                            rowColours=rcolors,
                            rowLoc='right',
                            cellLoc='left',
                            loc='center',
                            colWidths=[0.3 for x in cell_text])
        the_table.scale(1, 1.5)
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(9)
        self.table_ax.add_table(the_table)
        # Hide axes
        self.table_ax.get_xaxis().set_visible(False)
        self.table_ax.get_yaxis().set_visible(False)
        # Hide axes border
        plt.box(on=None)
        plt.draw()


    def plot_world(self):
        """
        Plot the world
        """
        self.map_ax.plot()
        self.table_ax.plot()
        self.camera.snap()


    def animate(self):
        """
        Save an animated gif of the world, one frame per tick
        """
        animation = self.camera.animate()
        animation.save('UI/tests/animation.gif', writer='imagemagick')

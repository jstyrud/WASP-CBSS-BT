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
        self.figure, self.axes = plt.subplots(nrows=1, ncols=2)
        self.map_ax = self.axes[0]
        self.table_ax = self.axes[1]
        self.camera = Camera(self.figure)

        title_text = 'World State'
        # Add title
        plt.suptitle(title_text)

        # initialize Map object
        self.map = Object(x=0, y=0, l=25, h=15, line='black', fill='white')
        # initialize Conveyors (L: light objects, H: heavy objects)
        self.convL = Object(x=1, y=2, l=10, h=2, line='black', fill='gainsboro')
        self.convH = Object(x=1, y=11, l=10, h=2, line='black', fill='gainsboro')
        # initialize Delivery
        self.delivery = Object(x=22, y=5, l=3, h=5, line='red', fill='gainsboro')
        # initialize Charging stations (C: near conveyors, D: near delivery)
        self.chargeC = Object(x=0, y=6.5, l=1, h=2, line='black', fill='limegreen')
        self.chargeD = Object(x=24, y=11, l=1, h=2, line='black', fill='limegreen')
        # initialize the Item objects (L: light objects, H: heavy objects)
        self.itemL = Object(x=0, y=0, l=0.5, h=0.5, line='red', fill='red')
        self.itemH = Object(x=0, y=0, l=0.5, h=1, line='blue', fill='blue')

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
        self.map_ax.add_patch(Rectangle(self.convL.origin, self.convL.length, self.convL.height, \
                                      edgecolor=self.convL.line, facecolor=self.convL.fill))
        self.map_ax.add_patch(Rectangle((self.convL.origin[0]-1, self.convL.origin[1]-1), 1, 4, \
            edgecolor='black', facecolor='black'))
        for i in range(self.convL.length):
            x_points = [self.convL.origin[0]+i, self.convL.origin[0]+i]
            y_points = [self.convL.origin[1], self.convL.origin[1]+self.convL.height]
            line = lines.Line2D(x_points, y_points, color='black', axes=self.map_ax)
            self.map_ax.add_line(line)
        self.map_ax.text(self.convL.origin[0]+0.5, self.convL.origin[1]-1.5, 'Conveyor LIGHT')

        self.map_ax.add_patch(Rectangle(self.convH.origin, self.convH.length, self.convH.height,  \
                                      edgecolor=self.convH.line, facecolor=self.convH.fill))
        self.map_ax.add_patch(Rectangle((self.convH.origin[0]-1, self.convH.origin[1]-1), 1, 4, \
            edgecolor='black', facecolor='black'))
        for i in range(self.convH.length):
            x_points = [self.convH.origin[0]+i, self.convH.origin[0]+i]
            y_points = [self.convH.origin[1], self.convH.origin[1]+self.convH.height]
            line = lines.Line2D(x_points, y_points, color='black', axes=self.map_ax)
            self.map_ax.add_line(line)
        self.map_ax.text(self.convH.origin[0]+0.5, self.convH.origin[1]+self.convH.height+1, 'Conveyor HEAVY')

        # add the Delivery area
        self.map_ax.add_patch(Rectangle(self.delivery.origin, self.delivery.length, self.delivery.height,  \
            edgecolor=self.delivery.line, facecolor=self.delivery.fill))
        self.map_ax.text(self.delivery.origin[0]-0.5, self.delivery.origin[1]-1, 'Delivery')

        # add the Chargin stations
        self.map_ax.add_patch(Rectangle(self.chargeC.origin, self.chargeC.length, self.chargeC.height, \
            edgecolor=self.chargeC.line, facecolor=self.chargeC.fill))
        self.map_ax.text(self.chargeC.origin[0]-0.5, self.chargeC.origin[1]-1, 'Charge 1')
        self.map_ax.add_patch(Rectangle(self.chargeD.origin, self.chargeD.length, self.chargeD.height, \
            edgecolor=self.chargeD.line, facecolor=self.chargeD.fill))
        self.map_ax.text(self.chargeD.origin[0]-2, self.chargeD.origin[1]+2.5, 'Charge 2')

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
        origin_lX = self.convL.origin[0] + self.convL.length - self.itemL.length*1.5
        origin_lY = self.convL.origin[1] + 0.5*(self.convL.height - self.itemL.height)
        for i in range(n_light):
            self.itemL.set_origin(origin_lX - i, origin_lY)
            self.map_ax.add_patch(Rectangle(self.itemL.origin, self.itemL.length, self.itemL.height, \
                edgecolor=self.itemL.line, facecolor=self.itemL.fill))

        origin_hX = self.convH.origin[0] + self.convH.length - self.itemH.length*1.5
        origin_hY = self.convH.origin[1] + 0.5*(self.convH.height - self.itemH.height)
        for i in range(n_heavy):
            self.itemH.set_origin(origin_hX - i, origin_hY)
            self.map_ax.add_patch(Rectangle(self.itemH.origin, self.itemH.length, self.itemH.height, \
                edgecolor=self.itemH.line, facecolor=self.itemH.fill))


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


    def state_table(self, world_state):
        """
        Plot a table summing up the world state.
        """
        
        headers = ['robot pose', 'battery lv', 'carried weight', 'carried light', 'carried heavy', \
            'heavy in conveyor', 'light in conveyor', 'delivered heavy', 'delivered light']
        values = [world_state.robot_pos, world_state.battery_level, world_state.carried_weight, \
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
                            loc='right',
                            colWidths=[0.3 for x in cell_text])
        the_table.scale(1, 1.5)
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(10)
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
        Print a gif with the animation of the simulation
        """
        animation = self.camera.animate()
        animation.save('animation.gif', writer='imagemagick')

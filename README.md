# WASP-CBSS-BT

## Objective
Your goal in this exercise is to construct a Behavior Tree (BT) that controls a mobile robot transferring objects from two conveyors to a delivery table. The two conveyors hold two different items. The top conveyor holds heavy objects which give a higher reward but due to their weight, the robot cannot carry as many. The bottom conveyor holds lighter objects. The robot also has a battery that needs to be recharged repeatedly. If the robot runs out of battery, it will no longer be able to move and no more objects can be transported. The behavior tree needs to find the best trade-off and decide when to perform each action.
![image](https://github.com/jstyrud/WASP-CBSS-BT/blob/main/environment.png)

## Setup the Environment and complete the challenge!
Go to https://github.com/jstyrud/WASP-CBSS-BT for all source code necessary. All you need to do is load the `runme.ipynb` [notebook](https://github.com/jstyrud/WASP-CBSS-BT/blob/main/runme.ipynb) and run it in some environment of your choice, we suggest [Colaboratory](https://colab.research.google.com/). Every other environment running the notebook is also fine but it might require some more preparation steps we do not provide instructions nor support for. Note that to run Colab you need to have a Google account.

In order to setup the notebook in Colab, first open a [new project](https://colab.research.google.com/notebooks/intro.ipynb?utm_source=scs-index) which will look like the image below.
![image](https://github.com/jstyrud/WASP-CBSS-BT/blob/main/colab1.png)

Then, to open the `runme.ipynb` notebook, on the top-left toolbar, go to `File`, then `Open Notebook`. This will prompt a window, where you need to select `GitHub` and paste the link to this repository. Colab will automatically recognise the notebook, that you can select to open.
![image](https://github.com/jstyrud/WASP-CBSS-BT/blob/main/colab2.png)

Once the notebook is loaded, you have to connect it to some hardware resources. You do so by pressing the `Connect` button on the top-right corner. Running in the free servers is kind of slow, so if you want to you can set up a local runtime, just follow the instructions. Or just skip the notebook and run code in a python file locally which will be even faster.

You will construct the Behavior Trees as string inputs, but in the notebook are functions to show them graphically and to show animations of episodes of the robot being controlled by the behavior tree.  
An example of a string representation of a BT is (the string symbols are defined in section [Available Behaiviors](#available-behaviors)):
```bash
individual = ['s(', 'f(', 'carried weight < 5?', \
                          's(', 'move to CHARGE1', 'charge!', ')', ')', \
                    'f(', 'conveyor light < 1?', 's(', 'move to CONVEYOR_LIGHT!', 'idle!', ')']
```
which represents the following BT:

![image](https://github.com/jstyrud/WASP-CBSS-BT/blob/main/BT_example.png)

The code for the simulation is all available on github and you may look at it or manipulate it locally for your own purposes, for example running some learning or search algorithm. When evaluating your behavior tree however, we will be doing it with the original code, only using your string representation of the behavior tree.

## Detailed task description
Each episode will run for 200 steps, with the tree being ticked 200 times. New objects will spawn on the heavy and light conveyors each step with a probability 6% of a heavy object spawning any given time step, and 12% for a light object being spawned. Each conveyor holds a maximum of 10 objects before being full. Moreover, the robot can only carry a maximum weight of 10. Heavy objects weigh 4 and light objects weight 2. The robot moves at a speed of 5. The battery has a maximum capacity of 100 and depletes with 1 for every action taken, plus 1 every time step regardless of whether an action was taken or not. The tree will always be ticked 200 times regardless of whether the root node returns SUCCESS, FAILURE or RUNNING at any time.  
After the episode you will be given a reward based on performance. For every heavy object delivered to the delivery table, 2 points are awarded. For every light object you will get 1 point. If at any given time step a conveyor is full when an object would otherwise have spawned, the rest of the factory is kept waiting and you receive a penalty of -0.5 points for blocked heavy objects and -0.25 points for blocked light objects. Finally we will remove 0.2 points for every node in the behavior tree so smaller trees are better.

### Example
You delivered 1 heavy object and 3 light objects, but you were to slow so 2 heavy objects were blocked and 10 light objects. Your tree consists of 25 nodes. The total fitness becomes:
2 * 1 + 1 * 3 – 0.5 * 2 – 0.25 * 10 – 0.2 * 25 = -3.5


## Submitting your behavior tree and getting a score.
You should try to find and work in groups of two. Some group(s) may have to be three so that everyone gets a group. Send an e-mail to jstyrud@kth.se and write your clever and witty group name in the subject. Also put the names of all members of your group in the e-mail. The deadline is 16.15. If possible, please send in your work earlier so that I have some time to evaluate. We will reconvenve at 16.40 in the lecture hall. Your behavior tree will be run on 100 episodes with different random seeds and your fitness is the average of those 100 episodes (tree size penalty is given every episode). We will then put your fitness up for everyone to see on this [document](https://docs.google.com/spreadsheets/d/1QsGNwj7DgN3P_k7Fnsj1gEzuOy0UmRV8gDhnfegFgFY/edit?usp=sharing), so that you can see how your solution compares to others.
You only get to submit once per group, so make it count! You will of course be able to test run a lot of different seeds by yourselves to make it robust, but we will not be giving any information on which seeds are run by us.

## Available behaviors
Only a specified set of behaviors can be used as listed below.
### Control nodes
#### ‘f(’
Fallback node without memory. All subsequent nodes up to an ending ‘)’ are part of the subtree.
#### ‘fm(’
Fallback node with memory. All subsequent nodes up to an ending ‘)’ are part of the subtree.
#### ‘s(’
Sequence node without memory. All subsequent nodes up to an ending ‘)’ are part of the subtree.
#### ‘sm(’
Sequence node with memory. All subsequent nodes up to an ending ‘)’ are part of the subtree.

### Condition nodes
#### ‘at station \<STATION>?’
Checks if robot is currently at \<STATION>. \<STATION> can be any of the following five: CHARGE1, CHARGE2, CONVEYOR_HEAVY, CONVEYOR_LIGHT, DELIVERY.

Returns SUCCESS if robot is at the station, FAILURE otherwise.

#### ‘battery level \<value>?’
Checks if battery level is currently above or below the given value. Example ‘battery level > 4’ returns SUCCESS if battery level is above 4, FAILURE otherwise while ‘battery level < 4’ returns SUCCESS if battery level is below 4, FAILURE otherwise.

#### ‘carried weight \<value>?’
Checks if the robots currently carried weight is above or below the given value. Works like the battery level behavior.

#### ‘carried light \<value>?’
Checks if the number of currently carried light objects is above or below the given value. Works like the battery level behavior.

#### ‘carried heavy \<value>?’
Checks if the number currently carried heavy objects is above or below the given value. Works like the battery level behavior.

#### ‘conveyor light \<value>?’
Checks if the number of objects currently on the light conveyor is above or below the given value. Works like the battery level behavior.

#### ‘conveyor heavy \<value>?’
Checks if the number of objects currently on the heavy conveyor is above or below the given value. Works like the battery level behavior.

### Action nodes
#### ‘idle!’
Does nothing. Always returns RUNNING.

#### ‘charge!’
If the robot is at any of the charging stations it will charge, adding 10 to the current battery level and returning RUNNING. If it’s not at a charging station it will return FAILURE. IF battery is fully charged it returns SUCCESS.

#### ‘pick!’
If the robot is at any of the conveyors, and there is an object there that the robot can carry without exceeding the weight limit it will pick it up and return RUNNING, otherwise returns FAILURE. Only picks one object per time step.

#### ‘place!’
If the robot is at the delivery table it will place all objects on the delivery table and return RUNNING, otherwise returns FAILURE. Places all currently held objects in one time step. Returns RUNNING regardless of whether any objects are actually carried and then placed.

#### ‘move to \<STATION>!’
Move towards the given station with a maximum speed of 5. Only moves in either x or y direction any given time step. A movement of 1 in x and 1 in y will therefore take 2 timesteps even if total distance is less than 5. \<STATION> can be any of the following five: CHARGE1, CHARGE2, CONVEYOR_HEAVY, CONVEYOR_LIGHT, DELIVERY.
If the robot is already at the station it will return SUCCESS, otherwise it will return RUNNING.







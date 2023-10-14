import tkinter
import copy
import os
import pickle
import time
from tkinter.font import Font
import random
from config import *
import math
from threading import Thread

"""
The tkinter module is used to render shapes and text on the screen to make up the elements of the game.
Some basic functions of the tkinter module are:
 - self.create_rectangle(x, y, x0, y0) Creates a rectangle
 - self.create_text(x, y) Creates text
 - self.create_oval(x, y, x0, y0) Creates an oval
Options for the functions
 - fill: The color of the shape
 - outline: The color of the outline of the shape
 - tag: The tag of the shape used to delete elements

The Pickle module is used for saving data into a file. The files are called buildings.bobfile which stores
the buildings and coins.bobfile which stores the amount of coins.
Some basic functions of the pickle module are:
 - with open(filaname, 'rb') as bobfile:
       data = pickle.load(bobfile)
       Gets the data from a file.
 - with open(filename, 'wb') as bobfile:
       pickle.dump(object, bobfile)
       Puts data into a file.
       
The project uses the os module to check if a data file exists.
If the file does not exist, the program creates a new file.
The function used from the os module is os.path.isfile(path) which checks if a file exists.

The project uses the time module to get the current time. This time is used
to measure delays that an action is performed. An example is the cannon tower which uses
the time module to shoot a cannonball every x seconds.
The function used from the time module is time.time() which is the number of seconds since january 1, 1970
The value of the function cannot be used directly and must be a difference of the time and the last time
that an action was performed.
For example, to check if the delay is over, we can do if time.time() - lastAction < delay, then set
lastAction to the current time, and do the action.

The random module is used to generate random numbers.
The function used is random.randint(1, 10). This genereates a random integer from 1 to 10.
It is used in the project to spawn zombies in random positions.
"""


class Thing(tkinter.Canvas):
    """
This function gets called when the window is created.
It sets up the buttons and binds to the motion, update and key functions
"""

    def __init__(self):
        super().__init__(width=WIDTH, height=HEIGHT)
        self.x = 0  # x and y store the mouse position on screen
        self.y = 0

        self.pack()
        self.bind_all('<Button-1>', self.onclick)

        self.after(1, self.update)  # runs the update function every 1 millisecond

        # creating the buttons to play the game        
        self.create_rectangle(350, 170, 650, 330, tag='dosomething')
        self.create_rectangle(100, 180, 300, 320, tag='dosomethingelse')
        self.create_rectangle(700, 180, 900, 320, tag='dosomethingelseelse')

        self.create_text(500, 250, text='Build stuff', font=Font(size=20))
        self.create_text(200, 250, text='Exit')
        self.create_text(800, 250, text='Instructions')

        self.bind_all('<Motion>', self.on_motion)  # listen to mouse motion
        self.bind_all('<Key>', self.on_key)  # listen to keys

    def onclick(self, event):
        if 350 <= self.x <= 650 and 170 <= self.y <= 330:
            # go to the building selection screen.
            self.destroy()
            game = BuildingSelection()
        if 100 <= self.x <= 300 and 180 <= self.y <= 320:
            # quit the program.
            self.destroy()
            quit()
        if 700 <= self.x <= 900 and 180 <= self.y <= 320:
            # go to the instructions.
            self.destroy()
            game = Instructions()

    """
This function gets called every millisecond to update the elements
in the game.
"""

    def update(self):
        # checks if the mouse position is within the button rectangle.

        if 350 <= self.x <= 650 and 170 <= self.y <= 330:
            self.itemconfigure('dosomething', outline='red')  # changes outline to red
        else:
            self.itemconfigure('dosomething', outline='black')

        if 100 <= self.x <= 300 and 180 <= self.y <= 320:
            self.itemconfigure('dosomethingelse', outline='red')  # changes outline to red
        else:
            self.itemconfigure('dosomethingelse', outline='black')

        if 700 <= self.x <= 900 and 180 <= self.y <= 320:
            self.itemconfigure('dosomethingelseelse', outline='red')  # changes outline to red
        else:
            self.itemconfigure('dosomethingelseelse', outline='black')

        self.after(1, self.update)  # run update every 1 millisecond

    """
This function is called when the mouse moves to update the mouse
position.
"""

    def on_motion(self, e):
        # updates the mouse position when the mouse moves.
        self.x = e.x
        self.y = e.y

    """
This function is called when a key is pressed to do actions.
"""

    def on_key(self, e):
        if e.keysym in ['space', 'Return']:
            self.onclick(None)


class Instructions(tkinter.Canvas):
    """
This function gets called when the window is created.
It sets up the buttons and binds to the motion, update and key functions
"""

    def __init__(self):
        super().__init__(width=WIDTH, height=HEIGHT)

        self.pack()
        self.bind_all('<Button-1>', self.onclick)

        self.text = ['''
Welcome to Bob the Builder Simulator!
Press space to continue!''',

                     '''
Click on buttons by pressing the
Space or Return key on the keyboard,
or clicking your mouse!
Like this one!
''',
                     '''
Now we will go to the
building demonstration!
'''
                     ]  # the text that is in the instructions
        self.frame = 0  # The index of the current text
        self.clicks = 0  # The number of clicks on the button in frame 2

        self.create_text(500, 250, text=self.text[self.frame], tag='text')  # create instruction text
        self.after(1, self.update)  # run update every 1 millisecond
        self.bind_all('<Key>', self.on_key)  # listen to keys
        self.bind_all('<Motion>', self.on_motion)  # listen to mouse motion

    """
This function gets called every milisecond to update the elements
in the game.
"""

    def update(self):
        if self.frame == len(self.text):
            self.destroy()
            game = BuildingSelection(demo=True)
            return
        self.delete('text')
        self.create_text(500, 250, text=self.text[self.frame], tag='text')

        if self.frame == 1:
            if 400 < self.x < 600 and 300 < self.y < 350:
                self.create_rectangle(400, 300, 600, 350, fill='black', tag='text', outline='red')
            else:
                self.create_rectangle(400, 300, 600, 350, fill='black', tag='text')
            self.create_text(500, 325, text='Something', tag='text', fill='white')
            self.create_text(500, 400, text=f'{self.clicks} clicks', tag='text')
        self.after(1, self.update)  # run update every 1 millisecond

    """
This function is called when the mouse moves to update the mouse
position.
"""

    def on_motion(self, e):
        # updates the mouse position when the mouse moves.
        self.x = e.x
        self.y = e.y

    def onclick(self, event):
        flag = False
        if self.frame == 1:
            if 400 < self.x < 600 and 300 < self.y < 350:
                flag = True
                self.clicks += 1
        if not flag:
            self.frame += 1

    """
This function is called when a key is pressed to do actions.
"""

    def on_key(self, k):
        if k.keysym in ['space', 'Return']:
            self.onclick(None)


class InstructionsFinish(tkinter.Canvas):
    """
This function gets called when the window is created.
It sets up the buttons and binds to the motion, update and key functions
"""

    def __init__(self):
        super().__init__(width=WIDTH, height=HEIGHT)

        self.pack()
        self.bind_all('<Button-1>', self.onclick)
        self.create_text(500, 250, text='''You have finished the instructions.
Now you can do whatever you want.
Some additional features:
 - You can zoom in or zoom out
   by pressing + and -
 - Upgrade a building by pressing U
 - Sell a building by pressing S
 - Display information about building by pressing I
Press any key to continue.''')
        self.bind_all('<Key>', self.onKey)  # Listen to keys

    def onclick(self, event):
        # When a key is pressed, go to the main screen
        game = Thing()
        self.destroy()

    """
This function is called when a key is pressed to do actions.
"""

    def onKey(self, k):
        self.onclick(None)


class BuildingSelection(tkinter.Canvas):
    """
This function gets called when the window is created.
It sets up the buttons and binds to the motion, update and key functions
"""

    def __init__(self, demo=False):
        super().__init__(width=WIDTH, height=HEIGHT)

        self.demo = demo  # Stores whether it is a demo game

        self.demoframe = 0  # Stores the frame of the demo

        self.pack()
        self.bind_all('<Button-1>', self.onclick)

        self.offset = 0  # the offset when scrollling

        # x and y store the mouse position on screen
        self.x = 0
        self.y = 0

        self.after(1, self.update)  # run update every millisecond
        self.bind_all('<Key>', self.onKey)  # listen to keys
        self.bind_all('<Motion>', self.onMotion)  # listen to mouse motion

    """
This function is called when the mouse moves to update the mouse
position.
"""

    def onMotion(self, e):
        # update the mouse x and y when the mouse is moving
        self.x = e.x
        self.y = e.y

    """
This function gets called every milisecond to update the elements
in the game.
"""

    def update(self):
        global coins
        self.delete('thing')  # delete everything
        self.delete('block')

        pos = 100  # stores the position that the next building is rendered
        counter = 1  # stores the building number.

        self.create_text(100, 50 + self.offset, text='Your buildings',
                         tag='thing')  # Create text that says "Your buildings"

        if 500 < self.x < 800 and self.offset + 30 < self.y < self.offset + 80:  # check if the mouse is on the button
            self.create_rectangle(500, self.offset + 30, 800, self.offset + 80, fill='black', tag='thing',
                                  outline='red')  # create the new building button with the outline red
        else:
            self.create_rectangle(500, self.offset + 30, 800, self.offset + 80, fill='black',
                                  tag='thing')  # create the new building button

        self.create_text(650, self.offset + 55, text='Create new building', tag='thing',
                         fill='white')  # create the new building text
        for i in buildings:

            currentbuilding = buildings[i][0]
            cost = self.getBuildingCost(currentbuilding)  # get the cost of the building

            self.create_rectangle(65, pos + self.offset, 800, pos + 300 + self.offset, fill='black',
                                  tag='thing')  # Create the rectangle

            o = 0  # o stores the position of the button
            for _ in ['Open', 'Delete']:
                # create the buttons

                col = '#222222'
                if 600 < self.x < 750 and pos + self.offset + 50 + o < self.y < pos + 100 + self.offset + o and (
                        _ != 'Sell' or cost <= coins):  # check if the mouse is on the button
                    self.create_rectangle(600, pos + self.offset + 50 + o, 750, pos + 100 + self.offset + o, fill=col,
                                          tag='thing', outline='red')  # create the rectangle with the outline of red
                else:
                    self.create_rectangle(600, pos + self.offset + 50 + o, 750, pos + 100 + self.offset + o, fill=col,
                                          tag='thing')  # create the rectangle with no outline

                if _ == 'Sell':
                    if cost > coins:
                        self.create_text(675, pos + self.offset + 120 + o, text='This building is overpriced!',
                                         tag='thing', fill='red')  # display text if the buliding is overpriced

                self.create_text(675, pos + self.offset + 75 + o, text=_, tag='thing',
                                 fill='white')  # create the text of the button

                o += 75  # update o

            for j in currentbuilding:
                # draw the preview of the building
                for k in j:
                    k.draw(self, 65 + 10 * k.x + 200, pos + 10 * k.y + self.offset + 100, 10)

            # disp,lay information about the building
            self.create_text(90, pos - 10 + self.offset, text=f'Building {counter}', tag='thing')
            self.create_text(130, pos + 30 + self.offset, text=f'Day: {buildings[i][1]}\nPreview:', fill='white',
                             tag='thing')
            pos += 350  # update pos and counter
            counter += 1

        self.create_rectangle(500 - 100, 0, 500 + 100, 50, tag='thing', fill='#333333')  # Create rectangle
        self.create_text(500, 25, text=f'Coins: {coins}', tag='thing',
                         fill='white')  # Displays how many coins the person has.

        # Display information for the new user.
        if self.demo:
            if self.demoframe == 0:
                self.create_text(500, 250, text='Click on the new building button to create a new building!',
                                 tag='thing', fill='#999999')
                self.create_line(500, 230, 650, 90, tag='thing', fill='#999999')
                self.create_line(650, 90, 600, 90, tag='thing', fill='#999999')
                self.create_line(650, 90, 650, 140, tag='thing', fill='#999999')

        self.after(1, self.update)

    def onclick(self, event):
        pos = 100
        for i in buildings:

            o = 0  # stores the positoin of the button
            flag = False  # whether the building is destroyed
            for _ in ['Open', 'Delete']:
                if 600 < self.x < 750 and pos + self.offset + 50 + o < self.y < pos + 100 + self.offset + o:  # Checks if the mouse is on the button
                    if _ == 'Open':
                        game = Game(i)  # open the game
                        self.destroy()
                    if _ == 'Delete':
                        # Deletes the building
                        buildings.pop(i)
                        with open('buildings.bobfile', 'wb') as bobfile:
                            pickle.dump(buildings, bobfile)
                        flag = True  # The building is destroyed

                o += 75  # update o

            if flag:
                break

            pos += 350  # update pos

        if 500 < self.x < 800 and self.offset + 30 < self.y < self.offset + 80:
            # Create a new building.
            if self.demo:
                game = Game(demo=True)
            else:
                game = Game()
            self.destroy()

    """
This function is called when a key is pressed to do actions.
"""

    def onKey(self, k):
        global buildings
        global coins

        if self.demo:
            if self.demoframe == 0:
                if not (500 < self.x < 800 and self.offset + 30 < self.y < self.offset + 80):
                    return
        # k.keysym is the key that the user has pressed

        if k.keysym == 'Down':
            self.offset -= 10  # scroll down
        if k.keysym == 'Up':
            self.offset += 10  # scroll up

        if k.keysym in ['space', 'Return']:
            self.onclick(None)

    """
This function gets the cost of the buiding by scanning each block.
"""

    def getBuildingCost(self, layers):
        cost = 0
        for i in layers:  # for each layer in the building
            for j in i:  # for each block in the layer
                cost += j.price
        return cost


class Death(tkinter.Canvas):
    def __init__(self):
        super().__init__(width=WIDTH, height=HEIGHT)

        self.pack()
        self.bind_all('<Button-1>', self.onclick)
        self.create_text(500, 250, text='You died. Click anywhere to continue.', font=Font(size=20))

    def onclick(self, e):
        self.destroy()
        game = Thing()



class Game(tkinter.Canvas):
    """
This function gets called when the window is created.
It sets up the buttons and binds to the motion, update and key functions
"""

    def __init__(self, id=None, demo=False):
        global buildings
        super().__init__(width=WIDTH, height=HEIGHT)

        self.demo = demo  # Stores whether it is a demo game
        self.demoframe = 0  # Stores the frame of the demo

        # if there is no id, create a new building otherwise open the building
        if id == None:
            self.id = time.time()
            buildings[self.id] = []

            self.layers = [[]]
            self.level = 1

            self.layers[0].append(Base(0, 0))
            for i in range(200):
                x = random.randint(-100, 100)
                y = random.randint(-100, 100)
                if x == 0 and y == 0:
                    continue
                self.layers[0].append(Gold(x, y))
        else:
            self.id = id
            self.layers = buildings[self.id][0]
            self.level = buildings[self.id][1]

        self.colors = {}  # the position of the colors buttons
        self.blocks_ = {}  # the position of the block buttons
        self.currentlayer = 0  # the current layer that the user is working on.

        self.x = 0  # The positions of the mouse on screen.
        self.y = 0

        # The offset
        self.xoff = 100
        self.yoff = 100

        self.pack()
        self.bind_all('<Button-1>', self.onclick)
        self.bind_all('<Button-2>', self.onmiddleclick)
        self.bind_all('<Button-3>', self.onrightclick)

        self.after(1, self.update)  # run update every 1 millisecond

        self.bind_all('<Motion>', self.on_motion)  # Listen to mouse movement
        self.bind_all('<Key>', self.on_key)  # Listen to key press

        self.color = 'red'  # set the current color
        self.block = None  # set the current block

        self.size = 100  # size for zooming in and zooming out

        self.gui = None
        self.autoupgrade = False

        self.towerlist = ['Tower', 'Wall', 'Base', 'Cannon', 'Gold Digger', 'Wall Healer', 'Spikey Wall', 'Dummy',
                          'Transporter']

        self.lastFrame = time.time()  # store the frames per second
        self.connectedToBase = []

        thread = Thread(target=self.updateNetwork)
        thread.start()

        if not (self.demo):
            self.after(10000, self.night)

    """
This function creates the zombies which try to take over your base
"""

    def spawnZombies(self):
        self.level += 1  # update level
        self.delete('night')  # Delete 'Zombie wave approaching' text

        buildingpositions = [[i.x, i.y] for i in self.layers[0]]
        for i in range(int(self.level ** 1.5)):  # Spawn zombies in random positions
            while True:
                x = random.randint(-50, 50)
                y = random.randint(-50, 50)
                if [x, y] not in buildingpositions:
                    break
            m = Minion(x, y, level=self.level)
            self.layers[0].append(m)

    """
This function gets called every 100 seconds to warn the player
that the zombies are approaching and spawns zombies
"""

    def night(self):
        # Create 'Zombie wave approaching' text
        self.create_text(200, 100, text='Zombie wave approaching', fill='red', tag='night')

        self.after(10000, self.spawnZombies)
        self.after(100000, self.night)  # Night happens every 100 seconds

    """
This function gets called every milisecond to update the elements
in the game.
"""

    def update(self):
        global connections
        connections = []

        # Get frames per second
        delay = time.time() - self.lastFrame
        self.lastFrame = time.time()
        if delay != 0:
            fps = int(1 / delay)
        else:
            fps = '64'

        global coins

        base = False  # if the base is found
        for i in self.layers[0]:
            if i.name.lower() == 'base':
                base = True

        # If the base is not found, the player is dead
        if not base:
            self.destroy()
            game = Death()
            return

        # Auto upgrade
        if self.autoupgrade:
            for tower in self.layers[0]:
                if tower.name in self.towerlist:
                    i = tower
                    if i.level != len(levelcolors):
                        if coins - i.level ** 2 * 100 < 0:
                            pass  # The building is too expensive to upgrade
                        else:
                            coins -= i.level ** 2 * 100
                            i.level += 1

        self.delete('overlay')
        self.delete('block')  # delete everything

        for j in self.layers:
            for i in j:
                i.pre_draw(self, self.size * i.x + self.xoff, self.size * i.y + self.yoff, self.size)

        # draw all of the blocks
        for j in self.layers:
            for i in j:
                if ((self.size * i.x + self.xoff > WIDTH or self.size * i.y + self.yoff > HEIGHT) or (
                        self.size * i.x + self.xoff < 0 or self.size * i.y + self.yoff < 0)):
                    pass
                else:

                    i.draw(self, self.size * i.x + self.xoff, self.size * i.y + self.yoff, self.size)

                i._update(self, self.size * i.x + self.xoff, self.size * i.y + self.yoff, self.size)
                i.update(self, self.size * i.x + self.xoff, self.size * i.y + self.yoff, self.size)

        for j in self.layers:
            for i in j:
                i.post_draw(self, self.size * i.x + self.xoff, self.size * i.y + self.yoff, self.size)

        self.delete('thing')  # dedlete everything

        if self.block is not None and self.block.name == 'Gold Digger':
            x = self.x
            y = self.y
            x = (x - self.xoff) // self.size
            y = (y - self.yoff) // self.size
            good = False
            for block in self.layers[0]:
                if abs(block.x - x) <= 1 and abs(block.y - y) <= 1 and block.name == 'Gold':
                    good = True
                    break
            if not good:
                self.create_rectangle(self.x, self.y, self.x + 300, self.y + 50, tag='thing', outline='', fill='black')
                self.create_text(self.x + 100, self.y + 23, text='''Place the Gold Digger next to 
Gold (the yellow circles)''', tag='thing', fill='red')

        x = self.x
        y = self.y

        if not (0 <= x <= 50 and 70 <= y <= 400):
            # get the selected block
            x = (x - self.xoff) // self.size
            y = (y - self.yoff) // self.size
            x = self.size * x + self.xoff
            y = self.size * y + self.yoff
            self.create_rectangle(x, y, x + self.size, y + self.size,
                                  tag='thing')  # Create rectangle that indicates selected block

        self.delete('thingy')  # delete everything
        self.create_rectangle(0, 30, 50, 470, fill='#000000', tag='thingy')  # create rectangle for block selection
        pos = 60  # stores the position of the button.
        self.colors = {}  # stores the position of the colors.
        for i in []:  # the list of colors
            self.create_rectangle(10, pos, 40, pos + 30, fill=i, outline=i,
                                  tag='thingy')  # create the button of the color
            self.colors[(10, pos, 40, pos + 30)] = i
            if i == self.color and self.block == None:
                self.create_rectangle(10, pos, 40, pos + 30, outline='#00ffff',
                                      tag='thingy')  # create an outline of the button if it is the current color.
            pos += 40  # update pos

        self.blocks_ = {}  # stores the position of the buttons for the blocks.

        minion = Minion(99999999999, 99999999999)
        minion.level = 999999999
        for i in [Wall(99999999999, 99999999999), Cannon(9999999999999, 9999999999999), minion,
                  GoldDigger(9999999999, 9999999), WallHealer(99999999999, 99999999999),
                  SpikeyWall(9999999999, 9999999999),
                  Dummy(99999999999, 999999999), Transporter(999999999999, 999999999999)]:  # the list of blocks
            i.draw(self, 10, pos, 30)  # draw the block.
            self.blocks_[(10, pos, 40, pos + 30)] = i
            if self.block != None and i.name == self.block.name:
                self.create_rectangle(10, pos, 40, pos + 30, outline='#00ffff',
                                      tag='thingy')  # create an outline of the button if it is the current block.
            pos += 40  # update pos

        self.create_text(25, 40, text='Towers', tag='thingy', fill='white')  # create the text that says "Colors".

        for i in self.colors:
            if i[0] <= self.x <= i[2] and i[1] <= self.y <= i[3]:
                # Create a white outline if the mouse is on a button.
                self.create_rectangle(i[0], i[1], i[2], i[3], outline='white', tag='thingy')

        for i in self.blocks_:
            if i[0] <= self.x <= i[2] and i[1] <= self.y <= i[3]:
                # Create a white outline if the mouse is on a button.
                self.create_rectangle(i[0], i[1], i[2], i[3], outline='white', tag='thingy')

        self.delete('layerselection')  # delete everything
        self.create_text(1000 - 60, 10, text='Current layer: ' + str(self.currentlayer), tag='layerselection')

        # creates the layer selection buttons
        if 940 < self.x < 965 and 35 < self.y < 60:
            # up button
            self.create_rectangle(965, 35, 940, 60, tag='layerselection', fill='black', outline='red')
        else:
            self.create_rectangle(965, 35, 940, 60, tag='layerselection', fill='black')

        if 940 < self.x < 965 and 75 < self.y < 90:
            # down button
            self.create_rectangle(965, 70, 940, 90, tag='layerselection', fill='black', outline='red')
        else:
            self.create_rectangle(965, 70, 940, 90, tag='layerselection', fill='black')

        self.create_text(952, 48, text='^', fill='white', tag='layerselection')  # up
        self.create_text(952, 78, text='\/', fill='white', tag='layerselection')  # down

        self.delete('coins')  # delete everything
        self.create_rectangle(420, 0, 580, 50, tag='coins', fill='black')  # create rectangle for coins
        self.create_text(500, 25, text=f'Coins: {coins}', tag='coins', fill='white')  # Create text that displays coins
        # self.create_text(500, 50, text=f'Total cost: {self.getBuildingCost()}', tag='coins', fill='white') # create text that displays building cost
        # if self.getBuildingCost() > coins:
        #    self.create_text(500, 65, text='Overpriced!', tag='coins', fill='red') # create text that says overpriced if the building is overpric3ed

        self.delete('save')  # delete everything
        # creates the button that says "save building & quit"
        if 100 < self.x < 300 and 0 < self.y < 50:
            self.create_rectangle(100, 0, 300, 50, tag='save', fill='black', outline='red')
        else:
            self.create_rectangle(100, 0, 300, 50, tag='save', fill='black')
        self.create_text(200, 25, text='Save building & quit', fill='white', tag='save')

        self.delete('demo')
        if self.demo:
            # Demo frame 0: Block selection
            if self.demoframe == 0:
                self.create_text(500, 250, text='''Select a cannon from the blocks!
It is the circle with the white line on it.''', tag='demo')
                self.create_line(400, 250, 100, 250, tag='demo')
                self.create_line(100, 250, 150, 300, tag='demo')
                self.create_line(100, 250, 150, 200, tag='demo')
            # Demo frame 1: How to place blocks
            if self.demoframe == 1:
                self.create_text(500, 250, text='''Click on the screen to place cannons!
These cannons will shoot balls at the zombies and harm them.
Press space to continue.''', tag='demo')
            # Demo frame 2: Place 7 cannons
            if self.demoframe == 2:
                self.create_text(500, 100, text=f'''Place 7 cannons
Cannons placed: {self.getBlockCount()}''', tag='demo')
                if self.getBlockCount() >= 7:
                    self.demoframe += 1
            # Demo frame 3: Gold diggers
            if self.demoframe == 3:
                self.create_text(500, 100, text=f'''Now place 7 gold diggers.
These gold diggers can dig for coins.
First select the block with two dollar signs on it. ($$)
Place these gold diggers next to a Gold block (They are yellow circles)
Gold diggers placed: {self.getBlockCount() - 7}''', tag='demo')
                if self.getBlockCount() >= 14:
                    self.demoframe += 0.25
            # Demo frame 3.25: Walls
            if self.demoframe == 3.25:
                self.create_text(500, 100, text=f'''Now place 7 walls.
These walls have lots of health and
protect you from zombies.
The block looks like a circle with a blue outline.
Walls placed: {self.getBlockCount() - 14}''', tag='demo')
                if self.getBlockCount() >= 21:
                    self.demoframe += 0.25
            # Demo frame 3.5: Upgrades
            if self.demoframe == 3.5:
                self.create_text(500, 100, text=f'''Upgrade all of your buildings once.
Press U on a building to upgrade it.
Upgrading makes the buildings have more health and produce more.
Upgraded buildings: {len([b for b in self.layers[0] if b.level >= 2])}''', tag='demo')
                if len([b for b in self.layers[0] if b.level >= 2]) == len(self.layers[0]):
                    self.demoframe += 0.5
            # Demo frame 4: zombie wave
            if self.demoframe == 4:
                self.create_text(500, 250, text='Now you will need to survive the zombie wave.', tag='demo')
            # Demo frame 5: the zombie wave
            if self.demoframe == 5:
                if self.level > self.demolevel and len([b for b in self.layers[0] if b.name == 'Minion']) == 0:
                    self.demoframe += 1
            # Demo frame 6: Save & quit
            if self.demoframe == 6:
                self.create_text(500, 250, text='Click on this button to save and quit', tag='demo')
                self.create_line(500, 240, 200, 70, tag='demo')
                self.create_line(200, 70, 250, 70, tag='demo')
                self.create_line(200, 70, 200, 120, tag='demo')

        self.delete('fps')
        self.create_text(100, 50, text=f'FPS: {fps}', fill='red', tag='fps')

        # Show the gui on top of everything
        self.delete('gui')
        if (self.gui != None):
            self.create_rectangle(100, 100, 900, 400, fill='black', tag='gui')
            self.create_text(500, 130, text=self.gui.name, fill='white', font=Font(size=30), tag='gui')

            self.create_text(500, 250, text=f"""Health: {self.gui.health}/{self.gui.maxHealth}
Level: {self.gui.level}
Upgrade cost: {self.gui.level ** 2 * 100}

Controls: Sell: s; Upgrade: u

Press space or Return to continue.""", fill='white', tag='gui')

        self.after(1, self.update)  # run update every 1 millisecond

    def updateDemoFrame(self):
        self.demoframe += 1

    def getBuildingCost(self):
        cost = 0
        # for every layer in the building
        for i in self.layers:
            # for every block in the layer
            for j in i:
                cost += j.price  # add price of the block to the cost
        return cost

    """
This function gets how many blocks are in the building.
"""

    def getBlockCount(self):
        count = 0
        # for every layer in the building
        for i in self.layers:
            # for every block in the layer
            for j in i:
                count += 1  # Increment count
        return count

    """
This function is called when the mouse moves to update the mouse
position.
"""

    def on_motion(self, e):
        # update the mouse positoin on screen
        self.x = e.x
        self.y = e.y

    connectedToBase = []

    def EVALUATE(self, posX: int, posY: int, lastPositions: list[list[int]], positions: list[list[int]]):
        nextPositions = [[int(x), int(y)] for x, y in positions if
                         abs(x - posX) < 4 and abs(y - posY) < 4 and [x,
                                                                      y] not in lastPositions and not(x == posX and y == posY)]
        if len(nextPositions) == 0:
            return

        isTransporter = False
        for block in self.layers[0]:
            if block.x == posX and block.y == posY and block.name in ['Transporter', 'Base']:
                isTransporter = True

        for pos in nextPositions:
            if pos in positions and pos not in self.connectedToBase:
                self.connectedToBase.append(pos)
            updatedLastPositions = lastPositions[:]
            updatedLastPositions.append(pos)
            if isTransporter:
                self.EVALUATE(pos[0], pos[1], updatedLastPositions, positions)

    def updateNetwork(self):
        self.connectedToBase = []
        self.EVALUATE(0, 0, [],
                      [[block.x, block.y] for block in self.layers[0] if block.name in ['Gold Digger', 'Transporter']])

        print(self.connectedToBase)

        for b in self.layers[0]:
            if b.name == 'Gold Digger':
                b.connected = [b.x, b.y] in self.connectedToBase

        # for b in self.layers[0]:
        #     if b.name == 'Gold Digger':
        #         b.connected = (
        #             GoldDigger.EVALUATE(b.x, b.y, [],
        #                                 [[block.x, block.y] for block in self.layers[0] if
        #                                  block.name == 'Gold Digger' or block.name == 'Base' or block.name == 'Transporter']))

    """
Called when the user clicks.
Places a tower
"""

    def onclick(self, event):
        global coins
        if self.demo:
            if self.demoframe == 0:
                if not (0 < self.x < 30 and 50 < self.y < 470):
                    return
            if self.demoframe == 1:
                self.demoframe += 1
                return
            if self.demoframe == 3:
                pass
            if self.demoframe == 3.5:
                pass
            if self.demoframe == 4:
                self.demoframe += 1
                self.after(1, self.night)
                self.demolevel = self.level
                return
            if self.demoframe == 6:
                if not (100 < self.x < 300 and 0 < self.y < 50):
                    return

        if (self.gui != None):
            self.gui = None
            return

        # gets the block position that is selected.
        x = self.x
        y = self.y
        x = (x - self.xoff) // self.size
        y = (y - self.yoff) // self.size

        flag = False  # flag stores if the block placement should be cancelled.
        for i in self.colors:
            # if the user clicked the button that selects colors
            if i[0] <= self.x <= i[2] and i[1] <= self.y <= i[3]:
                flag = True
                self.color = self.colors[i]
                self.block = None
                if self.demoframe == 0:
                    self.demoframe += 1
        for i in self.blocks_:
            # if the user clicked the button that selects blocks
            if i[0] <= self.x <= i[2] and i[1] <= self.y <= i[3]:
                flag = True
                self.block = self.blocks_[i]
                self.color = None
                if self.demoframe == 0:
                    self.demoframe += 1

        # Layer Selection
        if 940 < self.x < 965 and 35 < self.y < 60:  # go up 1 layer
            flag = True
            y = self.currentlayer + 1
            if y == len(self.layers) or y < 0:
                pass
            else:
                self.currentlayer += 1
                if self.demo and self.demoframe == 3:
                    self.demoframe += 1

        if 940 < self.x < 965 and 75 < self.y < 90:  # go down 1 layer
            flag = True
            y = self.currentlayer - 1
            if y == len(self.layers) or y < 0:
                pass
            else:
                self.currentlayer -= 1

        if 100 < self.x < 300 and 0 < self.y < 50:  # Save building & quit
            flag = True
            global buildings
            buildings[self.id] = [self.layers, self.level]

            # Saves the building to a file using pickle
            with open('buildings.bobfile', 'wb') as bobfile:
                pickle.dump(buildings, bobfile)

            if self.demo and self.demoframe == 6:
                game = InstructionsFinish()
            else:
                game = Thing()
            self.destroy()

        if not flag:
            flag2 = False  # stores if the block placement should be cancelled if the block already exists or it is eraser
            for i in self.layers[self.currentlayer]:
                if i.x == x and i.y == y:
                    flag2 = True
                    break
            if not flag2:
                if self.block == None:
                    self.layers[self.currentlayer].append(Block(self.color, x, y))
                else:
                    check = True
                    if self.block.name == 'Gold Digger':
                        x = self.x
                        y = self.y
                        x = (x - self.xoff) // self.size
                        y = (y - self.yoff) // self.size
                        good = False
                        for block in self.layers[0]:
                            if abs(block.x - x) <= 1 and abs(block.y - y) <= 1 and block.name == 'Gold':
                                good = True
                                break
                        if not good:
                            check = False
                    if check:
                        # Place a copy of the block
                        if coins - self.block.price >= 0:
                            coins -= self.block.price
                            block = copy.deepcopy(self.block)
                            block.x = x
                            block.y = y
                            self.layers[self.currentlayer].append(block)
                            thread = Thread(target=self.updateNetwork)
                            thread.start()

    """
Called when the user right clicks.
Displays information about a building.
"""

    def onrightclick(self, event):
        x = self.x
        y = self.y
        x = (x - self.xoff) // self.size
        y = (y - self.yoff) // self.size
        for i in self.layers[0]:
            if i.x == x and i.y == y:
                # If the building is a tower, display information about the buiding
                if i.name in self.towerlist:
                    self.gui = i

    """
Called when the user middle clicks.
Upgrades the buiding.
"""

    def onmiddleclick(self, event):
        global coins
        x = self.x
        y = self.y
        x = (x - self.xoff) // self.size
        y = (y - self.yoff) // self.size

        tower = None
        if self.gui != None:
            tower = self.gui
        else:
            for i in self.layers[0]:
                if i.x == x and i.y == y:
                    # If the building is a tower, upgrade the building
                    if i.name in self.towerlist:
                        tower = i
        if tower != None:
            i = tower
            if i.level != len(levelcolors):
                if coins - i.level ** 2 * 100 < 0:
                    pass  # The building is too expensive to upgrade
                else:
                    coins -= i.level ** 2 * 100
                    i.level += 1

    """
This function is called when a key is pressed to do actions.
"""

    def on_key(self, e):

        global coins
        # if the user is doing the demonstration, disable all buttons

        if e.keysym == 'Right':
            self.xoff -= 10
        if e.keysym == 'Left':
            self.xoff += 10
        if e.keysym == 'Up':
            self.yoff += 10
        if e.keysym == 'Down':
            self.yoff -= 10
        if e.keysym == 'minus':
            self.size *= 9 / 10
            self.xoff *= 9/10
            self.yoff *= 9/10
        if e.keysym == 'equal':
            self.size *= 10 / 9
            self.xoff *= 10/9
            self.yoff *= 10/9
        if e.keysym in ['space', 'Return']:
            self.onclick(None)

        if e.keysym.lower() == 'u':
            self.onmiddleclick(None)

        if e.keysym.lower() == 's':  # Sell the building
            x = self.x
            y = self.y
            x = (x - self.xoff) // self.size
            y = (y - self.yoff) // self.size

            tower = None
            if self.gui != None:
                tower = self.gui
                self.gui = None
            else:
                for i in self.layers[0]:
                    if i.x == x and i.y == y:
                        if i.name in self.towerlist and i.name != 'Base' and i.name != 'Gold':
                            tower = i
            if tower != None:
                i = tower
                self.layers[0].remove(i)
                coins += i.price + (i.level - 1) ** 2 * 100  # Add price and upgrade price to coins
                thread = Thread(target=self.updateNetwork)
                thread.start()

        if e.keysym.lower() == 'i':
            self.onrightclick(None)


class Block:
    def __init__(self, x, y):
        self.x = x  # the x position of the block.
        self.y = y  # the y position of the block.
        self.name = ""  # the name of the block.
        self.price = 100  # the price of the block.

    def pre_draw(self, canvas, x, y, size):
        pass

    def post_draw(self, canvas, x, y, size):
        pass

    def draw(self, canvas, x, y, size):
        # Draw the block.
        canvas.create_rectangle(x, y, x + size, y + size, fill=self.color, outline=self.color, tag='block')

    def update(self, canvas, x, y, size):
        pass


characters = ['00', '11', '22', '33', '44', '55', '66', '77', '88', '99', 'AA', 'BB', 'CC', 'DD', 'EE', 'FF']
levelcolors = [f'#{characters[i]}{(characters[len(characters) - 1 - i]) * 2}' for i in range(len(characters))]


class Tower(Block):
    def __init__(self, x, y, maxHealth):
        self.x = x
        self.y = y
        self.baseHealth = maxHealth
        self.maxHealth = maxHealth
        self.health = maxHealth
        self.name = 'Tower'
        self.price = 0
        self.level = 1

    def drawCircle(self, canvas, x, y, size, offset):
        # This is the inside of the tower
        canvas.create_oval(x + offset, y + offset, x + size - offset, y + size - offset, tag='block', fill='black')

    def draw(self, canvas, x, y, size):
        offset = size / 5
        self.drawCircle(canvas, x, y, size, offset)

        # This is the arc that displays the health of the building relative to the maximum health
        canvas.create_arc(x + offset, y + offset, x + size - offset, y + size - offset, tag='block',
                          outline=levelcolors[self.level - 1], start=90, extent=360 * self.health / self.maxHealth - 1,
                          style='arc', width=size / 20)

    def _update(self, canvas, x, y, size):
        # Natural regeneration
        self.maxHealth = self.level ** 2 * self.baseHealth
        self.health += 0.1 * self.level ** 2
        if self.health > self.maxHealth:
            self.health = self.maxHealth

        if self.health < 0:  # If the building is destroyed, remove the building
            canvas.layers[0].remove(self)


class Wall(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, 250)
        self.name = 'Wall'
        self.price = 100

    def draw(self, canvas, x, y, size):
        found = False

        try:
            # Draw the bonds between the walls
            for i in canvas.layers[0]:
                if i == self:
                    found = True
                if found and i.x - self.x in [-1, 0, 1] and i.y - self.y in [-1, 0,
                                                                             1] and i != self and i.name == self.name:
                    canvas.create_line(x + size / 2, y + size / 2, x + size / 2 + (i.x - self.x) * size,
                                       y + size / 2 + (i.y - self.y) * size, tag='block', width=size / 3)
        except:
            pass

        super().draw(canvas, x, y, size)


class WallHealer(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, 50)
        self.name = 'Wall Healer'
        self.price = 100

    def pre_draw(self, canvas, x, y, size):
        try:
            # Draw the bonds between the walls
            for i in canvas.layers[0]:
                if i.x - self.x in [-2, -1, 0, 1, 2] and i.y - self.y in [-2, -1, 0, 1, 2] and i != self and i.name in [
                    'Wall', 'Spikey Wall']:
                    if i.health < i.maxHealth:
                        canvas.create_line(x + size / 2, y + size / 2, x + size / 2 + (i.x - self.x) * size,
                                           y + size / 2 + (i.y - self.y) * size, tag='block', width=size / 20,
                                           fill='red')
                    else:
                        canvas.create_line(x + size / 2, y + size / 2, x + size / 2 + (i.x - self.x) * size,
                                           y + size / 2 + (i.y - self.y) * size, tag='block', width=size / 20,
                                           fill='black')
        except:
            pass

    def draw(self, canvas, x, y, size):

        super().draw(canvas, x, y, size)
        canvas.create_text(x + size / 2, y + size / 2, fill='white', text='+', tag='block',
                           font=Font(size=int(size / 5)))

    def update(self, canvas, x, y, size):
        for i in canvas.layers[0]:
            if i.x - self.x in [-2, -1, 0, 1, 2] and i.y - self.y in [-2, -1, 0, 1, 2] and i != self and i.name in [
                'Wall', 'Spikey Wall']:
                i.health += 0.1 * self.level ** 2
                if (i.health > i.maxHealth):
                    i.health = i.maxHealth


class SpikeyWall(Wall):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.name = 'Spikey Wall'
        self.price = 200

    def draw(self, canvas, x, y, size):
        super().draw(canvas, x, y, size)

        for add in range(5):
            t = time.time() + add * 60
            cx = math.sin(t * 5) * size / math.pi + x + size / 2
            cy = math.cos(t * 5) * size / math.pi + y + size / 2
            dx = math.sin(t * 5 + 0.6) * size / math.pi + x + size / 2
            dy = math.cos(t * 5 + 0.6) * size / math.pi + y + size / 2
            ex = math.sin(t * 5 + 0.3) * size / 2.5 + x + size / 2
            ey = math.cos(t * 5 + 0.3) * size / 2.5 + y + size / 2

            canvas.create_polygon(cx, cy, dx, dy, ex, ey,
                                  fill='red', tag='block')

    def update(self, canvas, x, y, size):
        super().update(canvas, x, y, size)
        for i in canvas.layers[0]:
            if i.name == 'Minion':
                e = (i.x - self.x) ** 2 + (i.y - self.y) ** 2
                if e < 1:
                    i.health -= 5 * self.level ** 2


class Base(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, 1000)
        self.name = 'Base'
        self.price = 0

    def draw(self, canvas, x, y, size):
        super().draw(canvas, x, y, size)

        # Draw the house shape
        unit = size / 5
        canvas.create_line(x + size / 2 - unit, y + size / 2, x + size / 2, y + size / 2 - unit, tag='block',
                           fill='white', width=size / 33)
        canvas.create_line(x + size / 2, y + size / 2 - unit, x + size / 2 + unit, y + size / 2, tag='block',
                           fill='white', width=size / 33)
        canvas.create_line(x + size / 2 - unit, y + size / 2, x + size / 2 + unit, y + size / 2, tag='block',
                           fill='white', width=size / 33)
        canvas.create_line(x + size / 2 - unit + size / 15, y + size / 2, x + size / 2 - unit + size / 15,
                           y + size / 2 + size / 5, tag='block', fill='white', width=size / 33)
        canvas.create_line(x + size / 2 + unit - size / 15, y + size / 2, x + size / 2 + unit - size / 15,
                           y + size / 2 + size / 5, tag='block', fill='white', width=size / 33)


class Cannon(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, 50)
        self.name = 'Cannon'
        self.price = 100
        self.lastTime = 0
        self.delay = 1

    def draw(self, canvas, x, y, size):
        super().draw(canvas, x, y, size)
        canvas.create_line(x + size / 2, y + size / 2, x + size / 2 + size / 3, y + size / 2, fill='white', tag='block',
                           width=size / 10)

    def update(self, canvas, x, y, size):

        if not (time.time() - self.lastTime > self.delay / self.level ** 0.7):
            return

        self.lastTime = time.time()

        def comp(x):
            if x.name == 'Minion' or x.name == 'Dummy':
                e = (x.x - self.x) ** 2 + (x.y - self.y) ** 2
                return e if e < self.level + 9 else 9999999999

            return 999999999

        # Gets the minion with the minimum distance to the cannon.
        target = min(canvas.layers[0], key=comp)

        # Spawn the cannon ball
        if target.name == 'Minion' or target.name == 'Dummy':
            cannon = Cannonball(self.x, self.y, target.x, target.y)
            cannon.level = self.level
            canvas.layers[0].append(cannon)


class Cannonball(Tower):
    def __init__(self, x, y, targetX, targetY):
        super().__init__(x, y, 100)
        self.name = 'Cannonball'
        self.price = 0
        self.targetX = targetX
        self.targetY = targetY

    def draw(self, canvas, x, y, size):
        unit = size / 3
        canvas.create_oval(x + unit, y + unit, x + size - unit, y + size - unit, fill='#555555', tag='block')

    def update(self, canvas, x, y, size):
        lastx = self.x
        lasty = self.y
        xdiff = self.targetX - self.x
        ydiff = self.targetY - self.y
        self.x += xdiff / 50 * self.level
        self.y += ydiff / 50 * self.level  # Moves the cannonball towards the target.

        if abs(self.x - self.targetX) < 0.1 and abs(self.y - self.targetY) < 0.1:
            canvas.layers[0].remove(self)

        for i in canvas.layers[0]:
            if i.name not in ['Minion', 'Dummy']:
                continue
            # Damages the minion if the cannonball touches it
            if abs(i.x - self.x) <= 0.5 and abs(i.y - self.y) <= 0.5:
                i.health -= self.level ** 2 * 50
                self.x = lastx
                self.y = lasty
                try:
                    canvas.layers[0].remove(self)
                except:
                    pass


class Minion(Tower):
    def __init__(self, x, y, level=1):
        super().__init__(x, y, 100)
        self.name = 'Minion'
        self.price = 0
        self.level = level
        self.baseHealth = self.level * 100
        self.maxHealth = self.level * self.baseHealth
        self.health = self.maxHealth

    def draw(self, canvas, x, y, size):
        unit = size / 4
        canvas.create_oval(x + unit, y + unit, x + size - unit, y + size - unit, fill='#222222', tag='block')

        diff = size - 2 * unit
        if self.health > 0:
            diff *= self.health / self.maxHealth
        else:
            diff = 0
        canvas.create_line(x + unit, y + unit + size / 1.5, x + size - unit, y + unit + size / 1.5, fill='#555555',
                           tag='block', width=size / 25)
        canvas.create_line(x + unit, y + unit + size / 1.5, x + unit + diff, y + unit + size / 1.5, fill='red',
                           tag='block', width=size / 25)

    def _update(self, canvas, x, y, size):
        # Natural regeneration
        self.maxHealth = self.level * self.baseHealth
        self.health += 0.01 * self.level ** 2
        if self.health > self.maxHealth:
            self.health = self.maxHealth

    def update(self, canvas, x, y, size):
        self.baseHealth = self.level * 100

        lastx = self.x
        lasty = self.y
        xdiff = -self.x
        ydiff = -self.y
        self.x += xdiff / 200
        self.y += ydiff / 200  # Moves the minion towards the base

        for i in canvas.layers[0]:
            if i.name in ['Minion', 'Cannonball', 'Dummy', 'Gold']:
                continue
            if abs(i.x - self.x) <= 0.5 and abs(i.y - self.y) <= 0.5:
                # Damages the building next to it
                i.health -= 0.5 * self.level
                self.x = lastx
                self.y = lasty

        if self.health < 0:
            canvas.layers[0].remove(self)


class Dummy(Minion):
    def __init__(self, x, y, level=1):
        super().__init__(x, y, 100)
        self.name = 'Dummy'
        self.price = 0
        self.level = level
        self.baseHealth = self.level ** 2 * 100
        self.maxHealth = self.level * self.baseHealth
        self.health = self.maxHealth

    def update(self, canvas, x, y, size):
        self.baseHealth = self.level ** 2 * 100


connections = []


class GoldDigger(Tower):
    connected = False

    def __init__(self, x, y):
        super().__init__(x, y, 100)
        self.name = 'Gold Digger'
        self.price = 100
        self.lastAction = time.time()
        self.connected = False

    def post_draw(self, canvas, x, y, size):
        if not self.connected:
            if x < canvas.x < x + size and y < canvas.y < y + size:
                canvas.create_rectangle(canvas.x, canvas.y, canvas.x + 200, canvas.y + 40, fill='#000000',
                                        outline='red', tag='overlay')
                canvas.create_text(canvas.x + 100, canvas.y + 20, fill='red',
                                   text='Connect this Gold Digger to\nthe base with a Transporter', tag='overlay')

    def pre_draw(self, canvas, x, y, size):
        for block in canvas.layers[0]:
            if abs(block.x - self.x) <= 1 and abs(block.y - self.y) <= 1 and block.name == 'Gold':
                canvas.create_line(x + size / 2, y + size / 2, x + size * (block.x - self.x) + size / 2,
                                   y + size * (block.y - self.y) + size / 2, tag='block', width=size / 3, fill='red')

        for block in canvas.layers[0]:
            if (block.name == 'Transporter' or block.name == 'Base' or block.name == 'Gold Digger') and abs(
                    block.x - self.x) < 4 and abs(block.y - self.y) < 4:
                color = '#DDDDDD'

                canvas.create_line(x + size / 2, y + size / 2, x + size / 2 + size * (block.x - self.x),
                                   y + size / 2 + size * (block.y - self.y), tag='block', fill=color, width=size / 50)

    def draw(self, canvas, x, y, size):
        super().draw(canvas, x, y, size)
        canvas.create_text(x + size / 2, y + size / 2, fill='white' if self.connected else 'red', text='$$',
                           tag='block',
                           font=Font(size=int(size / 9)))

    @staticmethod
    def EVALUATE(posX: int, posY: int, lastPositions: list[list[int]], positions: list[list[int]]) -> bool:
        global connections
        poss = [[(a), (b)] for a, b in positions if
                abs(a - posX) < 4 and abs(b - posY) < 4 and not ([a, b] in lastPositions)]
        if len(poss) in [0, 1]:
            return False
        if [0, 0] in poss:
            lastPositions.append([0, 0])
            for n in range(len(lastPositions) - 1):
                connections.append([lastPositions[n], lastPositions[n + 1]])
            return True
        for x, y in poss:
            if abs(posX - x) < 4 and abs(posY - y) < 4:
                if ([x, y] in lastPositions) or (x == posX and y == posY):
                    continue
                ls = lastPositions[:]
                ls.append([posX, posY])
                if GoldDigger.EVALUATE(x, y, ls, positions):
                    return True
        return False

    def update(self, canvas, x, y, size):
        global coins
        if time.time() - self.lastAction < 1:
            return
        self.lastAction = time.time()
        if self.connected:
            coins += 10 * self.level


class Gold(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, 0)
        self.name = 'Gold'

    def draw(self, canvas, x, y, size):
        canvas.create_oval(x, y, x + size, y + size, fill='#DDCC00', outline='', tag='block')

    def update(self, canvas, x, y, size):
        return


class Transporter(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, 10)
        self.name = 'Transporter'

    def pre_draw(self, canvas, x, y, size):
        for block in canvas.layers[0]:
            if (block.name == 'Transporter' or block.name == 'Base' or block.name == 'Gold Digger') and abs(
                    block.x - self.x) < 4 and abs(block.y - self.y) < 4:
                color = 'black'

                canvas.create_line(x + size / 2, y + size / 2, x + size / 2 + size * (block.x - self.x),
                                   y + size / 2 + size * (block.y - self.y), tag='block', fill=color, width=size / 20)

    def draw(self, canvas, x, y, size):
        canvas.create_oval(x + size / 3, y + size / 3, x + 2 * size / 3, y + 2 * size / 3, tag='block', fill='gray',
                           outline='')
        canvas.create_arc(x + size / 3, y + size / 3, x + 2 * size / 3, y + 2 * size / 3, tag='block', outline='black',
                          start=90, extent=360 * self.health / self.maxHealth)


def getData():
    global coins
    global buildings
    # Uses pickkle library to get the files
    coins = 0
    if not os.path.isfile('coins.bobfile'):
        with open('coins.bobfile', 'wb') as bobfile:  # if the file doesn't exisrt
            pickle.dump(1000, bobfile)
    with open('coins.bobfile', 'rb') as bobfile:
        coins = pickle.load(bobfile)

    buildings = {}
    if not os.path.isfile('buildings.bobfile'):
        with open('buildings.bobfile', 'wb') as bobfile:  # if the file doesn't exist
            pickle.dump({}, bobfile)
    with open('buildings.bobfile', 'rb') as bobfile:
        buildings = pickle.load(bobfile)


if __name__ == '__main__':
    # Get the data from the files.

    coins = 0
    buildings = {}
    getData()

    # Starts the window.
    root = tkinter.Tk()
    root.title('Hello')

    w = Thing()
    root.mainloop()

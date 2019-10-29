# -*- coding: utf-8 -*-

"""

COLOUR TEST SCRIPT

COGNITION AND COMMUNICATION CLASS ON LANGUAGE & THOUGHT

@author: Marlene Staib 2016

Modified by Kristian Tylén 2018 

"""



#import

from psychopy import visual, core, event, gui, monitors

import random, itertools, os, math

import numpy as np

import pandas as pd





"""VARIABLES AND STUFF"""



# Monitor parameters

#MON_DISTANCE = 60  # Distance between subject's eyes and monitor

#MON_WIDTH = 50  # Width of monitor in cm

#MON_SIZE = [1600, 900]  # Pixel-dimensions of monitor



# define dialogue box (important that this happens before you define window)

popup = gui.Dlg(title = "The Danish Pinks")

popup.addField("Participant ID: ") 

popup.addField("Is Danish your native language?: ", choices=["Yes", "No", "It's complicated" ])

popup.show()

if popup.OK: # To retrieve data from popup window

    ID = popup.data

elif popup.Cancel: # To cancel the experiment if popup is closed

    core.quit()



#window and stuff

#my_monitor = monitors.Monitor('testMonitor', width=MON_WIDTH)

#my_monitor.setSizePix((MON_SIZE)) #change this, dpending on monitor

win = visual.Window( fullscr=True, allowGUI=False, color='black') #monitor='testMonitor', size=MON_SIZE, units='norm',

mouse = event.Mouse(visible=True, newPos=[0,0], win=win)

win.mouseVisible = False

clock = core.Clock()  

trial = 0    #will get incremented on every trial



#Folder for writing the trials/create folder if it does not exist

SAVE_FOLDER = "Colour_Test_Data"

if not os.path.exists(SAVE_FOLDER):

    os.makedirs(SAVE_FOLDER)



# define panda with information

columns = ['subject', 'danish', 'trial', 'colour1', 'colour2', 'col1_name', 'col2_name', 'colour_distance', 'category', 'accuracy', 'rt']

index = np.arange(0)

DATA = pd.DataFrame(columns=columns, index = index)





#Stimuli

#instructions

text = visual.TextStim(win, units='norm', height = .06, pos= [0,0.1], wrapWidth=999)



#for colour choice trials

col1_stim = visual.Rect(win, units= "norm", width=0.2, height=(1.6/4.5), pos = [-0.5,0.3])

col2_stim = visual.Rect(win, units= "norm", width=0.2, height=(1.6/4.5), pos = [0.5,0.3])

col3_stim = visual.Rect(win, units= "norm", width=0.2, height=(1.6/4.5), pos = [0,-0.3])

COLOURS = []

for i in range(10):

    x = 1

    y = -1+((.75/10)*i)

    z = -1+((1.5/10)*i)

    COLOURS.append([x,y,z])

colour_pairs = [x for x in itertools.permutations(COLOURS, 2)]



#for colour naming trials

colour_stim = visual.Rect(win, units= "norm", width=0.3, height=(0.3*8/4.5), pos = [0, 0.2])

button1 = visual.Rect(win, units= "norm", width=0.2, height=0.2, pos = [-0.4, -0.5])

button2 = visual.Rect(win, units= "norm", width=0.2, height=0.2, pos = [0.4, -0.5])

text_red = visual.TextStim(win, text="red", units='norm', height = .06, pos= [-0.4,-0.5], wrapWidth=999)

text_pink = visual.TextStim(win, text="pink", units='norm', height = .06, pos= [0.4,-0.5], wrapWidth=999)





#Texts

welcome = u"""

Welcome to the experiment! And thank you for being here. In this experiment, you

will have to decide, which colours match. On each trial, you will be shown a pair

of colours (top of the screen). Below, you will see a third colour that matches

either the left or right colour from the top. Pick out the correct colour (pressing

the "left" or "right" arrow key) as quickly as possible, while being also as accurate

as possible. Hit "Enter" when you are ready to get started.

"""



intermezzo = u"""

You may take a short break. Hit "Enter" when you are ready to continue.

"""



end_matching = u"""

This is the end of the colour matching task. Now, we would like you to label

the colours for us, and then you are done. For each colour, select the colour 

term that you would (rather) use to describe this colour (using the arrow keys).

Hit "Enter" when you would like to start.

"""



end = u"""

This is the end of the Experiment.

Thank you very much for your participation.

"""





"""FUNCTIONS"""



#display info text and wait for key press

def info(string, end = False):

    text.text = string

    text.draw()

    win.flip()

    if end == True:

        keys = ['escape', 'p']

    else:

        keys = ['return', 'escape']

    key=event.waitKeys(keyList=keys)[0]

    if key == 'escape':

        core.quit()





#colour choice trials

def choice_trial(colours):

    #prepare

    global trial

    trial +=1

    test_col = random.choice(colours)

    col1_stim.setFillColor(colours[0])

    col2_stim.setFillColor(colours[1])

    col3_stim.setFillColor(test_col)

    #draw stuff to visual buffer and flip the window

    col1_stim.draw()

    col2_stim.draw()

    col3_stim.draw()

    t_start = win.flip()



    #record keypresses and time

    key, t_answer = event.waitKeys(keyList=["right", "left", "escape"], timeStamped=True)[0]

    if key == "right":

        answer = 1 #this way we can index the colour in the list from which it comes

    elif key == "left":

        answer = 0

    elif key == "escape":

        core.quit()



    #record accuracy and RT

    accuracy = 1 if answer == colours.index(test_col) else 0

    rt = (t_answer - t_start)*1000 #record rt in ms

    colour_distance_vector = [a - b for a, b in zip(colours[0], colours[1])]

    colour_dist = math.sqrt(math.pow(abs(colour_distance_vector[0]),2)+math.pow(abs(colour_distance_vector[2]),2)) #do the whole pythagoras thing. use absolute values to avoid negative numbers

    return accuracy, rt, colour_dist

    







#colour naming trials

def naming_trial(colour):

    colour_stim.setFillColor(colour)

    answer_pos = None

    #draw & present stimuli

    colour_stim.draw()

    button1.draw()

    button2.draw()

    text_pink.draw()

    text_red.draw()

    win.flip()

    #record choice

    key=event.waitKeys(keyList=["right", "left", "escape"])[0]

    if key == "right":

        answer = "pink"

    elif key == "left":

        answer = "red"

    elif key == "escape":

        core.quit()

    return answer









"""Run the experiment"""



#say hello

info(welcome)



#run the colour matching trials

for rep in range(2): #repeat 2 times

    random.shuffle(colour_pairs)

    for colour_pair in colour_pairs:

        outcome = choice_trial(colour_pair)

        #record variables in dataframe

        DATA = DATA.append({'subject': ID[0], 'danish': ID[1], 'trial': trial, 'colour1':str(colour_pair[0]), 'colour2':str(colour_pair[1]), 'colour_distance': outcome[2], 'accuracy': outcome[0], 'rt': outcome[1]}, ignore_index=True)

        if trial % 10 == 0 and not trial % 180 == 0: #on every 10th trial, let them have a little break

            info(intermezzo)

        # break between trials

        win.flip()

        core.wait(0.5)

info(end_matching)





#create a dictionary of the colour values and names (by running naming trials)

colour_dict = {}

random.shuffle(COLOURS)

for colour in COLOURS:

    colour_dict[str(colour)] = naming_trial(colour)

info(end) #where the experiment ends for the participant





#go through the rows in the df and add category &colour term values

for index, row in DATA.iterrows():

    colour1 = colour_dict[row['colour1']]

    colour2 = colour_dict[row['colour2']]

    category = 'within' if colour1 == colour2 else 'across'

    DATA['category'][index] = category

    DATA['col1_name'][index] = colour1 

    DATA['col2_name'][index] = colour2





#write df to csv file

DATA.to_csv(SAVE_FOLDER + "/logfile_" + ID[0] + '.csv')


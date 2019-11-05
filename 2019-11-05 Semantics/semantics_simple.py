
# Script that records word association lists, get semantic distances from http://swoogle.umbc.edu/SimService/GetSimilarity 
# and plot the distances

# import modules

from psychopy import visual, event, core, gui
import pandas as pd
import numpy as np
from requests import get


# create dialogue box for time entry
V = {'subject_ID':'', 'age': '', 'gender':['m', 'f', 'o'], 'category': ['animals', 'foods'], 'Insert time in secs (e.g. 120):':int()}
if not gui.DlgFromDict(V, order=['subject_ID', 'age', 'gender', 'Insert time in secs (e.g. 120):']).OK:
    core.quit()

# create empty panda matrix 

columns = ['subject', 'age', 'gender', 'word', 'word_nr', 'time']
index = np.arange(0) # array of numbers for the number of samples
word_list = pd.DataFrame(columns=columns, index = index)
word_nr = 0

# make word entry function 

# -*- coding: utf-8 -*-
chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# Set up window and text field

win = visual.Window(fullscr = True)
text = visual.TextStim(win, text='')


#display info text and wait for key press
def info(string, end = False):
    disp = visual.TextStim(win, text=string, height=.08)
    disp.draw()
    win.flip()
    event.waitKeys()[0]
    win.flip()
    event.clearEvents()

#pull up a screen that lets them start the experiment
txt="You now have {} seconds to name as many different {} as you can think of. Press any key when you are ready.".format(V["Insert time in secs (e.g. 120):"], V["category"])
info(txt)


# initialize abort option
endTrial = False
# initialize clock
clock = core.Clock()
stopwatch = core.Clock()

while not endTrial:
    # Wait for response...
    if clock.getTime() > int(V['Insert time in secs (e.g. 120):']):
        endTrial = True
    response = event.waitKeys()
    if response:
        # If backspace, delete last character
        if response[0] == 'backspace':
            text.setText(text.text[:-1])
            
        # Insert space
        elif response[0] == 'space':
            text.setText(text.text + ' ')

        # Else if a letter, append to text:
        elif response[0] in chars:
            text.setText(text.text + response[0])

        # If return, save word to panda and reset inputw
        elif response[0] == 'return':
            time = stopwatch.getTime()
            word_nr += 1
            word_list = word_list.append({'subject':V['subject_ID'], 'age':V['age'], 'gender':V['gender'], 'category':V['category'], 'word': text.text, 'word_nr': word_nr, 'time': time}, ignore_index=True)
            text.setText(text='')
            stopwatch.reset()
        
        # If esc key - end experiment
        elif response[0] == 'escape': 
            endTrial = True
        

    # Display updated text
    text.draw()
    win.flip()
win.close()

print (word_list)
    


# print the resulting list
print( word_list)
word_list.to_csv(str(V['subject_ID'])+'.csv')

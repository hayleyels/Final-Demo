
from classy import *
from pylab import imread,imsave,imshow,float32,figure,subplot,title,text,axis
from numpy import atleast_2d
import numpy as np
from image_defs import *
from glob import glob
from my_robot_functions import *
from Game import Board
from connect3 import *

def read_state_from_file(filename):
    text=open(filename).read()
    text=text.strip()
    lines=[line.strip() for line in text.split('\n')]  # get rid of \n
    
    row=lines[0].split()
    R,C=len(lines),len(row)
    print(f"{R}x{C} board")
    state=Board(R,C)
    state.board=[int(val) for val in text.split()]  
    print(state)
    return state

def read_state():
    from pylab import imread,imsave
    from numpy import atleast_2d
    import os

    state=Board(4,5)      #<========= change the size
    nr,nc=state.shape

    
    # load the classifier
    classifier=CSC()
    classifier.load('CSC_trained_demo4.json')
    
    
    # get the picture
    filename='current_board.jpg'              # for the robot
    take_picture(filename)


    # this part comes from your Make Training Squares script
    image=imread(filename)

    # these few lines are specific to your image
    corners= array([[89., 39.], 
                 [1105., 23.], 
                 [1198., 590.], 
                 [6., 593.]], dtype=float32)  
    image=image[300:900,:1200]
    im3=straighten_image(image,corners)
    squares=get_board_squares_from_image(im3,
                                     state.shape,
                                     middle_pixels=20)  # <=== check this

    # for debugging
    if not os.path.exists('predicted'):
        os.mkdir('predicted')

    count=0
    values=[]

    
    for r in range(nr):
        for c in range(nc):
            # convert the square image to a data vector for the classifier
            vector=squares[count].ravel()
            prediction=classifier.predict(atleast_2d(vector))[0]
        
            values.append(prediction)
    
            # for debugging
            imsave('predicted/square %d predicted as piece %d.jpg' % (count,prediction),squares[count])

            count+=1

    
    # reconstruct the state from the predictions
    state.board=values

    print("Current state is:")
    print(state)

    x=input("""
    Hit return if this is correct, otherwise type a character 
    and the state will be read from board.txt... 
    or type in a Board string like 111/000/222: """)

    if x:
        if "/" in x and '0' in x:
            state=Board(x)
        else:
            print("Reading from file...")
            state=read_state_from_file('board.txt')

    print("Using")
    print(state)

    
    return state

def get_move(state,player):
    if player==1:
        S=LoadTable("connect3_skittles1.json")
    else:
        S=LoadTable("connect3 skittles2.json")
    if state not in S:
        print("State is not in the Skittles table.", state)
        move=random_move(state,player)
    else:
        move=top_choice(S[state])
    print(move)
    return move

state=read_state()     #  read the state from the world
move=get_move(state,1)   # from an agent
make_move(state,move)        # robot motion to move pieces, etc...
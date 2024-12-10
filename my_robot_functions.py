from Robot373 import *
left,right,arm = Motors("abc")

# helper functions

# movement
def degrees(position):
    return position * 1.0

def distance_traveled(position):
    wheel_diameter_cm = 7.8
    pi = 3.141592653589793235

    return pi * wheel_diameter_cm * degrees(position) / 360

def forward():
    left.power = 20
    right.power = 20

def backward():
    left.power = -20
    right.power = -20

def stop():
    left.power = 0
    right.power = 0

def rot90left():
    left.reset_position()
    left.power = 30
    right.power = -30

    axis_length_cm = 16.35
    pi = 3.141592653589793235
    distance_needed = (axis_length_cm/2) * 2 * pi / 4
    while distance_traveled(left.position) < distance_needed:
        Wait(0.01)

def rot90right():
    right.reset_position()
    left.power = -30
    right.power = 30

    axis_length_cm = 16
    pi = 3.141592653589793235
    distance_needed = (axis_length_cm/2) * 2 * pi / 4
    while distance_traveled(right.position) < distance_needed:
        Wait(0.01)

# game implementation helper functions

def go_forward_cols(n):
    left.reset_position()
    num_cols = 4-n
    yellow_dist = 11.43+(19.05*num_cols)
    
    forward()

    while distance_traveled(left.position)<yellow_dist:
        Wait(0.01)

def go_backward_cols(n):
    left.reset_position()
    num_cols = 4-n
    yellow_dist = 11.43+(19.05*num_cols)
    
    backward()

    while distance_traveled(left.position) * -1 < yellow_dist:
        Wait(0.01)

def get_row(state,move):
    i = move+15
    row = 3

    while state[i]!=0:
        i-=5
        row-=1
    return row

def go_forward_rows(state,move):
    left.reset_position()

    row = get_row(state,move)
    
    print(row)

    blue_dist = 8.89+(12.7*row)

    forward()

    while distance_traveled(left.position)<blue_dist:
        Wait(0.01)

def go_backward_rows(state,move):
    left.reset_position()

    row = get_row(state,move)

    dist = 8.89+(12.7*row)

    backward()

    while distance_traveled(left.position) * -1 < dist:
        Wait(0.01)


# demo 3 function 3 - make move
def make_move(state,move):
    # piece
    rot90left()
    forward()
    Wait(1.5)

    # pick up piece
    arm.power = -10
    Wait(0.35)

    # move backward with piece
    backward()
    Wait(1.65)

    # rotate back to starting position
    rot90right()
    stop()

    # go to space (with piece)
    go_forward_cols(move)
    rot90left()
    stop()
    go_forward_rows(state,move)
    stop()

    # drop piece
    arm.power = 10
    Wait(0.7)
    arm.power = 0
    Wait(0.05)

    # move backward to start of column
    go_backward_rows(state,move)
    backward()
    Wait(0.5)
    rot90right()
    stop()
    go_backward_cols(move)
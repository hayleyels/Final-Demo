from Game import *
from Game.minimax import *

# game
def initial_state():
    return Board(4,5)

def valid_moves(state,player):
    moves=[]
    
    for i in range(5):
        if state[i]==0:
            moves.append(i)

    return moves

def update_state(state,player,move):
    # 0  1  2  3  4 
    # 5  6  7  8  9 
    # 10 11 12 13 14 
    # 15 16 17 18 19 
    if isinstance(move,int):
        new_state=state

        i=move+15
        
        while new_state[i]!=0:
            i-=5
            
        new_state[i]=player

    return new_state

def win_status(state,player):
    # 0  1  2  3  4 
    # 5  6  7  8  9 
    # 10 11 12 13 14 
    # 15 16 17 18 19  
    
    if player==1:
        other_player=2

    else:
        other_player=1

    for row in state.rows(3):
        if row==[player,player,player]:
            return "win"

    for col in state.cols(3):
        if col==[player,player,player]:
            return "win"

    for diag in state.diags(3):
        if diag==[player,player,player]:
            return "win"

    if not valid_moves(state,other_player):
        return "stalemate"

    return None

def show_state(state,player):
    print(state)

# human, random, and minimax
def human_move(state,player):
    while True:
        move = eval(input("What is your move? "))

        if move not in valid_moves(state,player):
            print("That is not a valid move")
        else:
            break

    return move
    
def random_move(state,player):
    return random.choice(valid_moves(state,player))

def minimax_move(state,player):
    values,actions=minimax_values(state,player, display=False,maxdepth=5)
    return top_choice(actions,values)

human_agent=Agent(human_move)
random_agent=Agent(random_move)
minimax_agent=Agent(minimax_move)

# skittles
def skittles_move(state,player,info):
    S=info.S
    last_state=info.last_state
    last_action=info.last_action
    verbose=info.verbose

    
    if verbose:
        print("\t","Player ",player," is thinking...")
        print("\t","State: ",state)
        print("\t","Table:",S)
        print("\t","Last state,action: ",last_state,last_action)
    
    # make/adjust the table

    if state not in S:
        # add a row to the table for each move
        S[state]=Table()
        moves=valid_moves(state,player)
        for action in moves:
            S[state][action]=3  # number of skittles/beads for each move
    
        if verbose:
            print("\t","State ",state,"unknown...added to table")
            print("\t","Table",S)
    
    move=weighted_choice(S[state])
    if verbose:
        print("\t","Choosing from S[",state,"]",S[state],"....Move: ",move)

    if move is None:  # there are no skittles in this row
        if last_state:
            if verbose:
                print("\t","No possible moves!")
                print("\t","Modifying the table: removing one skittle from (state,action) ",last_state,last_action)
            S[last_state][last_action]=S[last_state][last_action]-1
            
            if verbose:
                print("\t","Table:",S)
                
            if S[last_state][last_action]<0:                
                S[last_state][last_action]=0
                if verbose:
                    print("\t","Negative skittles...fixing.")
                    print("\t","Table:",S)                
        else:
            if verbose:
                print("\t","Started in a bad state ",state,"with no moves and no last state.  Won't modify table.")
                  
                  

        move=random_move(state,player)

    
    return move

def skittles_after(status,player,info):
    S=info.S
    last_state=info.last_state
    last_action=info.last_action
    verbose=info.verbose

    if verbose:
        print("\t","End of Game adjustments")
        print("\t","Player ",player," is thinking...")
        print("\t","Win Status: ",status)
        print("\t","Table:",S)
        print("\t","Last state,action: ",last_state,last_action)
        
    if status=='lose':
        if last_state:
            S[last_state][last_action]=S[last_state][last_action]-1
            if S[last_state][last_action]<0:
                S[last_state][last_action]=0
                
            if verbose:
                print("\t","Modifying the table: removing one skittle from (state,action) ",last_state,last_action)
                print("\t","Table:",S)

                
        else:
            if verbose:
                print("\t","No last state, so nothing to learn.")
            
                
    else:
        if verbose:
            print("\t","No adjustments needed.")
        
skittles_agent1=Agent(skittles_move)
skittles_agent1.S=Table()
skittles_agent1.post=skittles_after
skittles_agent1.verbose=False

skittles_agent2=Agent(skittles_move)
skittles_agent2.S=Table()
skittles_agent2.post=skittles_after
skittles_agent2.verbose=False
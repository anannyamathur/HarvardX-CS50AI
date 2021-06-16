"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    cnt=0
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                cnt=cnt+1
    if cnt%2==0:
        return O
    else:
        return X
    # raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    action=set([])
    for rows in range(3):
        for columns in range(3):
            if board[rows][columns]==EMPTY:
                action.add((rows,columns))
    return action
    # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Move is not valid")
    Cboard = copy.deepcopy(board)
    Cboard[action[0]][action[1]]=player(board)
    return Cboard

    # raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        row= ""
        for j in range(3):
            row= row + str(board[i][j])
        if(row=="OOO"):
            return O
        if(row=="XXX"):
            return X
    
    for i in range(3):
        column=""
        for j in range(3):
            column=column+str(board[j][i])
        if(column=="OOO"):
            return O
        if(column=="XXX"):
            return X
    d1= ""
    d2= ""
    for i in range(3):
        d1=d1+ str(board[i][i])
        d2=d2 + str(board[i][2-i])
    if(d1=="OOO" or d2=="OOO"):
        return O
    if(d1=="XXX" or d2=="XXX"):
        return X
    
    return None 

    # raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    if not actions(board):
        return True
    
    return False 
    # raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board)== 'X':
        return 1
    if winner(board)== 'O':
        return -1
    return 0
    
    # raise NotImplementedError

def maxValue(board, alpha, beta):
    if terminal(board):
        return (utility(board), None)
    x= float('-inf')
    y=None

    for moves in actions(board):
        minimum= minValue(result(board,moves), alpha,beta)[0]
        if minimum>x:
            x=minimum
            y=moves
        alpha=max(x,alpha)
        if (alpha>=beta):
            break
    return (x,y)

def minValue(board, alpha, beta):
    if terminal(board):
        return (utility(board), None)
    x= float('inf')
    y=None
    for moves in actions(board):
        maximum=maxValue(result(board,moves), alpha,beta)[0]
        if maximum<x:
            x=maximum
            y=moves
        beta=min(x,beta)
        if (alpha>=beta):
            break
    return (x,y)
    



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    alpha= float('-inf')
    beta=float('inf')
    if player(board)=='X':
        return maxValue(board,alpha,beta)[1]
    elif player(board)=='O':
        return minValue(board,alpha,beta)[1]

    # raise NotImplementedError

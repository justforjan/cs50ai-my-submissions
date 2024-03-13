"""
Tic Tac Toe Player
"""

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

    count = 0

    for row in board:
        count += row.count(X)
        count += row.count(O)    

    if count % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    actions = set()

    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if col is EMPTY:
                actions.add((i,j))
    
    return actions

    


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2:
        raise Exception("Move not valid")


    b = copy.deepcopy(board)

    if b[action[0]][action[1]] == EMPTY:
        b[action[0]][action[1]] = player(board)
        return b
    
    raise Exception("Move not valid")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # rows
    for row in board:
        if row[0] and (row[0] == row[1] == row[2]):
            return row[0]
    
    # diagonal
    if board[0][0] and (board[0][0] == board[1][1] == board[2][2]):
        return board[0][0]
    
    if board[0][2] and (board[0][2] == board[1][1] == board[2][0]):
        return board[0][2]
    
    # cols
    for i in range(len(board)):
        if board[0][i] and (board[0][i] == board[1][i] == board[2][i]):
            return board[0][i]
        
    return None




def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) is not None:
        return True
    
    if not actions(board):
        return True
    
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    w = winner(board)

    if w == X:
        return 1
    
    if w == O:
        return -1
    
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None
    
    resulting_action = None

    # tic = time.time()

    if player(board) is X:
        v = -10 

        for action in actions(board):
            value = minvalue(result(board, action), v)
            if  value > v:
                v = value
                resulting_action = action

    else:
        v = 10 

        for action in actions(board):
            value = maxvalue(result(board, action), v)
            if value < v:
                v = value
                resulting_action = action
    
    # toc = time.time()

    # print("Elapes time: " + str(toc -tic))

    return resulting_action


# Argument c for Alpha-Beta Pruning
def maxvalue(board, c):
    if terminal(board):
        return utility(board)
    
    v = -10
    
    for action in actions(board):
        v = max(v, minvalue(result(board, action), v))
        # Alpha-Beta Pruning:
        if v >= c:
            break

    return v



def minvalue(board, c):
    if terminal(board):
        return utility(board)
    
    v = 10

    for action in actions(board):
        v = min(v, maxvalue(result(board, action), v))
        # Alpha-Beta Pruning:
        if v <= c:
            break

    return v

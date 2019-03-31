from random import choice
from Experiments.DobotControl_TTT import drawMove

DOBOT = +1
HUMAN = -1
dobotMoves = []
board = [ [0, 0, 0],
          [0, 0, 0],
          [0, 0, 0], ]

def clearBoard():
    for x, col in enumerate(board):
        for y in enumerate(col):
            board[x][y] = 0

def get_Score(state):
    if is_EndState(state, DOBOT):
        score = +1
    elif is_EndState(state, HUMAN):
        score = -1
    else:
        score = 0

    return score

def is_EndState(state, player):
    win_Positions = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]] ]

    if [player, player, player] in win_Positions:
        return True
    else:
        return False

def test_Wins(state):
    return is_EndState(state, DOBOT) or is_EndState(state, HUMAN)

def get_FreePos(state):
    freeMoves = []
    
    for x, col in enumerate(state):
        for y, val in enumerate(col):
            if val == 0:
                freeMoves.append([x, y])
                # valStr = "x: {}, y: {}"
                # print(valStr.format(x, y))

    return freeMoves

def valid_Move(x, y):
    if [x, y] in get_FreePos(board):
        return True
    else:
        return False

def mark_Pos(x, y, player):
    if valid_Move(x, y):
        board[x][y] = player
        return True
    else:
        return False

def min_max(state, depth, player):
    if player == DOBOT:
        best = [-1, -1, -100]
    else:
        best = [-1, -1, 100]

    if depth == 0 or test_Wins(state):
        score = get_Score(state)
        return [-1, -1, score]

    for val in get_FreePos(state):
        x, y = val[0], val[1]
        state[x][y] = player
        score = min_max(state, depth - 1, (player * -1))
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == DOBOT:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score

    # valStr = "x: {}, y: {}"
    # print(valStr.format(best[0], best[1]))
    return best

def print_Board(state):
    chars = {
        +1: 1,
        -1: -1,
        0: 0
    }

    print("\nCurrent State of Board:")
    for col in state:
        for val in col:
            symbol = chars[val]
            valStr = "| {} |"
            # print(f"| {symbol} |", end="")
            print(valStr.format(symbol), end="")
        print("\n----------------")

def player_Move(index):
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    coords = moves[index]
    if [coords[0], coords[1]] not in dobotMoves:
        human_Turn(coords[0], coords[1])
                

def dobot_Turn():
    depth = len(get_FreePos(board))
    if depth == 0 or test_Wins(board):
        return

    print("\t--Dobot's Turn--")
    print_Board(board)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = min_max(board, depth, DOBOT)
        x, y = move[0], move[1]

    # valStr = "x: {}, y: {}"
    # print(valStr.format(x, y))

    
    mark_Pos(x, y, DOBOT)
    dobotMoves.append([x, y])
    drawMove(x, y)
    # time.sleep(1)

def human_Turn(x, y):
    depth = len(get_FreePos(board))
    if depth == 0 or test_Wins(board):
        return

    try:
        can_Move = mark_Pos(x, y, HUMAN)

        if not can_Move:
            print("Not a Valid Move Human, Try Again.")
            print_Board(board)
    except(KeyError, ValueError):
        print("Not Valid Human, Try Again.")
        print_Board(board)

def exe_Play():

    # Dobot Takes it's turn first
    while len(get_FreePos(board)) > 0 and not test_Wins(board):
        dobot_Turn()
        human_Turn()

    if is_EndState(board, DOBOT):
        print("\t--Dobot WINS--")
        print_Board(board)
        print("\t--Dobot WINS--")
    elif is_EndState(board, HUMAN):
        print("\t--Human WINS--")
        print_Board(board)
        print("\t--Human WINS--")
    else:
        print("\t--DRAW--")
        print_Board(board)
        print("\t--DRAW--")

    # exit()

exe_Play()

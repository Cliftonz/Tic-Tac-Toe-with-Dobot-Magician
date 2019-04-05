
from random import choice
# from DobotControl import drawMove

DOBOT = 1
HUMAN = -1
dobot_moves = []
board = [0, 0, 0, 0, 0, 0, 0, 0, 0]


def clear_board():
    for i in range(0, 9):
        board[i] = 0
        

def get_board(state):
    if is_win(state, DOBOT) is True:
        score = 1
    elif is_win(state, HUMAN) is True:
        score = -1
    else:
        score = 0

    return score


def is_win(state, player):
    win_positions = [
        [state[0], state[1], state[2]],
        [state[3], state[4], state[5]],
        [state[6], state[7], state[8]],
        [state[0], state[3], state[6]],
        [state[1], state[4], state[7]],
        [state[2], state[5], state[8]],
        [state[0], state[4], state[8]],
        [state[2], state[4], state[6]]
    ]
    
    if [player, player, player] in win_positions:
        return True
    else:
        return False


def test_draw():
    draw = False
    if len(get_free_pos(board)) == 0 and test_wins() == False:
        draw = True

    return draw


def test_wins():
    # return is_win(board, DOBOT) or is_win(board, HUMAN)
    win = False
    if is_win(board, DOBOT) is True or is_win(board, HUMAN) is True:
        win = True

    return win


def get_free_pos(state):
    free_moves = []

    for i in range(0, 9):
        if state[i] == 0:
            free_moves.append(i)

    return free_moves


def valid_move(index):
    if index in get_free_pos(board):
        return True
    else:
        return False


def mark_pos(index, player):
    if valid_move(index) is True:
        board[index] = player
        return True
    else:
        return False


def coord_trans(index):
    moves = [6, 3, 0,
             7, 4, 1,
             8, 5, 2
            ]
    
    coord = moves[index]

    return coord


def coord_func(index, player):
    # coord = coord_trans(index)
    
    if valid_move(index) is True:
        # drawMove(coords[0], coords[1])
        mark_pos(index, player)
        dobot_moves.append(index)
        print_board(board)


def rand_list(moveList):
    freeMoves = get_free_pos(board)
    posMoves = []
    for i in moveList:
        if i in freeMoves:
            posMoves.append(i)

    if len(posMoves) != 0:
        return choice(posMoves)
    else:
        return None


def get_ai_move(free_moves):
    
    # First, check if we can win in the next move
    for i in range(0, 9):
        copy = board.copy()
        co = coord_trans(i)
        if copy[co] == 0:
            copy[co] = DOBOT
            if is_win(copy, DOBOT) is True:
                return co

    # Check if the player could win on his next move, and block them.
    for i in range(0, 9):
        copy = board.copy()
        co = coord_trans(i)
        if copy[co] == 0:
            copy[co] = HUMAN
            if is_win(copy, HUMAN) is True:
                return co

    #rand_pos = choice(freeMoves)
    #co = coord_trans(rand_pos)
    #return co

    # Try to take the center, if it is free.
    if 4 in free_moves:
        return 4

    # Try to take one of the corners, if they are free.
    corners = [0, 2, 6, 8]
    move = rand_list(corners)
    if move is not None:
        return coord_trans(move)

    # Move on one of the sides.
    sides = [1, 3, 5, 7]
    pick = rand_list(sides)
    #if pick is not None:
    return coord_trans(pick)


def dobot_turn():
    if test_wins() is True or test_draw() is True:
        return
    free_moves = get_free_pos(board)

    move = get_ai_move(free_moves)
    if move not in free_moves:
        rand_pos = choice(free_moves)
        move = coord_trans(rand_pos)

    coord_func(move, DOBOT)


def dobot_turnv2():
    freeMoves = get_free_pos(board)
    copy = board.copy()

    move = -1
    found = False
    
    if len(freeMoves) <= 5:
        while found is False:
            for i in range(len(copy)):
                co = coord_trans(i)
                if copy[co] == 0:
                    copy[co] = DOBOT
                    if is_win(copy, DOBOT) is True:
                        move = co
                        found = True
                        break
                    copy[co] = 0

        while found is False:
            for i in range(len(copy)):
                co = coord_trans(i)
                if copy[co] == 0:
                    copy[co] = HUMAN
                    if is_win(copy, HUMAN) is True:
                        move = co
                        found = True
                        break
                    copy[co] = 0
    else:
        rand_pos = choice(freeMoves)
        co = coord_trans(rand_pos)
        move = co
        # coord_func(co, DOBOT)

    coord_func(move, DOBOT)


def human_turn(index):
    if test_wins() is True or test_draw() is True:
        return

    try:
        can_move = mark_pos(index, HUMAN)

        if not can_move:
            print("Not a Valid Move Human, Try Again.")
            #print_board(board)
    except(KeyError, ValueError):
        print("Not Valid Human, Try Again.")
        #print_board(board)

    print_board(board)


def print_board(state):
    chars = {
        +1: 1,
        -1: -1,
        0: 0
    }

    print("\nCurrent State of Board:")
    c = 1
    for val in state:
        symbol = chars[val]
        val_str = "| {} |"
        print(val_str.format(symbol), end="")
        if c % 3 == 0:
            print("\n----------------")
        c += 1


def player_move(index):
    moves = {
        1: 0, 2: 1, 3: 2,
        4: 3, 5: 4, 6: 5,
        7: 6, 8: 7, 9: 8
    }

    move = moves[index]
    if move not in dobot_moves:
        human_turn(move)

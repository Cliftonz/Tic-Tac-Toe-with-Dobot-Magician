
from random import choice
from DobotControl import drawMove

DOBOT = +1
HUMAN = -1
dobot_moves = []
board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]


def clear_board():
    for x, col in enumerate(board):
        for y in enumerate(col):
            board[x][y] = 0


def get_board(state):
    if is_end_state(state, DOBOT):
        score = +1
    elif is_end_state(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def is_end_state(state, player):
    win_positions = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]]]

    if [player, player, player] in win_positions:
        return True
    else:
        return False


def test_wins():
    return is_end_state(board, DOBOT) or is_end_state(board, HUMAN)


def get_free_pos(state):
    free_moves = []

    for x, col in enumerate(state):
        for y, val in enumerate(col):
            if val == 0:
                free_moves.append([x, y])

    return free_moves


def valid_move(x, y):
    if [x, y] in get_free_pos(board):
        return True
    else:
        return False


def mark_pos(x, y, player):
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def min_max(state, depth, player):
    if player == DOBOT:
        best = [-1, -1, -100]
    else:
        best = [-1, -1, 100]

    if depth == 0 or test_wins():
        score = get_board(state)
        return [-1, -1, score]

    for val in get_free_pos(state):
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

    return best


def dobot_turn():
    depth = len(get_free_pos(board))
    if depth == 0 or test_wins():
        return

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = min_max(board, depth, DOBOT)
        x, y = move[0], move[1]

    mark_pos(x, y, DOBOT)
    dobot_moves.append([x, y])
    drawMove(x, y)


def human_turn(x, y):
    depth = len(get_free_pos(board))
    if depth == 0 or test_wins():
        return

    try:
        can_move = mark_pos(x, y, HUMAN)

        if not can_move:
            print("Not a Valid Move Human, Try Again.")
            print_board(board)
    except(KeyError, ValueError):
        print("Not Valid Human, Try Again.")
        print_board(board)


def print_board(state):
    chars = {
        +1: 1,
        -1: -1,
        0: 0
    }

    print("\nCurrent State of Board:")
    for col in state:
        for val in col:
            symbol = chars[val]
            val_str = "| {} |"
            print(val_str.format(symbol), end="")
        print("\n----------------")


def player_move(index):
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    coords = moves[index]
    if [coords[0], coords[1]] not in dobot_moves:
        human_turn(coords[0], coords[1])

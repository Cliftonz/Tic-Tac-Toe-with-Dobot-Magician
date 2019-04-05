
from random import choice
from DobotControl import drawMove

DOBOT = +1
HUMAN = -1
dobot_moves = []
board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0], ]


def clear_board():
    for x in range(0, 3):
        for y in range(0, 3):
            board[x][y] = 0


def get_board(state):

    if is_end_state(state, DOBOT):
        score = +1
    elif is_end_state(state, HUMAN):
        score = -1
    else:
        score = 0

    if dobot_win_next_turn(state):
        score += 1

    if player_win_next_turn(state):
        score -= 1

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
    # return is_end_state(board, DOBOT) or is_end_state(board, HUMAN)
    win = False
    if is_end_state(board, DOBOT) is True or is_end_state(board, HUMAN) is True:
        win = True

    return win


def get_free_pos(state):
    free_moves = []

    for x in range(0, 3):
        for y in range(0, 3):
            if state[x][y] == 0:
                free_moves.append([x, y])

    return free_moves


def valid_move(x, y):
    if [x, y] in get_free_pos(board):
        return True
    else:
        return False


def mark_pos(x, y, player):
    # if valid_move(x, y):
    board[x][y] = player
    #    return True
    # else:
     #   return False


def mark_pos(x, y, player, state):
    # if valid_move(x, y):
    state[x][y] = player
    #    return True
    # else:
     #   return False


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
        next_state = state.copy()
        score = min_max(next_state, depth - 1, (player * -1))
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == DOBOT:
            if score[2] > best[2]:
                best = score.copy()
        else:
            if score[2] < best[2]:
                best = score.copy()

    return best


def dobot_win_next_turn(state):
    win = False
    # find if dobot will win next turn
    for x in range(0, 3):
        for y in range(0, 3):
            current_board = state.copy()
            if valid_move(x, y):
                mark_pos(x, y, DOBOT, current_board)
                if is_end_state(current_board, DOBOT):
                    win = True
                    break
    return win


def player_win_next_turn(state):
    win = False
    # find if player will win next turn and block
    for x in range(0, 3):
        for y in range(0, 3):
            current_board = state.copy()
            if valid_move(x, y):
                mark_pos(x, y, HUMAN, current_board)
                if is_end_state(current_board, DOBOT):
                    win = True
                    break
    return win


def dobot_turn():
    depth = len(get_free_pos(board))
    if depth == 0 or test_wins():
        return

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        current_board = board.copy()
        move = min_max(current_board, depth, DOBOT)
        x, y = move[0], move[1]

    # moves = {
    #     [0, 0]: [2, 0], [0, 1]: [1, 0], [0, 2]: [0, 0],
    #     [1, 0]: [2, 1], [1, 1]: [1, 1], [1, 2]: [0, 1],
    #     [2, 0]: [2, 2], [2, 1]: [1, 2], [2, 2]: [0, 2]
    # }

    moves = [
            [[2, 0],  [1, 0],  [0, 0]],
            [[2, 1],  [1, 1],  [0, 1]],
            [[2, 2],  [1, 2],  [0, 2]]
            ]

    coords = moves[x][y]

    mark_pos(coords[0], coords[1], DOBOT)
    dobot_moves.append(coords)
    drawMove(coords[0], coords[1])


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
        7: [2, 0], 8: [2, 1], 9: [2, 2]
    }

    coords = moves[index]
    if [coords[0], coords[1]] not in dobot_moves:
        human_turn(coords[0], coords[1])

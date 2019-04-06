

from random import choice
import copy

DOBOT = +1
HUMAN = -1
dobot_moves = []
board = [0, 0, 0, 0, 0, 0, 0, 0, 0 ]


def clear_board():
    for i in range(0, 9):
        board[i] = 0


def test_draw():
    draw = False
    if len(get_free_pos(board)) == 0 and test_wins() is False:
        draw = True

    return draw


def get_board(state):

    if is_win(state, DOBOT) is True:
        score = +1
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


def test_wins():
    # return is_end_state(board, DOBOT) or is_end_state(board, HUMAN)
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


def temp_state_valid_move(index, state):
    if index in get_free_pos(state):
        return True
    else:
        return False


def mark_pos(index, player):
    if valid_move(index) is True:
        board[index] = player
        return True
    else:
        return False


def mark_temp_board_pos(index, player, state):
    if valid_move(index) is True:
        state[index] = player
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
        next_state = copy.deepcopy(state)
        score = min_max(next_state, depth - 1, (player * -1))
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == DOBOT:
            if score[2] > best[2]:
                best = copy.deepcopy(score)
        else:
            if score[2] < best[2]:
                best = copy.deepcopy(score)

    return best


def dobot_win_next_turn(state):
    # find if dobot will win next turn
    for x in range(0, 8):
        current_board = copy.deepcopy(state)
        if temp_state_valid_move(x, current_board) is True:
            mark_temp_board_pos(x, DOBOT, current_board)
            if is_win(current_board, DOBOT):
                win = (x, True)
                break
            else:
                win = (x, False)
    return win


def player_win_next_turn(state):
    for x in range(0, 8):
        current_board = copy.deepcopy(state)
        if temp_state_valid_move(x, current_board) is True:
            mark_temp_board_pos(x, HUMAN, current_board)
            if is_win(current_board, HUMAN):
                win = (x, True)
                break
            else:
                win = (x, False)
    return win


def immediate_win(state):

    move = dobot_win_next_turn(state)

    if move[1] is True:
        return move

    move = player_win_next_turn(state)

    if move[1] is True:
        return move

    return move


def dobot_turn():
    depth = len(get_free_pos(board))

    if depth == 0 or test_wins():
        return

    if depth == 9:
        move = choice([0, 1, 2, 3, 4, 5, 6, 7, 8])

    elif depth <= 6:
        move = immediate_win(board)
        if move[1] is False:
            current_board = copy.deepcopy(board)
            move = min_max(current_board, depth, DOBOT)

    else:
        current_board = copy.deepcopy(board)
        move = min_max(current_board, depth, DOBOT)

    move_check = move

    if not(move in get_free_pos(board)):
        move = choice(get_free_pos(board))

    # moves = [
    #         [[2, 0],  [1, 0],  [0, 0]],
    #         [[2, 1],  [1, 1],  [0, 1]],
    #         [[2, 2],  [1, 2],  [0, 2]]
    #         ]

    mark_pos(move, DOBOT)

    dobot_moves.append(move)
    # in actual implementation draw coords[0], coords[1]
    print_board(board)


def human_turn(index):
    if test_wins() is True or test_draw() is True:
        return

    try:
        can_move = mark_pos(index, HUMAN)

        if not can_move:
            print("Not a Valid Move Human.")
            correct_pos = input("What was the players move: ")
            mark_pos(correct_pos, HUMAN)

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

    print_board(board)

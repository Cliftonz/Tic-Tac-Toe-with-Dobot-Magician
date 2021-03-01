from math import inf as infinity
from random import choice
import platform
import time
from os import system
import copy
import csv

DOBOT = +1
HUMAN = -1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

Visited = []

def evaluate(state):
    if wins(state, DOBOT):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def wins(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def game_over(state):
    return wins(state, HUMAN) or wins(state, DOBOT)


def empty_cells(state):
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def valid_move(x, y):
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minimax(state, depth, player):
    if player == DOBOT:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == DOBOT:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best


def GenStates(state, depth, player):
    if depth == 0 or wins(state, player) or wins(state, -player):
        return None

    States = []

    for pstate in empty_cells(state):

        x, y = pstate[0], pstate[1]
        state[x][y] = player
        next_state = copy.deepcopy(state)
        state[x][y] = 0

        if wins(next_state, player) or wins(next_state, -player) or next_state in Visited:
            continue

        # Get value for this state
        # If the state only has one opening find it and return it
        blanks = empty_cells(next_state)
        if len(blanks) == 1:
            # find blank position and return
            States.append((next_state, blanks[0][0] * 3 + blanks[0][1]))
            Visited.append(next_state)
        else:
            score = minimax(next_state, depth - 1, -player)

            move = score[0] * 3 + score[1]

            # add best move and current state to the return and return it
            States.append((next_state, move))

            Visited.append(next_state)

            # Recursive call to gen the set of states based off of this state
            States.extend(GenStates(next_state, depth - 1, -player))

    return States

def main():
    # Start with a blank board
    # tboard = [[0, 0, 0],
    #           [0, HUMAN, 0],
    #           [0, 0, 0], ]
    #
    # # Generate all valid positions for Dobot and human
    # states = [(tboard, 4)]
    #
    # states.extend(GenStates(tboard, 8, DOBOT))
    #
    # tboard = [[0, 0, 0],
    #           [0, DOBOT, 0],
    #           [0, 0, 0], ]
    #
    # states.extend(GenStates(tboard, 8, HUMAN))

    tboard = [[0, 0, 0],
              [0, 0, 0],
              [0, 0, 0], ]
    states = []

    states.extend(GenStates(tboard, 9, HUMAN))
    states.extend(GenStates(tboard, 9, DOBOT))

    # note make sure there are no duplicates in the output
    with open('TTTstates.csv', mode='w') as dataset:
        file_writer = csv.writer(dataset, dialect='excel', delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,)
        file_writer.writerow(['1', '2', '3', '4', '5', '6', '7', '8', '9', 'ans'])
        for row in states:
            # tmp = row[0].flatten()
            tmp = [item for sublist in row[0] for item in sublist]
            tmp.append(row[1])
            file_writer.writerow(tmp)

    print("finished")

    exit()


if __name__ == '__main__':
    main()


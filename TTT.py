
import cv2
import Vision_Processing as VP
import Motion_Processing as MP


def prompt(message):
    # raw_input returns the empty string for "enter"
    yes = {'yes', 'y', 'ye', ''}
    no = {'no', 'n'}

    print(message)

    choice = input().lower()
    if choice in yes:

        answer = True

    elif choice in no:

        answer = False

    else:

        print("Please respond with 'yes' or 'no'")

    return answer


if __name__ == '__main__':
    # TODO: Initialize camera, local variables, Game State, Dobot etc
    cam = cv2.VideoCapture(0)

    VP.camera_overlay(cam)

    play_again = True

    while play_again:

        cont = False
        while not cont:
            cont = prompt('Ready to start the game? ')
            print()

        # init current state of blank paper
        flags, current_state = cam.read()

        # initialize previous state
        flags, previous_state = cam.read()

        # Start of TTT loop
        current_game = True
        while current_game:

            # Did player make first move?
            # TODO: Make Dobot first move

            # Capture current state
            previous_state = current_state
            flags, current_state = cam.read()

            # wait 30 seconds for player input or motion has stopped
            MP.wait_for_player_move(cam)

            # Get player move
            previous_state = current_state
            flags, current_state = cam.read()

            # Todo: update state

            VP.get_player_move(previous_state, current_state)


            # Todo: If not an end game state , make next move and return to top of game loop

            # TODO: Else end loop

            # TODO: Play again prompt

            # TODO: clear internal representation

            # Todo: go to start

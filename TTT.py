
import cv2
import Vision_Processing as VP
import Motion_Processing as MP


def prompt(message):

    # raw_input returns the empty string for "enter"
    yes = {'yes', 'y', 'ye', ''}
    no = {'no', 'n'}

    print(message)

    while True:
        choice = input().lower()
        if choice in yes:

            answer = True
            break

        elif choice in no:

            answer = False
            break

        else:
            print("Please respond with 'yes' or 'no'")

    return answer


if __name__ == '__main__':
    # TODO: Initialize camera, local variables, Game State, Dobot etc
    cam = cv2.VideoCapture(0)

    VP.camera_overlay(cam)

    play_again = True

    while play_again:

        first_player = prompt('Will Dobot make the first move? ')

        if first_player is True:
            # Todo: send signal for Dobot to make x's
            pass
        else:
            # Todo: send signal for Dobot to make circles
            pass

        print('Do not')

        cont = prompt('Ready to start the game? ')

        # init current state of blank paper
        flags, current_state = cam.read()

        # initialize previous state
        flags, previous_state = cam.read()

        # Start of TTT loop
        current_game = True
        while current_game:

            if first_player:
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

            else:

                # wait 30 seconds for player input or motion has stopped
                MP.wait_for_player_move(cam)

                # Get player move
                previous_state = current_state
                flags, current_state = cam.read()

                # Todo: update state

                VP.get_player_move(previous_state, current_state)

                # TODO: Make Dobot move

                # Capture current state
                previous_state = current_state
                flags, current_state = cam.read()

        # Todo: If end game state, break

    play_again = prompt('Do you want to play again?')
    # TODO: clear internal representation


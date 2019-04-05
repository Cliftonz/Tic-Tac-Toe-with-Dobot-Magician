
import cv2
import Vision_Processing as Vision
import Motion_Processing as Motion
import Imp_MinimaxV2 as Logic
import time
import copy


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

    Debug = True

    cam = cv2.VideoCapture(0)

    play_again = True

    while play_again:

        Vision.camera_overlay(cam)

        first_player = prompt('Will Dobot make the first move? ')

        print('IMPORTANT - Make sure the game board is clear and nothing is in front of the camera.')

        cont = prompt('Ready to start the game? ')

        # init current state of blank paper
        flags, current_state = cam.read()

        # initialize previous state
        flags, previous_state = cam.read()

        # Start of TTT loop
        while True:

            if first_player:
                # Todo: send signal for Dobot to make x's or circles

                Logic.dobot_turn()
                time.sleep(8)
                # Capture current state
                previous_state = copy.deepcopy(current_state)
                flags, current_state = cam.read()

                if Logic.test_wins() is True:
                    break

                # wait 30 seconds for player input or motion has stopped
                Motion.wait_for_player_move(cam, Debug)

                # Get player move
                previous_state = copy.deepcopy(current_state)
                flags, current_state = cam.read()

                player_move = Vision.get_player_move(previous_state, current_state)

                Logic.player_move(player_move)

                if Logic.test_wins() is True:
                    break
            else:

                # wait 30 seconds for player input or motion has stopped
                Motion.wait_for_player_move(cam)

                # Get player move
                previous_state = copy.deepcopy(current_state)
                flags, current_state = cam.read()

                Logic.player_move(Vision.get_player_move(previous_state, current_state))

                if Logic.test_wins() is True:
                    break

                Logic.dobot_turn()

                # Capture current state
                previous_state = copy.deepcopy(current_state)
                flags, current_state = cam.read()

                if Logic.test_wins() is True:
                    break

        play_again = prompt('Do you want to play again?')

        Logic.clear_board()

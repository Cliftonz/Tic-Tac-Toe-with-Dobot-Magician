
import cv2
import Vision_Processing as Vision
import Motion_Processing as Motion
import Imp_MinimaxV2 as Logic
import time


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

    f = open('OfficalTestData/testData.text', 'a')

    cam = cv2.VideoCapture(0)

    play_again = True

    game_number = 0
    while play_again:
        if Debug is True:
            game_number += 1

            f.write(str(game_number))

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

                Logic.dobot_turn(Debug, f)
                time.sleep(8)
                # Capture current state
                previous_state = current_state[:]
                flags, current_state = cam.read()

                if Logic.test_wins() is True:
                    print("\t--DOBOT WINS--")
                    break
                if Logic.test_draw() is True:
                    print("\t--Tie--")
                    break

                # wait 30 seconds for player input or motion has stopped
                Motion.wait_for_player_move(cam, Debug)

                # Get player move
                previous_state = current_state[:]
                flags, current_state = cam.read()

                player_move = Vision.get_player_move(previous_state, current_state, Debug, f)

                print("The player's move was: " + str(player_move))

                Logic.player_move(player_move, Debug, f)

                if Logic.test_wins() is True:
                    print("\t--HUMAN WINS--")
                    break
                if Logic.test_draw() is True:
                    print("\t--Tie--")
                    break
            else:

                # wait 30 seconds for player input or motion has stopped
                Motion.wait_for_player_move(cam)

                # Get player move
                previous_state = current_state[:]
                flags, current_state = cam.read()

                player_move = Vision.get_player_move(previous_state, current_state, Debug, f)

                print("The player's move was: " + str(player_move))

                Logic.player_move(player_move, Debug, f)

                if Logic.test_wins() is True:
                    print("\t--DOBOT WINS--")
                    break
                if Logic.test_draw() is True:
                    print("\t--Tie--")
                    break

                Logic.dobot_turn(Debug, f)

                time.sleep(8)

                # Capture current state
                previous_state = current_state[:]
                flags, current_state = cam.read()

                if Logic.test_wins() is True:
                    print("\t--DOBOT WINS--")
                    break
                if Logic.test_draw() is True:
                    print("\t--Tie--")
                    break

        play_again = prompt('Do you want to play again?')

        Logic.clear_board()
    if Debug is True:
        f.close()

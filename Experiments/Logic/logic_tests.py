#import Game_Logic as Logic
from Experiments.Logic import GameLogicZ as Logic


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

    play_again = True

    while play_again:
        first_player = prompt('Will Dobot make the first move? ')

        # print('IMPORTANT - Make sure the game board is clear and nothing is in front of the camera.')

        cont = prompt('Ready to start the game? ')
        
        # Start of TTT loop
        while True:

            if first_player:
                # Todo: send signal for Dobot to make x's or circles

                Logic.dobot_turn()
                #time.sleep(8)
                # Capture current state
                if Logic.test_wins() is True or Logic.test_draw() is True:
                    print("\t--DOBOT WINS--")
                    break

                player_move = int(input("Choose Available Cell(1 - 9) to Move:"))

                Logic.player_move(player_move)

                if Logic.test_wins() is True or Logic.test_draw() is True:
                    print("\t--HUMAN WINS--")
                    break
            else:
                player_move = int(input("Choose Available Cell(1 - 9) to Move:"))
                
                Logic.player_move(player_move)

                if Logic.test_wins() is True or Logic.test_draw() == True:
                    print("\t--HUMAN WINS--")
                    break

                Logic.dobot_turn()
                
                if Logic.test_wins() is True or Logic.test_draw() == True:
                    print("\t--DOBOT WINS--")
                    break

        play_again = prompt('Do you want to play again?')

        Logic.clear_board()


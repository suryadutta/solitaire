import pprint
import random
import warnings
import numpy as np

from strategy import Game


pp = pprint.PrettyPrinter(indent = 4)
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning) 


def get_user_input():
    pay_to_play = input("\nHow much would you like to bet? Input an amount with numbers and\ndecimals only (e.g. 1.50).\n >> ")
    try:
        buyin_fee = float(pay_to_play)
    except:
        print("Unknown input. Using default value: $1.50")
        buyin_fee = 1.50
        
    see_each_move = input("\nWould you like to see each move? Y/N:\n >> ")
    if see_each_move == "Y":
        verbose = True
    elif see_each_move == "N":
        verbose = False
    else:
        print("Unknown input. Using default value: verbose = False")
        verbose = False
        
    simple_or_strategic = input("\nChoose a mode:\n1) Strategic\n2) Simple\n >> ")
    if simple_or_strategic == "1":
        turn = "strategic"
    elif simple_or_strategic == "2":
        turn = "simple"
    else:
        print("Unknown input. Using default value: strategic")
        turn = "strategic"
    
    return buyin_fee, verbose, turn

def main():
    print("--- STRATEGIC SOLITAIRE ---")
    fee, output, mode = get_user_input()

    # Set up betting info
    payout = 0
    buyin_fee = fee
    place_amount = buyin_fee * 0.3
    bonus_amount = buyin_fee * 3

    seed = 84 # Set to None for random state; 84 for win state
    random.seed(seed)
    verbose = output
    turn = mode

    play = Game()
    play.simulate(turn=turn, verbose=verbose)

    if(play.win()):
        result = 1
        payout += (52*place_amount) + bonus_amount
        print(f"\nYou won! Total winnings: {payout - buyin_fee}\n")
    else:
        result = 0
        placed = [np.sum([1 for card in play.ace_stacks[i].cards]) for i in list(play.ace_stacks.keys())]
        payout += np.sum(placed) * place_amount
        print(f"\nYou lost! Try again. Total winnings: {payout - buyin_fee}\n")

    return


if __name__ == "__main__":
    main()

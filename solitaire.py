import pprint

from gameplay import Game


pp = pprint.PrettyPrinter(indent = 4)


def main():
    play = Game()
    play.simulate(verbose = True)
    print()

    pp.pprint(play.get_game_elements())
    print()

    if(play.win()):
        print("You won!")
    else:
        print("You lost! Try again.")

    return


if __name__ == "__main__":
    main()

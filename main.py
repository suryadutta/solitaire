import pprint
pp = pprint.PrettyPrinter(indent=4)

from solitaire import Game

def main():
    thisGame = Game()
    thisGame.simulate(verbose=True)
    print()
    pp.pprint(thisGame.getGameElements())
    print()
    if(thisGame.checkIfCompleted()):
        print("Congrats! You won!")
    else:
        print("Sorry, you did not win")
    
    return
    
if __name__ == "__main__":
    main()
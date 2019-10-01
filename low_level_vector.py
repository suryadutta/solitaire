# this file should contain an implementation of a low-level state vector

# tentatively, using numpy arrays for vectors
from numpy import array

class LowLevelVector:
    # vector keeps track of its game and updates itself from the game
    #numpy array representation
    #1-4: number face-up cards in block piles
    #5-11: number face-up cards in each play pile
    def __init__(self, game):
        self.game = game
        lowLevelVector = numpy.array([0,0,0,0,1,1,1,1,1,1,1])
        self.update(self.game.getGameElements())

    def update(self, gameElements):
        # this method should update the vector according to the game elements "printout" received from self.game
        # implementation will depend on what we do for features

        blockPiles = gameElements(1)
        i=0
        for pile in blockPiles:
            self.lowLevelVector[i] = len(pile)

        # get number of flipped cards in each play pile and update
        playPiles = gameElements(2)
        i = 4
        for pile in playPiles:
            self.lowLevelVector[i] = len(pile.getFlippedCards())

        pass
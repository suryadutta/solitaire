# this file should contain an implementation of a low-level state vector

# tentatively, using numpy arrays for vectors
from numpy import array

class LowLevelVector:
    # vector keeps track of its game and updates itself from the game
    def __init__(self, game):
        self.game = game
        self.update(self.game.getGameElements())

    def update(self, gameElements):
        # this method should update the vector according to the game elements "printout" received from self.game
        # implementation will depend on what we do for features
        pass
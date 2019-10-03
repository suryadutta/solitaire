# this file should contain an implementation of a low-level state vector

# tentatively, using numpy arrays for vectors
from numpy import array
from solitaire import Game

class LowLevelVector:
    # vector keeps track of its game and updates itself from the game
    #numpy array representation
    #1-4: number face-up cards in block piles
    #5-11: number face-up cards in each play pile
    #keep corresponding weight array of feature vector size + 1
    def __init__(self, game):
        self.game = game
        lowLevelVector = numpy.array([0,0,0,0,1,1,1,1,1,1,1])
        lowLevelWeights = numpy.array([1,1,1,1,1,1,1,1,1,1,1,1])
        self.update(self.game.getGameElements())

    #update feature vector and weight array
    def update_features(self, state, action):
        # this method should update the vector according to the game elements "printout" received from self.game
        # implementation will depend on what we do for features

        next_state = state.make_move(state,action)
        gameElements = next_state.getGameElements()

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

    #TODO update weight array with gradient stuff
    def update_weights(self):
        pass

    #get Q using linear function approximation
    def get_Q(self,state,action):

        update_features(state,action)

        Q=lowLevelWeights[0]
        for i in range(lowLevelVector):
            Q += lowLevelVector[i]*lowLevelWeights[i+1]

        return Q




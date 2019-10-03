from solitaire import Game
from high_level_vector import HighLevelVector
from low_level_vector import LowLevelVector
from numpy import array
import numpy as np

class agent:

    #Function to choose what action to take next, depending on next state and epsilon
    #@return next action
    def epsilon_greedy(state,epsilon):

        #find all valid moves that can be made- some kind of vector
        possible_moves = state.getPossibleMoves()

        #get rewards corresponding to all possible moves
        #TODO - don't actually want to make the move, just get what the reward would be
        rewards=[]
        for action in possible_moves:
            rewards.append(state.make_move(state,action))

        #get random number between 1-10
        #if random number > epsilon*10 choose an action at random
        random_chance = np.random.randint(1,11)
        if random_chance > epsilon*10:
            random_choice = np.random.randint(0,len(possible_moves))
            return possible_moves[random_choice]

        #else choose move with hightest reward
        max_index = rewards.index(max(rewards))
        return possible_moves[max_index]

    """
    @param alpha- learning rate
    @param gamma - discount factor
    @param epsilon  - exploration
    @param num_games - number games for training
    @param max_moves - maximum moves until game is considered a loss
    """
    def SARSA(alpha, gamma, epsilon, num_games, max_moves,high_level):

        total_moves = []
        final_scores = []

        #possible actions
        actions=["moveBetweenPiles","moveDeckToPile","movePileToBlock","moveBlockToPile",
                 "recycleDeck","drawDeck"]

        #Get initial Q, depending on whether high or low level features
        if high_level:
            features = HighLevelVector
        else:
            features = LowLevelVector

        for game in range(num_games):

            won = False
            #print("Game number {game}")
            total_score = 0
            moves = 0

            #get initial state, action, Q, based on new game
            state = Game()
            action = epsilon_greedy(state,epsilon)
            Q = features.get_Q(state,action)

            while moves < max_moves:

                #make a move, update state and total score
                reward = state.make_move(action)
                total_score += reward
                moves += 1

                #get next action using epsilon greedy and corresponding Q
                next_action = epsilon_greedy(state,epsilon)
                next_Q = features.get_Q(state,next_action)

                #Update Q, feature weights, state, action
                Q += alpha*[reward+(gamma*next_Q-Q)]
                features.update_weights()
                action = next_action

                #If in terminal state (either won or out of moves) break out of while loop
                if next_Q == 0:
                    if game.checkIfCompleted():
                        won = True
                    break

            #Update score based off of win/loss
            if won:
                total_score += 1000
            else:
                total_score -= 1000

            total_moves.append(moves)
            final_scores.append(total_score)

        return total_moves, final_scores

    LEARNING_RATE = 0.1
    DISCOUNT_FACTOR = 0.9
    EPSILON = 0.9
    NUM_TRAINING_GAMES = 10000
    MOVE_LIMIT = 500
    HIGH_LEVEL = True

    total_moves, final_scores = SARSA(LEARNING_RATE,DISCOUNT_FACTOR,EPSILON,NUM_TRAINING_GAMES,MOVE_LIMIT,HIGH_LEVEL)

    #TODO: use total move and final score data to do some graphing / analysis

from solitaire import Game
from high_level_vector import HighLevelVector
from low_level_vector import LowLevelVector
from numpy import array
import numpy as np

class agent:

    #Function to choose what action to take next, depending on next state and epsilon
    #@return next action
    def epsilon_greedy(state,epsilon):

        #find all valid moves that can be made- returns list of action objects
        possible_moves = state.getPossibleMoves()
        rewards = []

        #get rewards corresponding to all possible moves
        for i in range(len(possible_moves)):

            #TODO can cause card flip +5 reward
            #if action is a move between piles, 0 reward
            if possible_moves[i].id == 1:
                rewards[i] = 0

            # TODO can cause card flip +5 reward
            #if action is a move from pile to block, 10 reward
            elif possible_moves[i].id == 2:
                rewards[i] = 10

            #if action is a move from block to pile, -15 reward
            elif possible_moves[i].id == 3:
                rewards[i] = -15

            #if action is draw card, 0 reward
            elif possible_moves[i].id == 4:
                rewards[i] = 0

            #if action is recycle deck, -100 reward
            elif possible_moves[i].id == 5:
                rewards[i] = -100

            #if action is move from waste to pile, 5 reward
            elif possible_moves[i].id == 6:
                rewards[i] = 5

            #if action is move from waste to block, 10 reward
            elif possible_moves[i].id == 7:
                rewards[i] = 10

        #get random number between 1-10
        #if random number > epsilon*10 choose an action at random
        random_chance = np.random.randint(1,11)
        if random_chance > epsilon*10:
            random_choice = np.random.randint(0,len(possible_moves))
            return possible_moves[random_choice]

        #else choose move with hightest reward
        #TODO decide how you want to handle if multiple actions have same max reward- pick one at random? Always choose first?
        #TODO currently index(max) takes first occurence of the max value
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
                # state automatically updates when making a move, no need to manually update value
                #TODO make sure make move method returns reward
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

                #If in terminal state (either won, can't move, or exceed move limit) break out of while loop
                if next_Q == 0 or moves >= 500:
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
    NUM_TRAINING_GAMES = 10
    MOVE_LIMIT = 500
    HIGH_LEVEL = True

    total_moves, final_scores = SARSA(LEARNING_RATE,DISCOUNT_FACTOR,EPSILON,NUM_TRAINING_GAMES,MOVE_LIMIT,HIGH_LEVEL)

    #TODO: use total move and final score data to do some graphing / analysis

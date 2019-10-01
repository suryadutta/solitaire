from solitaire import Game

class agent:
    #fill in Q with arbitrary (?) values
    #let's just do all 0's
    def init_Q():



    #I have no idea what this is going to do
    def get_Q(state,action):

        if Game.checkIfCompleted() or Game.checkIfOutOfMoves():
            return 0


    #Function to make a move given current state and action
    #@return next state and reward
    def make_move(s,a):
        return Game.make_move(s,a)

    #Function to choose what action to take next, depending on next state and epsilon
    #@return next action
    def epsilon_greedy(s,epsilon):

        #find all valid moves that can be made- some kind of vector
        possible_moves = Game.getPossibleMoves()

        #get rewards corresponding to all possible moves
        #choose move with hightest reward

        #do random move 1-epsilon % of the time


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

        #initialize Q as a matrix (?) size num actions x num states in vector
        Q = init_Q()

        for game in range(num_games):

            won = False
            #print("Game number {game}")
            total_score = 0
            moves = 0

            #get initial state based on new game
            state = Game.newGame(high_level)
            action = epsilon_greedy(state,epsilon)
            Q = get_Q(state,action)

            while moves < max_moves:

                #make a move, update state and total score
                reward, next_state = make_move(state,action)
                total_score += reward
                moves += 1

                next_action = epsilon_greedy(next_state,epsilon)
                next_Q = get_Q(next_state,next_action)

                #Update Q, state, action
                Q += alpha*[reward+(gamma*next_Q-Q)]
                state = next_state
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

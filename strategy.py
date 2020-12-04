import pprint
import random
import numpy as np

from setup import Card, Deck, Stack


class Game:

    values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    suits = { # Keys are unicode symbols for suits.
        u'\u2660': "black", # Spade
        u'\u2661': "red", # Hearts
        u'\u2663': "black", # Clubs
        u'\u2662': "red", # Diamonds
    }

    def __init__(self):
        """Initialize the Game class.
        """
        self.moves = 0
        
        # Instantiate the Deck.
        self.deck = Deck(self.values, self.suits)

        # Instantiate the Stacks.
        self.play_stacks = []

        # For each of the seven stacks...
        for i in range(7):
            this_stack = Stack()
            # ...take the first card from the Deck without flipping it and add
            # it to the current stack by inserting it into the first position.
            # The first stack will have 1 card, the second 2...the last, 7.
            [this_stack.add_card(self.deck.take_first_card(flip=False))
             for j in range(i + 1)]
            # Flip the topmost card in the stack.
            this_stack.flip_first_card()
            # Add the populated stack to the list of playable stacks.
            self.play_stacks.append(this_stack)

        # Populate the four Ace stacks.
        self.ace_stacks = {suit: Stack() for suit in self.suits}

        # Flip the first card in the Deck.
        self.deck.cards[0].flip()

    def show_board(self):
        board = {
            "deck": str(self.deck),
            "stacks": [str(stack) for stack in self.play_stacks],
            "ace stacks": {suit: str(stack) for suit, stack in
                           self.ace_stacks.items()}
        }
        return board

    def check_card_order(self, higher, lower):
        """Determine whether or not two cards can be placed consecutively. Make
        sure that both cards are of differing suits with suits_different. Then,
        ensure that the cards are consecutive with values_consecutive by check-
        ing that the value of the higher card is exactly one more than the
        value of the lower one. If both criteria are met, then the card order
        is allowed.
        """
        suits_different = self.suits[higher.suit] != self.suits[lower.suit]
        values_consecutive = self.values[self.values.index(higher.value)
                                        - 1] == lower.value
        return suits_different and values_consecutive

    def win(self):
        """Determine when the game is won. Deck must be empty, stacks must be
        empty, and Ace stacks must be full.
        """
        deck_empty = len(self.deck.cards) == 0
        stacks_empty = all(len(stack.cards) == 0 for stack in self.play_stacks)
        aces_full = all(len(stack.cards) == 13 for suit,
                        stack in self.ace_stacks.items())
        return deck_empty and stacks_empty and aces_full

    def add_to_ace_stack(self, card):
        """See if the current card can be added to the corresponding Ace stack.
        """
        if card is None: # do nothing if there is no current card
            return False
        # If there are cards in the Ace stack...
        elif len(self.ace_stacks[card.suit].cards) > 0:
            # ...get the value of topmost card.
            highest_value = self.ace_stacks[card.suit].cards[0].value
            # Check if value of the current card is higher than the topmost.
            if self.values[self.values.index(highest_value) + 1] == card.value:
                # If so, play the card to the corresponding Ace stack.
                self.ace_stacks[card.suit].cards.insert(0, card)
                return True
        else:
            return False
    
    def play_strategy_one(self, verbose=False):
        """Always play an Ace or Deuce wherever you can immediately.
        """
        card_added = self.deck.get_first_card()
        
        #--- 1.1 Always play an Ace wherever you can immediately. ---#
        
        # Play an Ace from the deck to its own stack.
        if card_added is not None and card_added.value == "A":
            card_added = self.deck.take_first_card()
            self.ace_stacks[card_added.suit].cards.insert(0, card_added)
            if verbose == True:
                    print(f"Move {self.moves}: Play {str(card_added)} from deck to Ace stack")
            return True
        
        # Play an Ace from the board to its own stack.
        for stack in np.random.permutation(self.play_stacks):
            if len(stack.cards) > 0 and stack.cards[0].value == "A":
                card_added = stack.cards.pop(0)
                self.ace_stacks[card_added.suit].cards.insert(0, card_added)
                if verbose == True:
                    print(f"Move {self.moves}: Play {str(card_added)} from board to Ace stack")
                return True
        
        #--- 1.2 Always play a Deuce wherever you can immediately. ---#
        
        # Play a Deuce from the deck to an Ace stack.
        if card_added is not None and card_added.value == "2":
            if self.add_to_ace_stack(self.deck.get_first_card()):
                card_added = self.deck.take_first_card()
                if verbose == True:
                    print(f"Move {self.moves}: Play {str(card_added)} from deck to Ace stack")
                return True

        # Play a Deuce from the board to an Ace stack.
        for stack in np.random.permutation(self.play_stacks):
            if len(stack.cards) > 0 and stack.cards[0].value == "2":
                if self.add_to_ace_stack(stack.cards[0]):
                    card_added = stack.cards.pop(0)
                    if verbose == True:
                        print(f"Move {self.moves}: Play {str(card_added)} from board to Ace stack")
                    return True
        return False
    
    def play_strategy_two(self, verbose=False):
        """Always make the play or transfer that frees (or allows a play that frees) a downcard,
        regardless of any other considerations. To debug, use seed=7. all_face_ups helps to implement strategy
        three.
        """
        all_face_ups = [(self.suits[stack.get_face_up_cards()[-1].suit], stack.get_face_up_cards()[-1].value) if len(stack.get_face_up_cards()) > 0 else ('', '') for stack in self.play_stacks]
        
        # For each stack in the deck...
        for index, stack in enumerate(np.random.permutation(self.play_stacks)):
            # ...get the number of face down cards.
            stack_face_up = stack.get_face_up_cards()
            num_stack_face_down = len(stack.cards) - len(stack_face_up)

            if num_stack_face_down > 0:
                stack_first_face_up = (self.suits[stack_face_up[-1].suit], stack_face_up[-1].value)
                
                # If there's only one card on it, check if it can be played to an ace stack.
                if len(stack_face_up) == 1 and self.add_to_ace_stack(stack_face_up[0]):
                        card_added = stack.cards.pop(0)
                        if verbose == True:
                            print(f"Move {self.moves}: Play {str(card_added)} from board to Ace stack")
                        return True
                # Else, try to move the stack somewhere else.
                else:
                    # Check all the available stacks.
                    for pile in np.random.permutation(self.play_stacks):
                        # Get all the face_up cards in the pile.
                        pile_face_up = pile.get_face_up_cards()
                        # Skip the current stack.
                        if pile is not stack and len(pile_face_up) > 0:
                            cards_to_move = stack_face_up[:len(stack_face_up)]
                            # If the card can be moved
                            if self.check_card_order(pile.cards[0], cards_to_move[-1]):
                                # Check if there's an alternative
                                locs = np.where([i == stack_first_face_up for i in all_face_ups])[0]
                                # If there's a better alternative, skip this stack since we'll reach the better
                                # choice as the loop continues
                                if len(locs) == 2 and not self.play_strategy_three(stack, self.play_stacks[locs[-1]]):
                                    break
                                else:
                                    if verbose == True:
                                        print("Stack:", [(card.suit, card.value) for card in stack_face_up], "\nPile:",  [(card.suit, card.value) for card in pile_face_up])
                                        print("Cards to move:", [(card.suit, card.value) for card in cards_to_move])
                                    [pile.cards.insert(0, card) for card in reversed(cards_to_move)]
                                    stack.cards = stack.cards[len(cards_to_move):]
                                    if verbose == True:
                                        print(f"Move {self.moves}: Move {len(cards_to_move)} cards between piles")
                                    return True
        return False

    def play_strategy_three(self, chosen_stack, alternate_stack):
        """When faced with a choice, always make the play or transfer that frees (or allows a play that frees)
        the downcard from the biggest pile of downcards. To debug, use seed=3.
        """
        chosen_stack_face_down = len(chosen_stack.cards) - len(chosen_stack.get_face_up_cards())
        alternate_stack_face_down = len(alternate_stack.cards) - len(alternate_stack.get_face_up_cards())
        return chosen_stack_face_down >= alternate_stack_face_down
    
    def play_strategy_four(self, cards):
        """Transfer cards from column to column only to allow a downcard to be freed or to make the columns
        smoother. To debug, use seed=1.
        """
        # Return the suits of the given cards.
        return [(card.suit, card.value) for card in cards[1::2]]
    
    def play_strategy_five(self, verbose=False):
        """Don't clear a spot unless there's a King IMMEDIATELY waiting to occupy it. To debug, use seed=1.
        """
        king_waiting = self.play_strategy_six()
        
        if king_waiting:
        
            for index, stack in enumerate(np.random.permutation(self.play_stacks)):
                stack_face_up = stack.get_face_up_cards()
                num_stack_face_down = len(stack.cards) - len(stack_face_up)
                # If the stack is already empty
                if num_stack_face_down == 0 and len(stack_face_up) == 0:
                    if king_waiting < 0:
                        card_added = self.deck.take_first_card()
                        stack.add_card(card_added)
                        if verbose == True:
                            print(f"Move {self.moves}: Move {str(card_added)} from deck to empty stack")
                        return True
                    else:
                        cards_to_move = self.play_stacks[king_waiting].get_face_up_cards()
                        # Move to empty stack
                        [stack.cards.insert(0, card) for card in reversed(cards_to_move)]
                        self.play_stacks[king_waiting].cards = self.play_stacks[king_waiting].cards[len(cards_to_move):]
                        if verbose == True:
                            print(f"Move {self.moves}: Move cards from board to empty stack")
                        return True
                # If there's only one card in the stack
                elif num_stack_face_down == 1 and len(stack_face_up) == 1:
                    if self.add_to_ace_stack(stack_face_up[0]):
                            card_added = stack.cards.pop(0)
                            if verbose == True:
                                print(f"Move {self.moves}: Play {str(card_added)} from board to Ace stack")
                            return True
                # If all cards in the stack are face up
                elif num_stack_face_down == 0 and len(stack_face_up) > 0:
                    #print([(card.suit, card.value) for card in stack.cards])
                    # Clear the spot
                    options = []
                    for pile in self.play_stacks:
                        # See if the card can be transfered
                            pile_face_up = pile.get_face_up_cards()
                            # Skip the working stack
                            if pile is not stack and len(pile_face_up) > 0:
                                cards_to_move = stack_face_up[:len(stack_face_up)]
                                if self.check_card_order(pile.cards[0], cards_to_move[-1]):
                                    options.append(pile)
                                    #print("Stack:", [(card.suit, card.value) for card in stack_face_up], "\nPile:",  [(card.suit, card.value) for card in pile_face_up])
                                    #print("Cards to move:", [(card.suit, card.value) for card in cards_to_move])
                                    #smooth_partners = self.play_strategy_four(pile_face_up)
                                    #print("Smooth partners:", smooth_partners)
                    #print(options)
                    for pile in options:
                        pile_face_up = pile.get_face_up_cards()                    
                        smooth_partners = self.play_strategy_four(pile_face_up)
                        cards_to_move = stack_face_up[:len(stack_face_up)]
                        if np.all([cards_to_move[-1].suit == suit for suit in smooth_partners]):
                            #print("Chosen:", [(card.suit, card.value) for card in pile_face_up])
                            [pile.cards.insert(0, card) for card in reversed(cards_to_move)]
                            stack.cards = stack.cards[len(cards_to_move):]
                            if verbose == True:
                                print(f"Move {self.moves}: Move {len(cards_to_move)} cards between piles")
                            if king_waiting < 0:
                                card_added = self.deck.take_first_card()
                                stack.add_card(card_added)
                                if verbose == True:
                                    print(f"Move {self.moves}: Move {str(card_added)} from deck to empty stack")
                                return True
                            else:
                                cards_to_move = self.play_stacks[king_waiting].get_face_up_cards()
                                # Move to empty stack
                                [stack.cards.insert(0, card) for card in reversed(cards_to_move)]
                                self.play_stacks[king_waiting].cards = self.play_stacks[king_waiting].cards[len(cards_to_move):]
                                if verbose == True:
                                    print(f"Move {self.moves}: Move cards from board to empty stack")
                                return True
        return False
    
    def play_strategy_six(self):
        """Only play a King that will benefit the column(s) with the biggest pile of downcards, unless the
        play of another King will at least allow a transfer that frees a downcard. best_king implements
        strategy three.
        """
        # Check the board for a King
        king_loc = 0
        best_king = 0
        
        for index, stack in enumerate(self.play_stacks):
            stack_face_up = stack.get_face_up_cards()
            num_stack_face_down = len(stack.cards) - len(stack_face_up)
            # If all cards in the stack are face up
            if num_stack_face_down > 0 and len(stack_face_up) > 0:
                # Check that there's a waiting King and choose the one with the biggest num cards face down
                if "K" in [(card.value) for card in stack_face_up] and num_stack_face_down > best_king:
                    best_king = num_stack_face_down
                    #king_waiting = stack_face_up
                    # print(index, [(card.suit, card.value) for card in king_waiting])
                    king_loc = index
        
        # Check the deck for a king
        if self.deck.get_first_card() is not None and self.deck.get_first_card().value == "K":
            king_loc = -1
        
        return king_loc
    
    def play_strategy_seven(self, verbose=False):
        """Only build your Ace stacks (with anything other than an Ace or Deuce) when the following apply:
            1) The move WILL NOT interfere with Next Card Protection
            2) The move WILL allow a play or transfer that frees a downcard
                - Criteria satisfied in play_strategy_two()
            3) The move WILL open up a space for a same-suit card pile transfer to free a downcard
            4) The move WILL clear a spot for an IMMEDIATE Waiting King
        To debug, use seed=5.
        """        
        # 1) The move WILL NOT interfere with Next Card Protection (play from the board)
        for stack in np.random.permutation(self.play_stacks):
            # If there are cards in the stack and the topmost card can be
            # added to its corresponding Ace stack...
            if len(stack.cards) > 0 and self.next_card_protection(stack.cards[0], current_stack=stack):
                if self.add_to_ace_stack(stack.cards[0]):
                    card_added = stack.cards.pop(0)
                    if verbose == True:
                        print(f"Move {self.moves}: Play {str(card_added)} from board to Ace stack")
                    return True

        # 1) The move WILL NOT interfere with Next Card Protection (play from the deck)
        card_to_add = self.deck.get_first_card()
        if self.next_card_protection(card_to_add):
            if self.add_to_ace_stack(card_to_add):
                card_added = self.deck.take_first_card()
                if verbose == True:
                    print(f"Move {self.moves}: Play {str(card_added)} from deck to Ace stack")
                return True
                
    def next_card_protection(self, card_to_add, current_stack=None):
        """Wait to build the Ace stack until all of these criteria are met. Note that enabling this may
        cause previously winning hands to lose. To debug, use seed=5 or seed=1.
        """
        # Turn off to debug
        disable = False
        
        if card_to_add is not None:
            next_lowest = Game.values.index(card_to_add.value) - 1
        
            # Check if there's another card with the same value on the board
            one_on_board = []
            for stack in self.play_stacks:
                if current_stack and stack is not current_stack:
                    one_on_board.append([(card.suit, card.value) for card in stack.get_face_up_cards() if (card.value == card_to_add.value and Game.suits[card.suit] == Game.suits[card_to_add.suit])])
            criteria1 = any(one_on_board)

            # Check if both next lowest cards of opposite suit are on the board
            both_on_board = []
            for stack in self.play_stacks:
                if current_stack and stack is not current_stack:
                    both_on_board.append([(card.suit, card.value) for card in stack.get_face_up_cards() if (card.value == Game.values[next_lowest] and Game.suits[card.suit] != Game.suits[card_to_add.suit])])
            criteria2 = np.count_nonzero(both_on_board) == 2

            # Check if both next lowest cards of opposite suit are in ace stacks
            both_in_aces = []
            for i in list(self.ace_stacks.keys()):
                both_in_aces.append([(card.suit, card.value) for card in self.ace_stacks[i].get_face_up_cards() if card.value == Game.values[next_lowest] and Game.suits[card.suit] != Game.suits[card_to_add.suit]])
            criteria3 = np.count_nonzero(both_in_aces) == 2
        
            return any([criteria1, criteria2, criteria3, disable])
    
    def play_strategy_eight(self, verbose=False):
        """DON'T PLAY OR TRANSFER A 5, 6, 7, OR 8 ANYWHERE UNLESS AT LEAST ONE OF THE FOLLOWING WILL APPLY:
            1) The card will be smooth with it's next highest even/odd partner in the column
            2) The move will allow a play or transfer that will IMMEDIATELY free a downcard
                - Criteria satisfied in play_strategy_two()
            3) There have not been any other cards already played to the column
            4) You have ABSOLUTELY no other choice but to continue playing (this is not a good sign)
        To debug, use seed=1.
        """
        card_to_add = self.deck.get_first_card()
        
        # Wait to play 5s, 6s, 7s and 8s from deck
        if card_to_add is not None and card_to_add.value in ['5', '6', '7', '8']:
            for stack in np.random.permutation(self.play_stacks):
                # For each non-empty stack...
                if len(stack.cards) > 0:
                    stack_face_up = stack.get_face_up_cards()
                    # 1) The card will be smooth with it's next highest even/odd partner in the column
                    if len(stack_face_up) > 1:
                        smooth_partners = self.play_strategy_four(stack_face_up)
                        if card_to_add.suit == smooth_partners[0][0]:
                            if self.check_card_order(stack.cards[0], card_to_add):
                                card_added = self.deck.take_first_card()
                                stack.add_card(card_added)
                                if verbose == True:
                                    print(f"Move {self.moves}: Play {str(card_added)} from deck to board")
                                return True
                    # 3) There have not been any other cards already played to the column
                    elif len(stack_face_up) == 1:
                        # ...check that the cards are in an allowable order.
                        if self.check_card_order(stack.cards[0], card_to_add):
                            #Add the card to the stack.
                            card_added = self.deck.take_first_card()
                            stack.add_card(card_added)
                            if verbose == True:
                                print(f"Move {self.moves}: Play {str(card_added)} from deck to board")
                            return True
                    # 4) You have ABSOLUTELY no other choice to continue playing
                    else:
                        if self.check_card_order(stack.cards[0], card_to_add):
                        # Add the card to the stack.
                            card_added = self.deck.take_first_card()
                            stack.add_card(card_added)
                            if verbose == True:
                                print(f"Move {self.moves}: Play {str(card_added)} from deck to board")
                            return True
        # Otherwise, immediately play any eligible cards from the deck
        elif card_to_add is not None:
            for stack in np.random.permutation(self.play_stacks):
                # For each non-empty stack...
                if len(stack.cards) > 0:
                    # ...check that the cards are in an allowable order.
                    if self.check_card_order(stack.cards[0], card_to_add):
                        # Add the card to the stack.
                        card_added = self.deck.take_first_card()
                        stack.add_card(card_added)
                        if verbose == True:
                            print(f"Move {self.moves}: Play {str(card_added)} from deck to board")
                        return True
    
    def play_strategy_nine(self, verbose=False):
        """When you get to a point that you think all of your necessary cards are covered and you can't just
        get to them, IMMEDIATELY play ANY CARDS YOU CAN to their appropriate Ace stacks. You may have to
        rearrange existing piles to allow blocked cards freedom to be able to go to their Ace stack. Hopefully
        this will clear an existing pile up to the point that you can use an existing pile upcard to
        substitute for the necessary covered card.
        """
        #1: Check if there are any cards that are playable to an Ace stack.
        for stack in np.random.permutation(self.play_stacks):
            # If there are cards in the stack and the topmost card can be
            # added to its corresponding Ace stack...
            if len(stack.cards) > 0 and self.add_to_ace_stack(stack.cards[0]):
                card_added = stack.cards.pop(0)
                if verbose == True:
                    print(f"Move {self.moves}: Play {str(card_added)} from board to Ace stack")
                return True

        #2: Check if any cards in the deck are playable to an Ace stack.
        if self.add_to_ace_stack(self.deck.get_first_card()):
            card_added = self.deck.take_first_card()
            if verbose == True:
                    print(f"Move {self.moves}: Play {str(card_added)} from deck to Ace stack")
            return True
        
        #5: Move cards around playable stacks.
        # For each stack on the board...
        for stack in np.random.permutation(self.play_stacks):
            # ...get all the face_up cards in that stack.
            stack_face_up = stack.get_face_up_cards()
            # If there are face_up cards in the stack...
            if len(stack_face_up) > 0:
                # ...check every other playable stack.
                for pile in np.random.permutation(self.play_stacks):
                    # Get all the face_up cards in the pile.
                    pile_face_up = pile.get_face_up_cards()
                    # If there are face_up cards in a different stack...
                    if pile is not stack and len(pile_face_up) > 0:
                        # ...choose how many cards to move.
                        for num_cards_to_move in range(1,len(stack_face_up) + 1):
                            cards_to_move = stack_face_up[:num_cards_to_move]
                            # Check if the card order is allowable.
                            if self.check_card_order(pile.cards[0],cards_to_move[-1]):
                                stack_face_down = len(stack.cards) - len(stack_face_up)
                                pile_face_down = len(pile.cards) - len(pile_face_up)
                                if pile_face_down < stack_face_down:
                                    [pile.cards.insert(0, card) for card in reversed(cards_to_move)]
                                    stack.cards = stack.cards[num_cards_to_move:]
                                    if verbose == True:
                                        print(f"Move {self.moves}: Move {num_cards_to_move} cards between piles")
                                    return True
                                elif stack_face_down == 0 and len(cards_to_move) == len(stack.cards):
                                    [pile.cards.insert(0, card) for card in reversed(cards_to_move)]
                                    stack.cards = []
                                    if verbose == True:
                                        print(f"Move {self.moves}: Move {num_cards_to_move} cards between piles")
                                    return True
                                else:
                                    # See if the move will free a card to an Ace stack
                                    next_up = stack_face_up[num_cards_to_move]
                                    next_lowest = Game.values.index(next_up.value) - 1
                                    result = np.count_nonzero([card for card in self.ace_stacks[next_up.suit].get_face_up_cards() if card.value == Game.values[next_lowest]])
                                    if result:
                                        [pile.cards.insert(0, card) for card in reversed(cards_to_move)]
                                        stack.cards = stack.cards[num_cards_to_move:]
                                        if verbose == True:
                                            print(f"Move {self.moves}: Move {num_cards_to_move} cards between piles")
                                        return True

            
    def take_strategic_turn(self, verbose=False):
        
        #0: Flip any face_down cards at the end of the stack.
        [stack.cards[0].flip() for stack in self.play_stacks if len(stack.cards) > 0 and not stack.cards[0].flipped]
        
        if self.play_strategy_one(verbose=verbose):
            return True
        
        if self.play_strategy_two(verbose=verbose):
            return True
        
        if self.play_strategy_five(verbose=verbose):
            return True
        
        if self.play_strategy_seven(verbose=verbose):
            return True
        
        if self.play_strategy_eight(verbose=verbose):
            return True
        
        if self.play_strategy_nine(verbose=verbose):
            return True
        
        return False
    
    def take_simple_turn(self, verbose=False):
        """The possible actions for each turn is as follows:

        1. Make sure first card in each play pile is flipped up
        2. Move any eligible cards to the block piles
        3. If possible, move any kings to any empty play pile
        4. If possible, add drawn card to a play pile
        5. Permute flipped up cards in the play piles to see if any of them can
        be switched around. Only move cards between play piles if the number of
        cards faced down in the old pile is more than the number of cards face
        down in the new pile.
        6. Draw new card

        The algorithm will pick the first item on the list that is successful,
        and restart from the top on the next turn.
        """

        #0: Flip any face_down cards at the end of the stack.
        [stack.cards[0].flip() for stack in self.play_stacks if len(
            stack.cards) > 0 and not stack.cards[0].flipped]

        #1: Check if there are any cards that are playable to an Ace stack.
        for stack in self.play_stacks:
            # If there are cards in the stack and the topmost card can be
            # added to its corresponding Ace stack...
            if len(stack.cards) > 0 and self.add_to_ace_stack(stack.cards[0]):
                card_added = stack.cards.pop(0)
                if verbose == True:
                    print(f"Move {self.moves}: Play {str(card_added)} from board to Ace stack")
                return True

        #2: Check if any cards in the deck are playable to an Ace stack.
        if self.add_to_ace_stack(self.deck.get_first_card()):
            card_added = self.deck.take_first_card()
            if verbose == True:
                    print(f"Move {self.moves}: Play {str(card_added)} from deck to Ace stack")
            return True

        #3: Move Kings to open stacks.
        for stack in self.play_stacks:
            # If there are no cards in the stack...
            if len(stack.cards) == 0:
                # ...first, check all of the other stacks...
                for pile in self.play_stacks:
                    # ...for a King.
                    if len(pile.cards) > 1 and pile.cards[0].value == "K":
                        card_added = pile.cards.pop(0)
                        # Place the King in the empty stack.
                        stack.add_card(card_added)
                        if verbose == True:
                            print(f"Move {self.moves}: Move {str(card_added)} to empty stack")
                        return True
                # Then, check the deck for a King.
                if self.deck.get_first_card() is not None and self.deck.get_first_card().value == "K":
                    card_added = self.deck.take_first_card()
                    stack.add_card(card_added)
                    if verbose == True:
                        print(f"Move {self.moves}: Play {str(card_added)} from deck to empty stack")
                    return True

        #4: Add drawn card to playable stack.
        for stack in self.play_stacks:
            # For each non-empty stack...
            if len(stack.cards) > 0 and self.deck.get_first_card() is not None:
                # ...check that the cards are in an allowable order.
                if self.check_card_order(stack.cards[0],
                                         self.deck.get_first_card()):
                    # Add the card to the stack.
                    card_added = self.deck.take_first_card()
                    stack.add_card(card_added)
                    if verbose == True:
                        print(f"Move {self.moves}: Play {str(card_added)} from deck to board")
                    return True

        #5: Move cards around playable stacks.
        # For each stack on the board...
        for stack in self.play_stacks:
            # ...get all the face_up cards in that stack.
            stack_face_up = stack.get_face_up_cards()
            # If there are face_up cards in the stack...
            if len(stack_face_up) > 0:
                # ...check every other playable stack.
                for pile in self.play_stacks:
                    # Get all the face_up cards in the pile.
                    pile_face_up = pile.get_face_up_cards()
                    # If there are face_up cards in a different stack...
                    if pile is not stack and len(pile_face_up) > 0:
                        # ...choose how many cards to move.
                        for num_cards_to_move in range(1,
                                                       len(pile_face_up) + 1):
                            cards_to_move = stack_face_up[:num_cards_to_move]
                            # Check if the card order is allowable.
                            if self.check_card_order(pile.cards[0],
                                                     cards_to_move[-1]):
                                stack_face_down = len(stack.cards) - len(
                                    stack_face_up)
                                pile_face_down = len(pile.cards) - len(
                                    pile_face_up)
                                if pile_face_down < stack_face_down:
                                    [pile.cards.insert(
                                        0, card) for card in reversed(
                                            cards_to_move)]
                                    stack.cards = stack.cards[num_cards_to_move:]
                                    if verbose == True:
                                        print(f"Move {self.moves}: Move {num_cards_to_move} cards between piles")
                                    return True
                                elif stack_face_down == 0 and len(
                                    cards_to_move) == len(stack.cards):
                                    [pile.cards.insert(
                                        0, card) for card in reversed(
                                            cards_to_move)]
                                    stack.cards = []
                                    if verbose == True:
                                        print(f"Move {self.moves}: Move {num_cards_to_move} cards between piles")
                                    return True
        return False
    
    def simulate(self, draw=False, turn="strategic", verbose=False):
        pp = pprint.PrettyPrinter(indent = 4)

        if verbose==True:
            print()
            pp.pprint(self.show_board())
            print(); print()
            
        # Clear cache if last turn wasn't a card draw.
        if not draw:
            self.deck.cache = []

        # Take a turn.
        if turn == "simple":
            turn_result = self.take_simple_turn(verbose=verbose)
        else:
            turn_result = self.take_strategic_turn(verbose=verbose)
        
        # If the turn was successful, take another.
        if turn_result:
            self.moves += 1
            self.simulate(verbose=verbose)

        else:
            self.moves += 1
            # Try to draw from deck.
            if len(self.deck.cards) > 0:
                current_card = self.deck.cards[0]

                if current_card in self.deck.cache:
                    if verbose == True:
                        print("No more moves left!")
                        print(f"Moves: {self.moves}")
                    return

                else:
                    self.deck.draw_card()
                    if verbose == True:
                        print(f"Move {self.moves}: Draw a card")
                    self.deck.cache.append(current_card)
                    return self.simulate(draw=True, verbose=verbose)

            else:
                if verbose == True:
                    print("No more moves left!")
                    print(f"Moves: {self.moves}")
                return

from setup import Card, Stack, Deck


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

    def get_game_elements(self):
        object = {
            "deck": str(self.deck),
            "stacks": [str(stack) for stack in self.play_stacks],
            "ace stacks": {suit: str(stack) for suit, stack in
                           self.ace_stacks.items()}
        }
        return object

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
            # Immediately play any Ace to its corresponding stack.
            if card.value == "A":
                self.ace_stacks[card.suit].cards.insert(0, card)
                return True
            else:
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
                return True

        #2: Check if any cards in the deck can be added.
        if self.add_to_ace_stack(self.deck.get_first_card()):
            card_added = self.deck.take_first_card()
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
                        return True
                # Then, check the deck for a King.
                if self.deck.get_first_card() is not None and self.deck.get_first_card().value == "K":
                    card_added = self.deck.take_first_card()
                    stack.add_card(card_added)
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
                                    return True
                                elif stack_face_down == 0 and len(
                                    cards_to_move) == len(stack.cards):
                                    [pile.cards.insert(
                                        0, card) for card in reversed(
                                            cards_to_move)]
                                    stack.cards = []
                                    return True
        return False

    def simulate(self, draw=False, verbose=False):
        # Clear cache if last turn wasn't a card draw.
        if not draw:
            self.deck.cache = []

        # Take a turn.
        turn_result = self.take_simple_turn(verbose=verbose)

        # If the turn was successful, take another.
        if turn_result:
            self.simulate(verbose=verbose)

        else:
            # Try to draw from deck.
            if len(self.deck.cards) > 0:
                current_card = self.deck.cards[0]

                if current_card in self.deck.cache:
                    print("No more moves left!")
                    return

                else:
                    self.deck.draw_card()
                    self.deck.cache.append(current_card)
                    return self.simulate(draw=True, verbose=verbose)

            else:
                print("No more moves left!")
                return










# TODO: allow player to take stupid or strategic turn
# TODO: update main file to allow the above

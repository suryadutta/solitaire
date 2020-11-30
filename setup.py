import random

class Card:

    def __init__(self, suit, value):
        """Initialize the Card class. Each card belongs to a suit, has
        a value, and can be flipped or not.
        """
        self.suit = suit
        self.value = value
        self.flipped = False

    def flip(self):
        """Flip a card. If a card is currently face_down, set it to face_up,
        and vice versa.
        """
        self.flipped = not self.flipped

    def __str__(self):
        """Return the suit and value of a card, e.g. "3 of ♠".
        """
        return(f"{self.value} of {self.suit}")


class Stack:

    def __init__(self):
        """Initialize the Stack class.
        """
        self.cards = []

    def add_card(self, Card):
        """Add a card to a stack. Inserts the card into the first position.
        """
        self.cards.insert(0, Card)

    def flip_first_card(self):
        """Flip the first card in the stack if there are cards in the stack.
        """
        if len(self.cards) > 0:
            self.cards[0].flip()

    def get_face_up_cards(self):
        """Return the cards in the stack that are currently face_up.
        """
        return [card for card in self.cards if card.flipped]

    def __str__(self):
        """Return the current stack as the number of face_down cards and then
        each face_up card by value and suit.
        """
        returned_cards = [str(card) for card in reversed(
            self.get_face_up_cards())]
        face_down_count = len(self.cards) - len(self.get_face_up_cards())
        if face_down_count > 0:
            returned_cards.insert(0, f"{face_down_count} cards face down.")
        return ", ".join(returned_cards)


class Deck:

    def __init__(self, values, suits):
        self.cards = []
        self.cache = []
        self.populate(values, suits)
        self.shuffle()

    def __str__(self):
        return ", ".join([str(card) for card in self.cards])

    def populate(self, values, suits):
        for suit in suits:
            for value in values:
                this_card = Card(suit, value)
                self.cards.append(this_card)

    def shuffle(self):
        random.shuffle(self.cards)

    def get_first_card(self):
        if len(self.cards) > 0:
            return self.cards[0]
        else:
            return None

    def take_first_card(self, flip=True):
        if len(self.cards) > 0:
            next_card = self.cards.pop(0)
            if flip and len(self.cards) > 0:
                self.cards[0].flip()
            return next_card
        else:
            return None

    def draw_card(self):
        if len(self.cards) > 0:
            self.cards[0].flip()
            self.cards.append(self.cards.pop(0))
            self.cards[0].flip()

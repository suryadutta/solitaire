# action type

# actions have card(s) (a list), a current pile, and a target pile (no spot number needed since it's always spot 0)

class Action:

    def __init__(self, cards, pile, target):
        self.card = cards
        self.pile = pile
        self.target = target



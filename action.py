# action type

# actions have card(s) (a list), a current pile, a target pile (no spot number needed since it's always spot 0), and an ID

#ID:
#1. moveBetweenPiles
#2. movePileToBlock
#3. moveBlockToPile
#4. drawCard
#5. recycleDeck
#6. wasteToPile
#7. wasteToBlock

class Action:

    def __init__(self, cards, pile, target,id):
        self.card = cards
        self.pile = pile
        self.target = target
        self.id = id
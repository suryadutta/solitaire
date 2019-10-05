from card_elements import Card, Deck, Pile
from action import Action

class Game:

    values = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]

    suits = { #keys are unicode symbols for suits
        u'\u2660': "black",
        u'\u2665': "red",
        u'\u2663': "black",
        u'\u2666': "red",
    }

    numPlayPiles = 7

    def __init__(self):
        self.deck = Deck(self.values, self.suits)
        self.playPiles = []
        for i in range(self.numPlayPiles):
            thisPile = Pile()
            [thisPile.addCard(self.deck.takeFirstCard(flip=False)) for j in range(i + 1)]
            thisPile.flipFirstCard()
            self.playPiles.append(thisPile)
        self.blockPiles = {suit: Pile() for suit in self.suits}
        self.trashPileUp = []
        self.trashPileDown = [self.deck.takeFirstCard(flip=False) for i in range(0, len(self.deck.cards))]

    def getGameElements(self):
        returnObject = {
            "playPiles": [str(pile) for pile in self.playPiles],
            "blockPiles": {suit: str(pile) for suit, pile in self.blockPiles.items()},
            "trash pile up": ", ".join([str(card) for card in self.trashPileUp]),
            "trash pile down": ", ".join([str(card) for card in self.trashPileDown])
        }
        return returnObject

    def checkCardOrder(self,higherCard,lowerCard):
        suitsDifferent = self.suits[higherCard.suit] != self.suits[lowerCard.suit]
        valueConsecutive = self.values[self.values.index(higherCard.value)-1] == lowerCard.value
        return suitsDifferent and valueConsecutive

    def checkIfCompleted(self):
        deckEmpty = len(self.deck.cards)==0
        pilesEmpty = all(len(pile.cards)==0 for pile in self.playPiles)
        blocksFull = all(len(pile.cards)==13 for suit,pile in self.blockPiles.items())
        return deckEmpty and pilesEmpty and blocksFull

    def addToBlock(self, card):
        if card is None:
            return False
        elif len(self.blockPiles[card.suit].cards)>0:
            highest_value = self.blockPiles[card.suit].cards[0].value
            if self.values[self.values.index(highest_value)+1] == card.value:
                self.blockPiles[card.suit].cards.insert(0,card)
                return True
            else:
                return False
        else:
            if card.value=="A":
                self.blockPiles[card.suit].cards.insert(0,card)
                return True
            else:
                return False


    ######################Katy's additions###############################
    def canAddToBlock(self, card):
        """Check whether we can add the card to the block, without actually doing it. If it can be moved, return target pile."""
        if card is None:
            return False
        elif len(self.blockPiles[card.suit].cards) > 0:
            highest_value = self.blockPiles[card.suit].cards[0].value
            if self.values[self.values.index(highest_value) + 1] == card.value:
                return self.blockPiles[card.suit]
            else:
                return False
        else:
            if card.value == "A":
                return self.blockPiles[card.suit]
            else:
                return False

    def canMoveBlockToPile(self, card):
        moves = []
        if card is None:
            return False
        for pile in self.playPiles:
            if len(pile.cards)>0:
                if self.checkCardOrder(pile.cards[0], card):
                    moves.append(pile)
        if len(moves) > 0:
            return moves
        else:
            return False




    ##################End Katy's additions###############################


    def takeTurn(self, verbose=False):

        #1: check if there are any play pile cards you can play to block piles
        for pile in self.playPiles:
            if len(pile.cards) > 0 and self.addToBlock(pile.cards[0]):
                card_added = pile.cards.pop(0)
                if len(pile.cards) > 0 and not pile.cards[0].flipped:
                    pile.cards[0].flip()
                if verbose:
                    print("Adding play pile card to block: {0}".format(str(card_added)))
                return True

        #2: check if cards in deck can be added
        if len(self.trashPileUp) > 0 and self.addToBlock(self.trashPileUp[-1]):
            card_added = self.trashPileUp[-1]
            self.trashPileUp.pop(-1)
            if verbose:
                print("Adding card from deck to block: {0}".format(str(card_added)))
            return True

        #3: move kings to open piles
        for pile in self.playPiles:
            if len(pile.cards)==0: #pile has no cards
                for pile2 in self.playPiles:
                    if len(pile2.cards)>1 and pile2.cards[0].value == "K":
                        card_added = pile2.cards.pop(0)
                        if len(pile2.cards) > 0 and not pile2.cards[0].flipped:
                            pile2.cards[0].flip()
                        pile.addCard(card_added)
                        if verbose:
                            print("Moving {0} from Pile to Empty Pile".format(str(card_added)))
                        return True

                if len(self.trashPileUp) > 0 and self.trashPileUp[-1].value == "K":
                    card_added = self.trashPileUp[-1]
                    pile.addCard(card_added)
                    self.trashPileUp.pop(-1)
                    if verbose:
                        print("Moving {0} from Deck to Empty Pile".format(str(card_added)))
                    return True

        #4: add drawn card to playPiles
        for pile in self.playPiles:
            if len(pile.cards)>0 and len(self.trashPileUp) > 0:
                if self.checkCardOrder(pile.cards[0],self.trashPileUp[-1]):
                    card_added = self.trashPileUp[-1]
                    pile.addCard(card_added)
                    self.trashPileUp.pop(-1)
                    if verbose:
                        print("Moving {0} from Deck to Pile".format(str(card_added)))
                    return True

        #5: move around cards in playPiles
        for pile1 in self.playPiles:
            pile1_flipped_cards = pile1.getFlippedCards()
            if len(pile1_flipped_cards)>0:
                for pile2 in self.playPiles:
                    pile2_flipped_cards = pile2.getFlippedCards()
                    if pile2 is not pile1 and len(pile2_flipped_cards)>0:
                        for transfer_cards_size in range(1,len(pile1_flipped_cards)+1):
                            cards_to_transfer = pile1_flipped_cards[:transfer_cards_size]
                            if self.checkCardOrder(pile2.cards[0],cards_to_transfer[-1]):
                                pile1_downcard_count = len(pile1.cards) - len(pile1_flipped_cards)
                                pile2_downcard_count = len(pile2.cards) - len(pile2_flipped_cards)
                                if pile2_downcard_count < pile1_downcard_count:
                                    [pile2.cards.insert(0,card) for card in reversed(cards_to_transfer)]
                                    pile1.cards = pile1.cards[transfer_cards_size:]
                                    if len(pile1.cards) > 0 and not pile1.cards[0].flipped:
                                        pile1.cards[0].flip()
                                    if verbose:
                                        print("Moved {0} cards between piles: {1}".format(
                                            transfer_cards_size,
                                            ", ".join([str(card) for card in cards_to_transfer])
                                                                                         ))
                                    return True
                                elif pile1_downcard_count==0 and len(cards_to_transfer) == len(pile1.cards):
                                    [pile2.cards.insert(0,card) for card in reversed(cards_to_transfer)]
                                    pile1.cards = []
                                    if len(pile1.cards) > 0 and not pile1.cards[0].flipped:
                                        pile1.cards[0].flip()

                                    if verbose:
                                        print("Moved {0} cards between piles: {1}".format(
                                            transfer_cards_size,
                                            ", ".join([str(card) for card in cards_to_transfer])
                                                                                         ))
                                    return True
        return False

    def simulate(self,  recycles, verbose=False):

        actions = self.getPossibleMoves()
        turnResult = self.takeTurn(verbose=verbose)
        if recycles == 10:
            print("You recycled too much")
            return

        if turnResult:
            self.simulate(recycles,verbose=verbose)

        else:
            # End: draw from deck
            if len(self.trashPileDown) > 0:

                currentCard = self.trashPileDown.pop(0)
                currentCard.flip()
                self.trashPileUp.append(currentCard)
                print("Drawing new card: {0}".format(str(currentCard)))
                return self.simulate(recycles,verbose=verbose)
            else:
                if len(self.trashPileUp) > 1:
                    # recycle trash
                    self.trashPileDown = self.trashPileUp
                    self.trashPileUp = []
                    for i in self.trashPileDown:
                        i.flip()
                    #self.trashPileDown.extend([self.trashPileUp.pop(0).flip() for i in range(0, len(self.trashPileUp))])
                    print("Recycling deck")
                    recycles += 1
                    return self.simulate(recycles,verbose=verbose)
                elif verbose:
                    print("No more moves left!")
                return

#Olivia's Additions ###############################################

    # Get all possible moves somehow
    def getPossibleMoves(self):
        actions = []

        # start with finding all possible moves from pile to pile
        for pile1 in self.playPiles:
            pile1_flipped_cards = pile1.getFlippedCards()

            #if a pile is empty and another pile has a king
            if len(pile1.cards) == 0:  # pile has no cards
                for pile2 in self.playPiles:
                    if len(pile2.cards) > 1 and pile2.cards[0].value == "K":
                        actions.append(Action(pile2.getFlippedCards(),pile2,pile1))


            if len(pile1_flipped_cards) > 0:
                for pile2 in self.playPiles:
                    pile2_flipped_cards = pile2.getFlippedCards()
                    if pile2 is not pile1 and len(pile2_flipped_cards) > 0:
                        for transfer_cards_size in range(1, len(pile1_flipped_cards) + 1):
                            cards_to_transfer = pile1_flipped_cards[:transfer_cards_size]
                            if self.checkCardOrder(pile2.cards[0], cards_to_transfer[-1]):
                                pile1_downcard_count = len(pile1.cards) - len(pile1_flipped_cards)
                                pile2_downcard_count = len(pile2.cards) - len(pile2_flipped_cards)
                                if pile2_downcard_count < pile1_downcard_count:
                                    actions.append(Action(reversed(cards_to_transfer), pile1, pile2))
                                elif pile1_downcard_count == 0 and len(cards_to_transfer) == len(pile1.cards):
                                    actions.append(Action(reversed(cards_to_transfer), pile1, pile2))

        # then find all moves from pile to block
        for pile in self.playPiles:
            if len(pile.cards) > 0:
                add = self.canAddToBlock(pile.cards[0])
                if add:
                    actions.append(Action([pile.cards[0]], pile, add))

        # then, look for moves from block to piles (negative reward, but technically allowed)
        for suit in self.suits:
            if len(self.blockPiles[suit].cards) > 0:
                add = self.canMoveBlockToPile(self.blockPiles[suit].cards[0])
                if add:
                    actions.extend([Action(self.blockPiles[suit].cards[0], self.blockPiles[suit], i.cards) for i in add])

        #for block in self.blockPiles:
        #    add = self.canMoveBlockToPile(block.cards[0])
        #    if len(block.cards) > 0 and add:
        #        actions.extend([Action([block.cards[0]], block, add[i]) for i in add])

        # then look for opportunity to draw card
        if len(self.trashPileDown) > 0:
            actions.append(Action(self.trashPileDown[0], self.trashPileDown, self.trashPileUp))
        # then, look for opportunity to recycle trash
        if len(self.trashPileDown) < 1:
            # recycle trash
            # for now, we represent this action as (None, self.trashPileUp, self.trashPileDown)
            actions.append(Action(None, self.trashPileUp, self.trashPileDown))

        # then, look for move from trash to block or pile

        # trash to pile
        for pile in self.playPiles:

            if len(self.trashPileUp) > 0:
                if len(pile.cards)==0 and self.trashPileUp[-1].value=='K':
                    actions.append(Action(self.trashPileUp[-1],self.trashPileUp,pile))

                if len(pile.cards) > 0:
                    add = self.checkCardOrder(pile.cards[0], self.trashPileUp[-1])
                    if add:
                        actions.append(Action(self.trashPileUp[-1], self.trashPileUp, pile))

        # trash to block
        if len(self.trashPileUp) > 0:
            add = self.canAddToBlock(self.trashPileUp[-1])
            if add:
                actions.append(Action(self.trashPileUp[-1], self.trashPileUp, add))

        return actions

    #Check if player is out of moves
    def checkIfOutOfMoves(self):
        pass

    #Check if card on pile needs to be turned- reward 5
    def checkIfPileDrawn(self):
        return True

    #Move a card between two piles - no reward
    def moveBetweenPiles(self):

        if checkIfPileDrawn():
            return 5
        else:
            return 0

    #Move a card from the deck to the pile - reward 5
    def moveDeckToPile(self):
        return 5

    #Move a card from the deck to block - reward 10
    def movePileToBlock(self):

        if checkIfPileDrawn():
            return 15
        else:
            return 10

    #Move a card from block back to pile - reward -15
    def moveBlockToPile(self):
        return -15

    #Recycle deck - return -100
    def recycleDeck(self):
        return -100

    #Draw a card from the deck - no reward
    def drawDeck(self):
        return 0

    def make_move(state,action):
        if action == "moveBetweenPiles":
            reward = moveBetweenPiles()

        elif action == "moveDeckToPile":
            reward = moveDeckToPile()

        elif action == "movePileToBlock":
            reward = movePileToBlock()

        elif action == "moveBlockToPile":
            reward = moveBlockToPile()

        elif action == "recycleDeck":
            reward = recycleDeck()

        elif action == "drawDeck":
            reward = drawDeck()

        return reward

from card_elements import Card, Deck, Pile

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
        self.deck = Deck(self.values,self.suits)
        self.playPiles = []
        for i in range(self.numPlayPiles):
            thisPile = Pile()
            [thisPile.addCard(self.deck.takeFirstCard(flip=False)) for j in range(i+1)]
            thisPile.flipFirstCard()  
            self.playPiles.append(thisPile)
        self.blockPiles = {suit: Pile() for suit in self.suits}
        self.deck.cards[0].flip()
    
    def getGameElements(self):
        returnObject = {
            "deck": str(self.deck),
            "playPiles": [str(pile) for pile in self.playPiles],
            "blockPiles": {suit: str(pile) for suit, pile in self.blockPiles.items()}
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
        
    def takeTurn(self, verbose=False):
                
        #Pre: flip up unflipped pile end cards -> do this automatically
        [pile.cards[0].flip() for pile in self.playPiles if len(pile.cards)>0 and not pile.cards[0].flipped]
         
        #1: check if there are any play pile cards you can play to block piles
        for pile in self.playPiles:
            if len(pile.cards) > 0 and self.addToBlock(pile.cards[0]):
                card_added = pile.cards.pop(0)
                if verbose:
                    print("Adding play pile card to block: {0}".format(str(card_added)))
                return True
            
        #2: check if cards in deck can be added
        if self.addToBlock(self.deck.getFirstCard()):
            card_added = self.deck.takeFirstCard()
            if verbose:
                print("Adding card from deck to block: {0}".format(str(card_added)))
            return True
            
        #3: move kings to open piles
        for pile in self.playPiles:
            if len(pile.cards)==0: #pile has no cards
                for pile2 in self.playPiles:
                    if len(pile2.cards)>1 and pile2.cards[0].value == "K":
                        card_added = pile2.cards.pop(0)
                        pile.addCard(card_added)
                        if verbose:
                            print("Moving {0} from Pile to Empty Pile".format(str(card_added)))
                        return True
                    
                if self.deck.getFirstCard() is not None and self.deck.getFirstCard().value == "K":
                    card_added = self.deck.takeFirstCard()
                    pile.addCard(card_added)
                    if verbose:
                        print("Moving {0} from Deck to Empty Pile".format(str(card_added)))
                    return True
            
        #4: add drawn card to playPiles 
        for pile in self.playPiles:
            if len(pile.cards)>0 and self.deck.getFirstCard() is not None:
                if self.checkCardOrder(pile.cards[0],self.deck.getFirstCard()):
                    card_added = self.deck.takeFirstCard()
                    pile.addCard(card_added) 
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
                                    if verbose:
                                        print("Moved {0} cards between piles: {1}".format(
                                            transfer_cards_size,
                                            ", ".join([str(card) for card in cards_to_transfer])
                                                                                         ))
                                    return True
                                elif pile1_downcard_count==0 and len(cards_to_transfer) == len(pile1.cards):
                                    [pile2.cards.insert(0,card) for card in reversed(cards_to_transfer)]
                                    pile1.cards = []
                                    if verbose:
                                        print("Moved {0} cards between piles: {1}".format(
                                            transfer_cards_size,
                                            ", ".join([str(card) for card in cards_to_transfer])
                                                                                         ))
                                    return True
        return False
        
                    
    def simulate(self, draw = False, verbose=False):
        
        # clear cache if last turn was not card draw
        if not draw:
            self.deck.cache = []
        
        turnResult = self.takeTurn(verbose=verbose)
        
        if turnResult:
            self.simulate(verbose=verbose)
                    
        else:
            #End: draw from deck
            if len(self.deck.cards)>0:

                currentCard = self.deck.cards[0]

                if currentCard in self.deck.cache:
                    if verbose:
                        print("No more moves left!")
                    return 

                else:
                    self.deck.drawCard()
                    #if verbose:
                        #print("Drawing new card: {0}".format(str(currentCard)))
                    self.deck.cache.append(currentCard)
                    return self.simulate(draw=True, verbose=verbose)
            else:
                if verbose:
                    print("No more moves left!")
                return

#Olivia's Additions ###############################################

    #Get all possible moves somehow
    def getPossibleMoves(self):
        # start with finding all possible moves for each card on piles

        # then, look for moves from block to piles

        # then, look for move from trash to block or pile

    #Create new game and return initial state vector (high level or low level)
    def newGame(high_level):
        game = Game()

        if high_level:

        else:

    #Check if player is out of moves
    def checkIfOutOfMoves(self):

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

        if action == "moveDeckToPile":
            reward = moveDeckToPile()

        if action == "movePileToBlock":
            reward = movePileToBlock()

        if action == "moveBlockToPile":
            reward = moveBlockToPile()

        if action == "recycleDeck":
            reward = recycleDeck()

        if action == "drawDeck":
            reward = drawDeck()

        next_state = getNextState(state)
        return reward,next_state

    #called after making a move- recalculate state based on move made
    def getNewState(state):
        pass

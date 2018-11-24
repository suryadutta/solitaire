# Python Solitaire Simulator
### Surya Dutta

This code uses object oriented programming in Python to simulate Solitaire games. 

## Quickstart

To run one simulated game of Solitaire, use 

```
python main.py
```

 on the console. This will output a list of all the actions, the position of the cards at the end of play, and whether or not this was a successful game (happens about **4%** of the time)


 ## Definitions

* **Deck**:  Stack of cards that can be drawn from. This code only supports one card drawn at a time
* **Play Piles**:  The seven piles that cards are added to and shuffled around. Each pile can contain flipped up cards that have to follow sequential order and alternate colors
* **Block Piles**: Also called foundations - the four piles (one for each suit) that build up from Ace to King. When all block piles are completed, the player wins the game


## Code Overview

The code has three files:

* `card_elements.py` contains 3 classes: **Card**, **Pile**, and **Deck**. Each of these three classes have methods and variables that persist throughout the game.

* `solitaire.py` contains 1 class: **Game**. This contains methods for initializing a game of solitaire, checking/outputing status, and simulating a complete game using an ad-hoc algorithm discussed below. 

* `main.py` contains a simple script to simulate one game, and output the elements and result. 


## Algorithm

The possible actions for each turn is as follows: 

1. Make sure first card in each play pile is flipped up

2. Move any eligible cards to the block piles

3. If possible, move any kings to any empty play pile

4. If possible, add drawn card to a play pile

5. Permute flipped up cards in the play piles to see if any of them can be switched around. Only move cards between play piles if the number of cards faced down in the old pile is more than the number of cards faced down in the new pile

6. Draw new card

The algorithm will pick the first item on the list that is successful, and restart from the top on the next turn. If there are no possible moves left, the game will end, and can be checked if it is finished or not. 

This is definitely not the best algorithm for this game, and better ones [like this one](http://www.chessandpoker.com/solitaire_strategy.html) can be found readily. This was just the simplest one I could think of that made sense and could sometimes win. 

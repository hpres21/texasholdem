from dataclasses import dataclass
import itertools
import random

@dataclass
class Card:
    """
    Class for a card in poker. Each card has a value (2-10, J, Q, K, A) and a suit (s, c, h, d). 
    Values are stored as integers, where J = 11... A = 14. 
    """
    value: int 
    suit: str
    face_cards = {11: "J", 12: "Q", 13: "K", 14: "A"}
    

    def __repr__(self):
        if self.value <= 10:
            return f"{self.value}{self.suit}"   
        else: 
            return f"{self.face_cards[self.value]}{self.suit}"


@dataclass
class Deck:
    """
    Class for a deck containing 52 cards
    """

    values: tuple = (2+i for i in range(13))
    suits: tuple = ('h', 'c', 's', 'd')
    cards : tuple = tuple(itertools.product(values, suits))
    deck = [Card (v,s) for v,s in cards]

    def shuffle(self) -> list:
        random.shuffle(self.deck)

    def draw(self):
        return self.deck.pop()
    
    def reset(self, shuffle: bool = False):
        self.deck = [Card (v,s) for v,s in self.cards]
        if shuffle:
            self.shuffle()


if __name__ == "main":
    """
    Write tests here
    """
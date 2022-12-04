from dataclasses import dataclass
import itertools
import functools
import random

@dataclass(repr=False, eq=False, frozen=True)
@functools.total_ordering
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

    def _is_valid_operand(self, other):
        return hasattr(other, "value")


    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.value == other.value

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.value < other.valueone

    def __gt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.value > other.value

    def same_suit(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.suit == other.suit




@dataclass()
class Deck:
    """
    Class for a deck containing 52 cards
    """

    def __init__(self, ordered = False):
        values = (2+i for i in range(13))
        suits = ('h', 'c', 's', 'd')
        cards = tuple(itertools.product(values, suits))
        deck = [Card (v,s) for v,s in cards]
        if not ordered:
            random.shuffle(deck)
        self.deck = deck

    def draw(self):
        return self.deck.pop()


if __name__ == "main":
    """
    Write tests here
    """

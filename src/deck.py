from dataclasses import dataclass
import itertools
import functools
import random


@dataclass(repr=False, eq=False, frozen=True)
@functools.total_ordering
class Card:
    """
    Class for a card in poker. Each card has a value (2-10, J, Q, K, A) and
     a suit (s, c, h, d). All values are stored as integers, where face cards
     are stored as: J = 11... A = 14.
    """

    value: int
    suit: str
    face_cards = {11: "J", 12: "Q", 13: "K", 14: "A"}

    def __repr__(self):
        if self.value <= 10:
            return f"{self.value}{self.suit}"
        else:
            return f"{self.face_cards[self.value]}{self.suit}"

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.value == other.value and self.suit == other.suit

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.value < other.value

    def __gt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.value > other.value

    def __hash__(self) -> int:
        return hash(str(self))

    def same_suit(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.suit == other.suit

    @staticmethod
    def _is_valid_operand(other):
        return hasattr(other, "value")


@dataclass()
class Deck:
    """
    Class for a deck containing 52 cards
    """

    def __init__(self):
        self.deck = Deck.deck()
        random.shuffle(self.deck)

    def shuffle(self):
        random.shuffle(self.deck)

    def draw(self):
        return self.deck.pop()

    @staticmethod
    def deck():
        values = (2 + i for i in range(13))
        suits = ("h", "c", "s", "d")
        cards = tuple(itertools.product(values, suits))
        deck = [Card(v, s) for v, s in cards]
        return deck

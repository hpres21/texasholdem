import pytest
from deck import Card, Deck

def test_empty_deck():
    d = Deck()
    for _ in range(52):
        d.draw()
    assert len(d.deck) == 0

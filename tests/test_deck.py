from src.poker_game import Deck


def test_empty_deck():
    """
    a shuffled deck drawn 52 times should have no remaining cards
    """
    deck = Deck()
    for _ in range(52):
        deck.draw()
    assert len(deck.deck) == 0

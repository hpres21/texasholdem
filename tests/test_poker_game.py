import pytest
import random
from src.deck import Card, Deck
from src.poker_game import Player, PokerTable

n_tests = 10

def test_player_hand():
    """
    when a player draws a hand from a deck 26 times, every hand should be two
    cards and the remaining deck should be empty
    """
    deck = Deck()
    p1 = Player(100)
    for _ in range(26):
        p1.draw_hand(deck)
        assert all(isinstance(c, Card) for c in p1.hand)
        assert len(p1.hand) == 2
        p1.clear_hand()
    assert len(deck.deck) == 0


@pytest.mark.parametrize("unused_parameter", range(n_tests))
def test_adding_and_removing_players(unused_parameter):
    """
    adding x players to a table and then later removing y players should result
    in a table with x - y players
    """
    players_added = random.randint(2,6)
    players_removed = random.randint(0, players_added - 2)
    table = PokerTable()
    table.reset()
    for i in range(players_added):
        table.add_player(Player(i))
    for i in range(players_removed):
        table.remove_player(Player(i))
    assert len(table.players) == players_added - players_removed


@pytest.mark.parametrize("unused_parameter", range(n_tests))
def test_drawing_table_cards(unused_parameter):
    """
    flopping and drawing twice should result in a list of 5 cards
    """
    table = PokerTable()
    table.reset()
    table.flop()
    table.draw_card()
    table.draw_card()
    assert all(isinstance(c, Card) for c in table.board)
    assert len(table.board) == 5

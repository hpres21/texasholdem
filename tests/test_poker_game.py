# flake8: noqa
import pytest
import random
from deck import Card, Deck
from player import Player
from poker_game import PokerTable

n_tests = 10


@pytest.mark.parametrize("unused_parameter", list(range(n_tests)))
def test_adding_and_removing_players(unused_parameter):
    """
    adding x players to a table and then later removing y players should result
    in a table with x - y players
    """
    players_added = random.randint(2, 6)
    players_removed = random.randint(0, players_added - 2)
    table = PokerTable()
    table.reset()
    table.clear_players()
    for i in range(players_added):
        table.add_player(Player(name="p" + str(i)))
    for i in range(players_removed):
        table.sit_out_player(Player(name="p" + str(i)))
        table.remove_player(Player(name="p" + str(i)))
    assert len(table.players) == players_added - players_removed


@pytest.mark.parametrize("unused_parameter", list(range(n_tests)))
def test_drawing_table_cards(unused_parameter):
    """
    flopping and drawing twice should result in a list of 5 cards
    """
    table = PokerTable()
    table.reset()
    table.flop()
    table.draw_card()
    table.draw_card()
    assert len(table.board) == 5


def test_table_payout():
    """
    Test table paying out winnings to player
    """
    money = random.randint(1, 1000)
    test_table = PokerTable()
    test_player = Player(stack=0)
    test_table.pot_size = money
    test_table.payout(test_player)
    assert test_table.pot_size == 0
    assert test_player.stack == money

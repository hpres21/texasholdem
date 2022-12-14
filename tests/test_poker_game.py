# flake8: noqa
import pytest
import random
from unittest.mock import patch
from deck import Card, Deck
from poker_game import Player, PokerTable

n_tests = 10


def test_player_hand():
    """
    when a player draws a hand from a deck 26 times, every hand should be two
    cards and the remaining deck should be empty
    """
    deck = Deck()
    p1 = Player(stack=100)
    for _ in range(26):
        p1.draw_hand(deck)
        assert all(isinstance(c, Card) for c in p1.hand)
        assert len(p1.hand) == 2
        p1.clear_hand()
    assert len(deck.deck) == 0


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


@patch("builtins.input", lambda _: "CHECK")
def test_player_check():
    """
    Tests whether the the player's decision to check is valid.
    """
    test_player = Player("test", stack=1000)
    test_player.decision(0, 0)
    assert test_player.current_decision == 0


@patch("builtins.input", lambda _: 50)
def test_player_bet():
    """
    Tests whether the player's decision to bet is valid.
    """
    test_player = Player("test", stack=1000)
    test_player.decision(0, 0)
    assert test_player.current_decision == 50


@patch("builtins.input", lambda _: "CALL")
def test_player_call():
    """
    Tests whether the player's decision to call is valid.
    """
    test_player = Player("test", stack=1000)
    test_player.decision(15, 15)
    assert test_player.current_decision == 15


@patch("builtins.input", lambda _: "FOLD")
def test_player_fold():
    """
    Tests whether the player can fold
    """
    test_player = Player("test", stack=1000)
    test_player.decision(15, 15)
    assert test_player.current_decision == "FOLD"


@patch("builtins.input", lambda _: "ALL IN")
def test_player_all_in():
    """
    Tests whether the player can fold
    """
    test_player = Player("test", stack=1000)
    test_player.decision(15, 15)
    assert test_player.current_decision == test_player.stack


def test_player_reset_action():
    """
    Method to test a reset action of a
    """
    deck = Deck()
    test_player = Player(stack=1000)
    test_player.current_decision = random.randint(1, 1000)
    test_player.status = "highest bettor"
    test_player.bet_this_round = random.randint(1, 1000)
    test_player.reset_action()
    assert test_player.status == None
    assert test_player.current_decision == None
    assert test_player.bet_this_round == 0


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

import pytest
import random
from unittest.mock import patch
from deck import Card, Deck
from player import Player, NpcRandom, NpcStrategy1, NpcStrategy2

n_tests = 10


@patch("builtins.input", lambda _: "CHECK")
def test_player_check():
    """
    Tests whether the the player's decision to check is valid.
    """
    test_player = Player("test", stack=1000)
    test_player.decision([], 0, 0)
    assert test_player.current_decision == 0


@patch("builtins.input", lambda _: 50)
def test_player_bet():
    """
    Tests whether the player's decision to bet is valid.
    """
    test_player = Player("test", stack=1000)
    test_player.decision([], 0, 0)
    assert test_player.current_decision == 50


@patch("builtins.input", lambda _: "CALL")
def test_player_call():
    """
    Tests whether the player's decision to call is valid.
    """
    test_player = Player("test", stack=1000)
    test_player.decision([], 15, 15)
    assert test_player.current_decision == 15


@patch("builtins.input", lambda _: "FOLD")
def test_player_fold():
    """
    Tests whether the player can fold
    """
    test_player = Player("test", stack=1000)
    test_player.decision([], 15, 15)
    assert test_player.current_decision == "FOLD"


@patch("builtins.input", lambda _: "ALL IN")
def test_player_all_in():
    """
    Tests whether the player can fold
    """
    test_player = Player("test", stack=1000)
    test_player.decision([], 15, 15)
    assert test_player.current_decision == test_player.stack


def test_player_reset_action():
    """
    Method to test a reset action of a
    """
    test_player = Player(stack=1000)
    test_player.current_decision = random.randint(1, 1000)
    test_player.status = "highest bettor"
    test_player.bet_this_round = random.randint(1, 1000)
    test_player.reset_action()
    assert test_player.status is None
    assert test_player.current_decision is None
    assert test_player.bet_this_round == 0


def test_player_hand():
    """
    when a player draws a hand from a deck 26 times,
     every hand should be two cards and the remaining
     deck should be empty
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
def test_npc_random(unused_parameter):
    """
    The random npc will choose FOLD, CALL, CHECK or BET a
    valid value no matter what are the hand and board.
    """
    # Initialize a random npc
    stack = random.randint(0, 100)
    p1 = NpcRandom(name="p1", stack=stack)
    # set up the status before decision
    p1.bet_this_round = random.randint(0, stack)
    # call the decision method
    current_bet = random.randint(0, 100)
    p1.decision(current_bet=current_bet, pot=0, table_cards=[])
    if isinstance(p1.current_decision, int):
        assert p1.current_decision in list(
            range(
                2 * current_bet - p1.bet_this_round,
                p1.stack + 1
            )
        ) + [0, current_bet - p1.bet_this_round]
    else:
        assert p1.current_decision == "FOLD"


@pytest.mark.parametrize("unused_parameter", list(range(n_tests)))
def test_npc_strategy1_analysis(unused_parameter):
    """
    The analysis method will return a probability between 0
    and 1 and its standard deviation.
    """
    # Initialize a random npc
    deck = Deck()
    p1 = NpcStrategy1(name="p1", stack=0)
    # set up the status before decision
    p1.draw_hand(deck)
    # call the analysis method
    p, p_std = p1.analysis(table_cards=[deck.draw() for _ in range(5)])
    assert 0 <= p <= 1
    assert p_std < min(p, 1 - p)


@pytest.mark.parametrize("unused_parameter", list(range(n_tests)))
def test_npc_strategy1_decision(unused_parameter):
    """
    The npc with strategy 1 will only choose FOLD, CHECK or CALL
     (ALL IN if stack not enough to call).
    """
    # Initialize a random npc
    deck = Deck()
    stack = random.randint(0, 100)
    p1 = NpcStrategy1(name="p1", stack=stack)
    # set up the status before decision
    p1.draw_hand(deck)
    p1.bet_this_round = random.randint(0, stack)
    # call the decision method
    current_bet = random.randint(0, 100)
    pot = random.randint(0, 200)
    p1.decision(
        current_bet=current_bet,
        pot=pot,
        table_cards=[deck.draw() for _ in range(5)],
    )
    if isinstance(p1.current_decision, int):
        assert p1.current_decision in list(
            range(
                2 * current_bet - p1.bet_this_round,
                p1.stack + 1
            )
        ) + [0, current_bet - p1.bet_this_round]
    else:
        assert p1.current_decision == "FOLD"


@pytest.mark.parametrize("unused_parameter", list(range(n_tests)))
def test_npc_strategy2_analysis(unused_parameter):
    """
    The analysis method will return a probability between
    0 and 1 and its standard deviation.
    """
    # Initialize a random npc
    deck = Deck()
    p1 = NpcStrategy2(name="p1", stack=0)
    # set up the status before decision
    p1.draw_hand(deck)
    # call the analysis method
    p, p_std = p1.analysis(table_cards=[deck.draw() for _ in range(5)])
    assert 0 <= p <= 1
    assert p_std < min(p, 1 - p)


@pytest.mark.parametrize("unused_parameter", list(range(n_tests)))
def test_npc_strategy2_decision(unused_parameter):
    """
    The npc with strategy 2 will only choose FOLD, CHECK or
    CALL (ALL IN if stack not enough to call).
    """
    # Initialize a random npc
    deck = Deck()
    stack = random.randint(0, 100)
    p1 = NpcStrategy2(name="p1", stack=stack)
    # set up the status before decision
    p1.draw_hand(deck)
    p1.bet_this_round = random.randint(0, stack)
    # call the decision method
    current_bet = random.randint(0, 100)
    pot = random.randint(0, 200)
    p1.decision(
        current_bet=current_bet,
        pot=pot,
        table_cards=[deck.draw() for _ in range(5)],
    )
    if isinstance(p1.current_decision, int):
        assert p1.current_decision in list(
            range(
                2 * current_bet - p1.bet_this_round,
                p1.stack + 1
            )
        ) + [0, current_bet - p1.bet_this_round]
    else:
        assert p1.current_decision == "FOLD"

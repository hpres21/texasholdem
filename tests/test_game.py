import pytest
from deck import Card, Deck
from poker_game import Player


def test_player_hand():
    """
    when a player draws a hand from a deck 26 times, every hand should be two
    cards and the remaining deck should be empty
    """
    deck = Deck()
    deck.shuffle()
    p1 = Player(100)
    for _ in range(26):
        p1.draw_hand(deck)
        assert all(isinstance(c, Card) for c in p1.hand)
        assert len(p1.hand) == 2
    assert len(deck.deck) == 0



# import pytest
# from deck import Card, Deck
# from table import Player
#
# N_max = 10_000
# n_tests = 5


# # helper functions
# @pytest.fixture
# def random_int_list():
#     """generate a list of random players with values and size sampled from [0,N_max]"""
#     return list(np.random.randint(0, N_max, np.random.randint(0, N_max)))
#
#
# # tests
# @pytest.mark.parametrize("unused_parameter", range(n_tests))  # test n_tests times
# def test_merge_sort(unused_parameter,random_int_list):
#     # create a list of two random lists
#     l1 = sorted(random_int_list)
#     l2 = sorted(random_int_list)
#     assert merge(l1, l2) == sorted(l1 + l2)

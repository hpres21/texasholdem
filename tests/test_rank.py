import pytest
import random
from deck import Card
from rank import BestHand


@pytest.mark.parametrize("unused_parameter", range(n_tests))
def test_pair():
    hand = [Card(2, "c"), Card(2, "c")]
    board = [Card(3, "s"), Card(4, "s"), Card(10, "d"), Card(14, "h"), Card(7, "s")]

    bh = BestHand(hand, board)
    bh.find_best_hand()

    assert bh.rank == "pair"
    assert bh.best_hand == [
        Card(2, "c"),
        Card(2, "c"),
        Card(14, "h"),
        Card(10, "d"),
        Card(7, "s"),
    ]

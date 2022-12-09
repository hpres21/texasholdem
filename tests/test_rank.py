import itertools
from src.deck import Card, Deck
from src.rank import BestHand


def test_royal_flush():
    """
    should give 'royal flush' as a result of best hand
    """
    pocket = [Card(value=10, suit="s"), Card(value=12, suit="s")]
    board = [
        Card(value=13, suit="s"),
        Card(value=11, suit="s"),
        Card(value=9, suit="d"),
        Card(value=9, suit="s"),
        Card(value=14, suit="s"),
    ]

    bh = BestHand(pocket, board)
    assert bh.rank == "royal flush"
    assert bh.best_hand == [
        Card(value=14, suit="s"),
        Card(value=13, suit="s"),
        Card(value=12, suit="s"),
        Card(value=11, suit="s"),
        Card(value=10, suit="s"),
    ]


def test_straight_flush():
    """
    should give 'straight flush' as a result of best hand
    """
    pocket = [Card(value=10, suit="s"), Card(value=12, suit="s")]
    board = [
        Card(value=13, suit="s"),
        Card(value=11, suit="s"),
        Card(value=9, suit="d"),
        Card(value=9, suit="s"),
        Card(value=2, suit="s"),
    ]

    bh = BestHand(pocket, board)
    assert bh.rank == "straight flush"
    assert bh.best_hand == [
        Card(value=13, suit="s"),
        Card(value=12, suit="s"),
        Card(value=11, suit="s"),
        Card(value=10, suit="s"),
        Card(value=9, suit="s"),
    ]


def test_four_of_a_kind():
    """
    should give 'four of a kind' as a result of best hand
    """
    pocket = [Card(value=10, suit="s"), Card(value=10, suit="h")]
    board = [
        Card(value=10, suit="d"),
        Card(value=10, suit="c"),
        Card(value=9, suit="d"),
        Card(value=9, suit="s"),
        Card(value=2, suit="s"),
    ]

    bh = BestHand(pocket, board)
    assert bh.rank == "four of a kind"
    assert bh.best_hand in [
        x + y
        for x, y in itertools.product(
            itertools.permutations(
                [
                    Card(value=10, suit="s"),
                    Card(value=10, suit="h"),
                    Card(value=10, suit="d"),
                    Card(value=10, suit="c"),
                ]
            ),
            itertools.permutations([Card(value=9, suit="d"), Card(value=9, suit="s")]),
        )
    ]


def test_full_house_case1():
    """
    should give 'full house' as a result of best hand
    """
    pocket = [Card(value=10, suit="s"), Card(value=10, suit="h")]
    board = [
        Card(value=10, suit="d"),
        Card(value=9, suit="c"),
        Card(value=9, suit="d"),
        Card(value=9, suit="s"),
        Card(value=2, suit="s"),
    ]

    bh = BestHand(pocket, board)
    assert bh.rank == "full house"
    assert bh.best_hand in [
        x + y
        for x, y in itertools.product(
            itertools.permutations(
                [
                    Card(value=10, suit="s"),
                    Card(value=10, suit="h"),
                    Card(value=10, suit="d"),
                ]
            ),
            itertools.permutations(
                [
                    Card(value=9, suit="c"),
                    Card(value=9, suit="d"),
                    Card(value=9, suit="s"),
                ],
                2,
            ),
        )
    ]


def test_full_house_case2():
    """
    should give 'full house' as a result of best hand
    """
    pocket = [Card(value=10, suit="s"), Card(value=10, suit="h")]
    board = [
        Card(value=10, suit="d"),
        Card(value=8, suit="c"),
        Card(value=9, suit="d"),
        Card(value=9, suit="s"),
        Card(value=2, suit="s"),
    ]

    bh = BestHand(pocket, board)
    assert bh.rank == "full house"
    assert bh.best_hand in [
        x + y
        for x, y in itertools.product(
            itertools.permutations(
                [
                    Card(value=10, suit="s"),
                    Card(value=10, suit="h"),
                    Card(value=10, suit="d"),
                ]
            ),
            itertools.permutations([Card(value=9, suit="d"), Card(value=9, suit="s")]),
        )
    ]


def test_flush():
    """
    should give 'flush' as a result of best hand
    """
    pocket = [Card(value=10, suit="s"), Card(value=10, suit="h")]
    board = [
        Card(value=10, suit="d"),
        Card(value=3, suit="s"),
        Card(value=8, suit="s"),
        Card(value=9, suit="s"),
        Card(value=2, suit="s"),
    ]

    bh = BestHand(pocket, board)
    assert bh.rank == "flush"
    assert bh.best_hand == [
        Card(value=10, suit="s"),
        Card(value=9, suit="s"),
        Card(value=8, suit="s"),
        Card(value=3, suit="s"),
        Card(value=2, suit="s"),
    ]


def test_straight():
    """
    should give 'straight' as a result of best hand
    """
    pocket = [Card(value=10, suit="s"), Card(value=8, suit="h")]
    board = [
        Card(value=6, suit="d"),
        Card(value=9, suit="s"),
        Card(value=3, suit="s"),
        Card(value=3, suit="d"),
        Card(value=7, suit="h"),
    ]

    bh = BestHand(pocket, board)
    assert bh.rank == "straight"
    assert bh.best_hand == [
        Card(value=10, suit="s"),
        Card(value=9, suit="s"),
        Card(value=8, suit="h"),
        Card(value=7, suit="h"),
        Card(value=6, suit="d"),
    ]


def test_three_of_a_kind():
    """
    should give 'three_of_a_kind' as a result of best hand
    """
    pocket = [Card(value=8, suit="s"), Card(value=8, suit="h")]
    board = [
        Card(value=8, suit="d"),
        Card(value=9, suit="s"),
        Card(value=3, suit="s"),
        Card(value=3, suit="d"),
        Card(value=7, suit="h"),
    ]

    bh = BestHand(pocket, board)
    assert bh.rank == "three of a kind"
    assert bh.best_hand in [
        x + [Card(value=9, suit="s"), Card(value=7, suit="h")]
        for x in itertools.permutations(
            [Card(value=8, suit="s"), Card(value=8, suit="h"), Card(value=8, suit="d")]
        )
    ]


def test_two_pair():
    """
    should give 'two pair' as a result of best hand
    """
    pocket = [Card(value=8, suit="s"), Card(value=8, suit="h")]
    board = [
        Card(value=7, suit="d"),
        Card(value=9, suit="s"),
        Card(value=3, suit="s"),
        Card(value=3, suit="d"),
        Card(value=7, suit="h"),
    ]

    bh = BestHand(pocket, board)
    assert bh.rank == "two pair"
    assert bh.best_hand in [
        x + y + [Card(value=9, suit="s")]
        for x, y in itertools.product(
            itertools.permutations([Card(value=8, suit="s"), Card(value=8, suit="h")]),
            itertools.permutations([Card(value=7, suit="d"), Card(value=7, suit="h")]),
        )
    ]


def test_pair():
    """
    should give 'pair' as a result of best hand
    """
    pocket = [Card(value=9, suit="s"), Card(value=6, suit="h")]
    board = [
        Card(value=7, suit="d"),
        Card(value=9, suit="c"),
        Card(value=2, suit="s"),
        Card(value=3, suit="d"),
        Card(value=5, suit="h"),
    ]

    bh = BestHand(pocket, board)
    assert bh.rank == "pair"
    assert bh.best_hand in [
        x + [Card(value=7, suit="d"), Card(value=6, suit="h"), Card(value=5, suit="h")]
        for x in itertools.permutations(
            [Card(value=9, suit="s"), Card(value=9, suit="c")]
        )
    ]


def test_high_card():
    """
    should give 'high card' as a result of best hand
    """
    pocket = [Card(value=9, suit="s"), Card(value=6, suit="h")]
    board = [
        Card(value=7, suit="d"),
        Card(value=10, suit="c"),
        Card(value=2, suit="s"),
        Card(value=3, suit="d"),
        Card(value=5, suit="h"),
    ]

    bh = BestHand(pocket, board)
    assert bh.rank == "high card"
    assert bh.best_hand == [
        Card(value=10, suit="c"),
        Card(value=9, suit="s"),
        Card(value=7, suit="d"),
        Card(value=6, suit="h"),
        Card(value=5, suit="h"),
    ]

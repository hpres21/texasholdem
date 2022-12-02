import functools
import table
from deck import Card


@functools.total_ordering
class BestHand:
    ranks = {"high card": 0, "pair": 1, "two pair": 2, "three of a kind": 3,
             "straight": 4, "flush": 5, "full house": 6, "four of a kind": 7,
             "straight flush": 8, "royal flush": 9
             }

    def __init__(self, pocket: list[Card], board: list[Card]):
        self.pocket = pocket
        self.board = board
        self.rank = ""
        self.besthand = []
        self.best_hand()

    # def __init__(self, player: Player, table: Table):
    #     self.pocket = player.hand
    #     self.table = table.board

    def best_hand(self):
        if self._is_straight_flush():
            if self.besthand[0].value == 14:
                self.rank = "royal flush"
            else:
                self.rank = "straight flush"
        elif self._is_four_of_a_kind():
            self.rank = "four of a kind"
        elif self._is_full_house():
            self.rank = "full house"
        elif self._is_flush():
            self.rank = "flush"
        elif self._is_straight():
            self.rank = "straight"
        elif self._is_three_of_a_kind():
            self.rank = "three of a kind"
        elif self._is_two_pair():
            self.rank = "two pair"
        elif self._is_pair():
            self.rank = "pair"
        else:
            self.rank = "high card"
            self.besthand = [*self.pocket, *self.board[:3]]

    def _is_straight_flush(self):
        self.besthand = [*self.pocket, *self.board[:3]]
        self.pocket_in_best_hand = [0, 1]
        return False

    def _is_four_of_a_kind(self):
        self.besthand = [*self.pocket, *self.board[:3]]
        self.pocket_in_best_hand = [0, 1]
        return False

    def _is_full_house(self):
        self.besthand = [*self.pocket, *self.board[:3]]
        self.pocket_in_best_hand = [0, 1]
        return False

    def _is_flush(self):
        self.besthand = [*self.pocket, *self.board[:3]]
        self.pocket_in_best_hand = [0, 1]
        return False

    def _is_straight(self):
        self.besthand = [*self.pocket, *self.board[:3]]
        self.pocket_in_best_hand = [0, 1]
        return False

    def _is_three_of_a_kind(self):
        self.besthand = [*self.pocket, *self.board[:3]]
        self.pocket_in_best_hand = [0, 1]
        return False

    def _is_two_pair(self):
        self.besthand = [*self.pocket, *self.board[:3]]
        self.pocket_in_best_hand = [0, 1]
        return False

    def _is_pair(self):
        self.besthand = [*self.pocket, *self.board[:3]]
        self.pocket_in_best_hand = [0, 1]
        return False

    @staticmethod
    def _is_valid_operand(other):
        return (hasattr(other, "besthand") and
                hasattr(other, "rank"))

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return ((self.ranks[self.rank], tuple(self.besthand)) ==
                (self.ranks[other.rank], tuple(other.besthand)))

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return ((self.ranks[self.rank], tuple(self.besthand)) <
                (self.ranks[other.rank], tuple(other.besthand)))

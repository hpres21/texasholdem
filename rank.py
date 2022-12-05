import functools
import itertools
from typing import List

import poker_game
from deck import Card


@functools.total_ordering
class BestHand:
    """
    Class for the best hand for a player.
    """
    ranking = {"high card": 0, "pair": 1, "two pair": 2, "three of a kind": 3,
               "straight": 4, "flush": 5, "full house": 6, "four of a kind": 7,
               "straight flush": 8, "royal flush": 9
               }

    def __init__(self, pocket: list[Card], board: list[Card]):
        """
        Automatically find the best hand upon initialization. 
        The best hand of a player, is in the list 'BestHand(pocket, board).best_hand', or equivalently
        player_A = BestHand(pocket, board)
        player_A.best_hand
        
        Pocket cards are player_A.best_hand[player_A.pocket_pos].
        """
        self.pocket = pocket
        self.board = board
        self.rank: str
        self.best_hand: list[Card]
        self.pocket_pos: list[int]
        self.find_best_hand()

    # def __init__(self, player: Player, table: Table):
    #     self.pocket = player.hand
    #     self.table = table.board

    def _update_rank(self, possible_rank: str):
        assert possible_rank in self.ranking, f'{possible_rank} is not in ranking dictionary.'
        if self.ranking[self.rank] < self.ranking[possible_rank]:
            self.rank = possible_rank

    def find_best_hand(self) -> None:
        straight_or_flush = self._is_straight_or_flush()
        if straight_or_flush == 'royal flush' or straight_or_flush == 'straight flush':
            return None
        if self._is_four_of_a_kind():
            return None
        if self._is_full_house():
            return None
        if straight_or_flush:
            return None
        if self._is_three_of_a_kind_or_two_pair():
            return None
        if self._is_pair():
            return None
        else:
            self.rank = "high card"
            self.best_hand = sorted([*self.pocket, *self.board], reverse=True)[:5]
            return None

    @property
    def _is_straight_or_flush(self):
        temp_best_hand = [0]
        # for all possible combinations
        for hand in itertools.combinations(self.pocket + self.board, 5):
            # sort it descending
            sorted_hand = sorted(hand, reverse=True)
            is_flush = False
            is_straight = False
            # see if it is flush
            if len(set([card.suit for card in sorted_hand])) == 1:
                is_flush = True
                self._update_rank("flush")
            # see if it is straight
            sorted_value = [card.value for card in sorted_hand]
            # if it is the special case [A 5 4 3 2], change it to [5 4 3 2 A] to make it the smallest straight
            if sorted_value == [14, 5, 4, 3, 2]:
                sorted_value = [5, 4, 3, 2, 14]
                sorted_hand = [sorted_hand[1:], sorted_hand[0]]
                is_straight = True
                self._update_rank("straight")
            elif len(set(sorted_value)) == 5 and (sorted_value[4] - sorted_value[0]) == 4:
                is_straight = True
                self._update_rank("straight")
            # update the temporary best hand
            if is_straight:
                if is_flush:
                    if self.rank == "straight flush":
                        if sorted_hand[0] > temp_best_hand[0]:
                            temp_best_hand = sorted_hand
                    else:
                        self._update_rank("straight flush")
                        temp_best_hand = sorted_hand
                elif self.rank == "straight":
                    if sorted_hand[0] > temp_best_hand[0]:
                        temp_best_hand = sorted_hand
            elif is_flush and self.rank == "flush":
                if sorted_hand[0] > temp_best_hand[0]:
                    temp_best_hand = sorted_hand
        if self.rank:
            if self.rank == 'straight flush' and self.best_hand[0].value == 14:
                self.rank = "royal flush"
            self.best_hand = temp_best_hand
            return self.rank
        else:
            return False

    def _is_four_of_a_kind(self):
        temp_best_hand = [0, 0, 0, 0, 0]
        # for all possible combinations
        for hand in itertools.combinations(self.pocket + self.board, 5):
            is_four_of_a_kind = False
            # sort it descending
            sorted_hand = sorted(hand, reverse=True)
            # see if it is four of a kind
            if len(set([card.value for card in hand])) == 2:
                if sorted_hand[0].value != sorted_hand[1].value:
                    sorted_hand = [sorted_hand[1:], sorted_hand[0]]
                    is_four_of_a_kind = True
                elif sorted_hand[3].value != sorted_hand[4].value:
                    is_four_of_a_kind = True
            # update the temporary best hand
            if is_four_of_a_kind and (sorted_hand[0], sorted_hand[4]) > (temp_best_hand[0], temp_best_hand[4]):
                self._update_rank("four of a kind")
                temp_best_hand = sorted_hand
        if self.rank == 'four of a kind':
            self.best_hand = temp_best_hand
            return True
        else:
            return False

    def _is_full_house(self):
        temp_best_hand = [0, 0, 0, 0, 0]
        # for all possible combinations
        for hand in itertools.combinations(self.pocket + self.board, 5):
            is_full_house = False
            # sort it descending
            sorted_hand = sorted(hand, reverse=True)
            # see if it is full house:
            if len(set([card.value for card in hand])) == 2:
                if sorted_hand[1].value != sorted_hand[2].value:
                    sorted_hand = sorted_hand[2:] + sorted_hand[:2]
                    is_full_house = True
                elif sorted_hand[2].value != sorted_hand[3].value:
                    is_full_house = True
            # update the temporary best hand
            if is_full_house and (sorted_hand[0], sorted_hand[3]) > (temp_best_hand[0], temp_best_hand[3]):
                self._update_rank("full house")
                temp_best_hand = sorted_hand
        if self.rank == 'full house':
            self.best_hand = temp_best_hand
            return True
        else:
            return False

    def _is_three_of_a_kind_or_two_pair(self):
        temp_best_hand = [0]
        # for all possible combinations
        for hand in itertools.combinations(self.pocket + self.board, 5):
            is_three_of_a_kind = False
            is_two_pair = False
            # sort it descending
            sorted_hand = sorted(hand, reverse=True)
            # see if it is three of a kind:
            if len(set([card.value for card in hand])) == 3:
                if len(set([card.value for card in sorted_hand[:3]])) == 1:
                    is_three_of_a_kind = True
                elif len(set([card.value for card in sorted_hand[1:4]])) == 1:
                    sorted_hand = sorted_hand[1:3] + sorted_hand[:1] + sorted_hand[-1:]
                    is_three_of_a_kind = True
                elif len(set([card.value for card in sorted_hand[2:]])) == 1:
                    sorted_hand = sorted_hand[2:] + sorted_hand[:2]
                    is_three_of_a_kind = True
                elif len(set([card.value for card in sorted_hand[:4]])) == 2:
                    is_two_pair = True
                elif len(set([card.value for card in sorted_hand[1:]])) == 2:
                    sorted_hand = sorted_hand[1:] + sorted_hand[:1]
                    is_two_pair = True
                else:
                    sorted_hand = sorted_hand[:3] + sorted_hand[3:4] + sorted_hand[-2:]
                    is_two_pair = True
            # update the temporary best hand
            if is_three_of_a_kind:
                if self.rank == 'three of a kind' and (sorted_hand[0].value, sorted_hand[3].value) > (temp_best_hand[0], temp_best_hand[3]):
                    temp_best_hand = sorted_hand
                else:
                    self._update_rank("three of a kind")
                    temp_best_hand = sorted_hand
            if is_two_pair:
                if self.rank == 'two pair' and (sorted_hand[0].value, sorted_hand[2].value) > (temp_best_hand[0], temp_best_hand[2]):
                    temp_best_hand = sorted_hand
                elif self.rank == '':
                    self._update_rank("two pair")
                    temp_best_hand = sorted_hand
        if self.rank == 'full house':
            self.best_hand = temp_best_hand
        if self.rank == 'two pair':
            self.best_hand = temp_best_hand
            return True
        else:
            return False
    def _is_pair(self):
        return True

    @staticmethod
    def _is_valid_operand(other):
        return (hasattr(other, "best_hand") and
                hasattr(other, "rank"))

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return ((self.ranking[self.rank], tuple(self.best_hand)) ==
                (self.ranking[other.rank], tuple(other.best_hand)))

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return ((self.ranking[self.rank], tuple(self.best_hand)) <
                (self.ranking[other.rank], tuple(other.best_hand)))

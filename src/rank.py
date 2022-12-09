import functools
import itertools
from src.deck import Card


@functools.total_ordering
class BestHand:
    """
    Class for the best hand for a player.
    """
    _ranking = {None: -1, "high card": 0, "pair": 1, "two pair": 2, "three of a kind": 3,
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
        self.__pocket = pocket
        self.__board = board
        self.rank = ''
        self.best_hand: list[Card]
        self.pocket_pos: list[int]

        self._find_best_hand()

    def _update_rank(self, new_rank: str) -> bool:
        assert new_rank in self._ranking, f'{new_rank} is not in ranking dictionary.'
        if not self.rank:
            self.rank = new_rank
            return True
        elif self._ranking[self.rank] < self._ranking[new_rank]:
            self.rank = new_rank
            return True
        else:
            return False

    def find_best_hand(self) -> None:
        """"
        This method runs the checks for each hand ranks and assigns the highest value to self.best_hand
        """
        self._check_pairings()
        if self.rank == "four of a kind" or self.rank == "full house":
            self.pocket_pos = [self.best_hand.index(card) for card in self.__pocket]
            return None
        else:
            self._check_straight_or_flush()
            self.pocket_pos = [self.best_hand.index(card) for card in self.__pocket]
            return None

    def _check_straight_or_flush(self):
        temp_bh = [Card(0, "u")]
        # for all possible combinations
        for hand in itertools.combinations(self.__pocket + self.__board, 5):
            # sort it descending
            sorted_hand = sorted(hand, reverse=True)
            is_flush = False
            is_straight = False

            # see if it is flush
            if len(set([card.suit for card in sorted_hand])) == 1:
                is_flush = True

            # see if it is straight
            sorted_value = [card.value for card in sorted_hand]

            # if it is the special case [A 5 4 3 2], change it to [5 4 3 2 A] to make it the smallest straight
            if sorted_value == [14, 5, 4, 3, 2]:
                sorted_hand = [sorted_hand[1:], sorted_hand[0]]
                is_straight = True
            elif len(set(sorted_value)) == 5 and (sorted_value[0] - sorted_value[4]) == 4:
                is_straight = True

            # update temp_bh
            if is_straight:
                if is_flush:
                    if self.rank == "straight flush":
                        if sorted_hand[0] > temp_bh[0]:
                            temp_bh = sorted_hand
                    else:
                        self._update_rank("straight flush")
                        temp_bh = sorted_hand
                else:
                    if self.rank == "straight" and sorted_hand[0] > temp_bh[0]:
                        temp_bh = sorted_hand
                    elif self._update_rank("straight"):
                        temp_bh = sorted_hand
            elif is_flush:
                if self.rank == "flush" and sorted_hand[0] > temp_bh[0]:
                    temp_bh = sorted_hand
                elif self._update_rank("flush"):
                    temp_bh = sorted_hand
        if self.rank in ['straight', 'flush', 'straight flush', 'royal flush']:
            if self.rank == 'straight flush' and temp_bh[0].value == 14:
                self.rank = "royal flush"
            self.best_hand = temp_bh
        return None

    def _check_pairings(self) -> None:
        """
        This method identifies four of a kinds, full houses, three of a kinds, 
        two pair, pairs, and high card hands. It then updates self.rank
        and constructs a list of the five best cards which is stored in 
        self.best_hand.
        """
        bh = []
        pairs = []
        trips = []
        quads = []

        sorted_hand = sorted(self.__pocket + self.__board, reverse=True)

        for num, group in itertools.groupby(sorted_hand, lambda card: card.value):
            count = sum(1 for _ in group)
            if count == 2:
                pairs.append((num, list(group)))
            elif count == 3:
                trips.append((num, list(group)))
            elif count == 4:
                quads.append((num, list(group)))

        pairs = sorted(pairs, key=lambda x: x[0], reverse=True)
        trips = sorted(trips, key=lambda x: x[0], reverse=True)
        if len(quads) > 0:
            self._update_rank("four of a kind")
            bh.extend(quads[0][1])
        elif len(trips) > 0 and len(trips + pairs) >= 2:
            self._update_rank("full house")
            bh.extend(trips[0][1])
            if len(trips) == 2:
                bh.extend(trips[1][1])
                bh = bh[:-1]
            else:
                bh.extend(pairs[0][1])
        elif len(trips) == 1:
            self._update_rank("three of a kind")
            bh.extend(trips[0][1])
        elif len(pairs) >= 2:
            self._update_rank("two pair")
            bh.extend(pairs[0][1] + pairs[1][1])
        elif len(pairs) == 1:
            self._update_rank("pair")
            bh.extend(pairs[0][1])
        else:
            self._update_rank("high card")

        i = 0
        while len(bh) < 5:
            if sorted_hand[i] not in bh:
                bh.append(sorted_hand[i])
            i += 1
        self.best_hand = bh
        return None

    @staticmethod
    def _is_valid_operand(other):
        return (hasattr(other, "best_hand") and
                hasattr(other, "rank"))

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return ((self._ranking[self.rank], tuple(self.best_hand)) ==
                (self._ranking[other.rank], tuple(other.best_hand)))

    def __ne__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return ((self._ranking[self.rank], tuple(self.best_hand)) !=
                (self._ranking[other.rank], tuple(other.best_hand)))

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return ((self._ranking[self.rank], tuple(self.best_hand)) <
                (self._ranking[other.rank], tuple(other.best_hand)))

    def __gt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return ((self._ranking[self.rank], tuple(self.best_hand)) >
                (self._ranking[other.rank], tuple(other.best_hand)))
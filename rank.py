import functools
import itertools
from deck import Card


def filter_by_value(value: int, l: list[Card]) -> list[Card]:
    """"
    Helper function to find cards in a list specified card value. 
    """
    return list(filter(lambda x: x.value == value, l))

@functools.total_ordering
class BestHand:
    """
    Class for the best hand for a player.
    """
    ranking = {None: -1, "high card": 0, "pair": 1, "two pair": 2, "three of a kind": 3,
               "straight": 4, "flush": 5, "full house": 6, "four of a kind": 7,
               "straight flush": 8, "royal flush": 9
               }
    rank: str

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
        self.rank = None
        self.best_hand: list[Card]
        self.pocket_pos: list[int]

    # def __init__(self, player: Player, table: Table):
    #     self.pocket = player.hand
    #     self.table = table.board

    def _update_rank(self, possible_rank: str):
        assert possible_rank in self.ranking, f'{possible_rank} is not in ranking dictionary.'
        if not self.rank:
            self.rank = possible_rank
        if self.ranking[self.rank] < self.ranking[possible_rank]:
            self.rank = possible_rank

        
    def find_best_hand(self) -> None:
        """"
        This method runs the checks for each hand ranks and assigns the highest value to the 
        """
        self.check_pairings()
        if self.rank == "four of a kind" or self.rank == "full house":
            return None
        else:
            self._is_straight_or_flush()


    def is_straight_or_flush(self):
        temp_best_hand = [Card(0, "u")]
        # for all possible cmobinations
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
                sorted_hand = [sorted_hand[1:], sorted_hand[0]]
                is_straight = True
                self._update_rank("straight")
            elif len(set(sorted_value)) == 5 and (sorted_value[0] - sorted_value[4]) == 4:
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
        if self.rank in ['straight', 'flush', 'straight flush', 'royal flush']:
            if self.rank == 'straight flush' and temp_best_hand[0].value == 14:
                self.rank = "royal flush"
            self.best_hand = temp_best_hand
            return self.rank
        else:
            return False

    def check_pairings(self) -> None:
        """"
        This method identifies four of a kinds, full houses, three of a kinds, 
        two pair, pairs, and high card hands. It then updates self.handrank
        and constructs a list of the five best cards which is stored in 
        self.best_hand.
        """
        bh = []
        pairs = []
        trips = []
        quads = []

        sorted_hand = sorted(self.pocket + self.board, reverse=True)
        hand_values = map(lambda x: x.value, sorted_hand)

        for num, group in itertools.groupby(hand_values):
            count = sum(1 for _ in group)
            if count == 2:
                pairs.append(num)
            elif count == 3:
                trips.append(num)
            elif count == 4:
                quads.append(num)

        if len(quads) > 0:
            self._update_rank("four of a kind")
            bh.extend(filter_by_value(quads[0], sorted_hand))
        elif len(trips) > 0 and len(trips + pairs) >= 2:
            self._update_rank("full house")
            bh.extend(filter_by_value(trips[0], sorted_hand))
            if len(trips) == 2:
                bh.extend(filter_by_value(trips[1], sorted_hand))
                bh = bh[:-1]
                # if there are 2 trips, we need to choose the higher trip in the full house
            else:
                bh.extend(filter_by_value(pairs[0], sorted_hand))
                # if there are 1 trip and 2 two pairs, we need to choose the higher two pair
        elif len(trips) == 1:
            self._update_rank("three of a kind")
            bh.extend(filter_by_value(trips[0], sorted_hand))
        elif len(pairs) >= 2:
            self._update_rank("two pair")
            for p in pairs:
                bh.extend(filter_by_value(p, sorted_hand))
            # if there are 3 pairs, bh will have 6 cards;
            # also we need higher pairs to come first in bh in order to properly compare different hands
        elif len(pairs) == 1:
            self._update_rank("pair")
            bh.extend(filter_by_value(pairs[0], sorted_hand))
        else:
            self._update_rank("high card")

        i = 0
        while len(bh) < 5:
            if sorted_hand[i] not in bh:
                bh.append(sorted_hand[i])
            i+=1
        self.best_hand = bh

    @staticmethod
    def _is_valid_operand(other):
        return (hasattr(other, "best_hand") and
                hasattr(other, "rank"))

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return ((self.ranking[self.rank], tuple(self.best_hand)) ==
                (self.ranking[other.rank], tuple(other.best_hand)))
    
    def __ne__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return ((self.ranking[self.rank], tuple(self.best_hand)) !=
                (self.ranking[other.rank], tuple(other.best_hand)))


    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return ((self.ranking[self.rank], tuple(self.best_hand)) <
                (self.ranking[other.rank], tuple(other.best_hand)))
    
    def __gt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return ((self.ranking[self.rank], tuple(self.best_hand)) >
                (self.ranking[other.rank], tuple(other.best_hand)))

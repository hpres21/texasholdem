import itertools
import random
import bisect
import rank
import numpy as np
from deck import Deck, Card
from poker_game import Player


class NpcRandom(Player):
    """
    This is a NPC player that will randomly make decisions no matter what its
    hand and board are.
    """

    name: str = None

    def __init__(self, name, stack):
        self.name = name
        self.stack = stack

    def decision(self, current_bet: int, pot: int, board: list[Card]) -> None:
        """
        Decision method prompts the npc to choose an action for their turn.
        The npc will decide randomly between all choices.
        """
        # Skip player who is all-in
        if self.stack == 0:
            self.current_decision = 0
            return

        if current_bet * 2 < self.stack:
            possible_action = {
                "FOLD",
                random.randint(current_bet * 2, self.stack + 1),
            }
        else:
            possible_action = {"FOLD"}

        if current_bet > self.bet_this_round:
            possible_action.add("CALL")
        elif current_bet == self.bet_this_round:
            possible_action.add("CHECK")

        action = random.sample(possible_action, 1)[0]
        try:
            action = int(action)
            self.bet(action - self.bet_this_round)
        except ValueError:
            if action.upper() == "CALL":
                if self.bet_this_round < current_bet <= self.stack:
                    self.bet(current_bet - self.bet_this_round)
                else:
                    self.bet(self.stack - self.bet_this_round)
            elif action.upper() == "CHECK":
                self.current_decision = 0
                self.status = None
            elif action.upper() == "FOLD":
                self.current_decision = "FOLD"


class NpcStrategy1(Player):
    """
    This is a NPC player that will make decisions from CHECK, FOLD, and CALL
    based on probability of winning.
    """

    name: str = None

    def __init__(self, name, stack):
        self.name = name
        self.stack = stack

    def decision(self, current_bet: int, pot: int, board: list[Card]) -> None:
        """
        Decision method prompts the npc to choose an action for their turn.
        The npc will decide based on the probability of winning.
        """
        # Skip player who is all-in
        if self.stack == 0:
            self.current_decision = 0
            return

        # CHECK when it's possible
        if current_bet == self.bet_this_round:
            self.current_decision = 0
            self.status = None
        else:
            p_win, p_std = self.analysis(board)
            # FOLD when analysis result is negative
            if p_win * pot < (1 - p_win) * (current_bet - self.bet_this_round):
                self.current_decision = "FOLD"
            # CALL when analysis result is positive
            else:
                if current_bet <= self.stack:
                    self.bet(current_bet - self.bet_this_round)
                else:
                    self.bet(self.stack - self.bet_this_round)

    def analysis(self, board: list[Card]) -> tuple[float, float]:
        deck = Deck()
        my_possible_hands = []
        other_possible_hands = []

        for hand in itertools.combinations(
            [card for card in deck.deck if card not in (self.hand + board)],
            5 - len(board),
        ):
            other_possible_hands = [
                rank.BestHand(self.hand, board + list(hand)).best_hand
            ]
        for hand in itertools.combinations(
            [card for card in deck.deck if card not in (self.hand + board)],
            5 - len(board),
        ):
            other_possible_hands = [
                rank.BestHand(list(hand[:2]), list(hand[2:])).best_hand
            ]
        other_possible_hands.sort()

        p_win: list[float] = []
        for bh in my_possible_hands:
            p_win.append(
                (
                    bisect.bisect_left(other_possible_hands, bh)
                    + bisect.bisect_right(other_possible_hands, bh)
                )
                / 2
                / len(other_possible_hands)
            )
        return p_win.mean, np.std(p_win)


class NpcStrategy2(Player):
    """
    This is a NPC player that will make decisions from CHECK, FOLD, CALL, and
    BET based on probability of winning based. The difference from
    NpcStrategy1 is that there is some randomness to hide the pattern of its
    strategy.
    """

    name: str = None

    def __init__(self, name, stack):
        self.name = name
        self.stack = stack

    def decision(self, current_bet: int, pot: int, board: list[Card]) -> None:
        """
        Decision method prompts the npc to choose an action for their turn.
        The npc will decide based on the probability of winning, and
        randomization is introduced to hide pattern.
        """
        # Skip player who is all-in
        if self.stack == 0:
            self.current_decision = 0
            return

        # CHECK when it's possible
        if current_bet == self.bet_this_round:
            self.current_decision = 0
            self.status = None
        else:
            p_win, p_std = self.analysis(board)
            # generate a random winning probability based on gaussian
            # distribution
            p_random = np.random.normal(loc=p_win, scale=p_std)
            if p_random < 0:
                p_random = 0
            elif p_random > 1:
                p_random = 1
            # FOLD when analysis result is negative
            if p_random * pot < (1 - p_random) * (
                current_bet - self.bet_this_round
            ):
                self.current_decision = "FOLD"
            # CALL when analysis result is positive
            elif p_random == 1:
                self.bet(self.stack - self.bet_this_round)
            else:
                bet_size = int(p_random / (1 - p_random) * pot)
                if bet_size < self.stack:
                    if bet_size < 2 * current_bet:
                        self.bet(current_bet - self.bet_this_round)
                    else:
                        self.bet(bet_size - self.bet_this_round)
                else:
                    self.bet(self.stack - self.bet_this_round)

    def analysis(self, board: list[Card]) -> tuple[float, float]:
        deck = Deck()
        my_possible_hands = []
        other_possible_hands = []

        for hand in itertools.combinations(
            [card for card in deck.deck if card not in (self.hand + board)],
            5 - len(board),
        ):
            other_possible_hands = [
                rank.BestHand(self.hand, board + list(hand)).best_hand
            ]
        for hand in itertools.combinations(
            [card for card in deck.deck if card not in (self.hand + board)],
            5 - len(board),
        ):
            other_possible_hands = [
                rank.BestHand(list(hand[:2]), list(hand[2:])).best_hand
            ]
        other_possible_hands.sort()

        p_win: list[float] = []
        for bh in my_possible_hands:
            p_win.append(
                (
                    bisect.bisect_left(other_possible_hands, bh)
                    + bisect.bisect_right(other_possible_hands, bh)
                )
                / 2
                / len(other_possible_hands)
            )
        return p_win.mean, np.std(p_win)

from dataclasses import dataclass
import itertools
import random
import bisect
import rank
import numpy as np
from deck import Deck, Card
from rank import BestHand


@dataclass
class Player:
    name: str = random.sample(["Henry", "Jiachen", "Jonathan"], 1)[0]
    stack: int = 0
    hand = []
    bet_this_round: int = 0
    current_decision: int | str | None = None
    status: (
        str | None
    ) = None  # 'little blind', 'big blind', 'dealer' 'highest bettor'

    def __repr__(self) -> str:
        return str((self.name, self.stack, self.hand))

    def draw_hand(self, deck: Deck) -> None:
        self.hand = [deck.draw() for _ in range(2)]

    def clear_hand(self) -> None:
        self.hand = []

    def best_hand(self, board: list[Card]) -> BestHand:
        return BestHand(self.hand, board)

    def reset_action(self):
        self.status = None
        self.current_decision = None
        self.bet_this_round = 0

    def bet(self, action: int) -> None:
        """
        Sets current_decision and bet_this_round attributs on self
        """
        self.current_decision = action
        self.bet_this_round += self.current_decision

    def decision(
        self,
        table_cards: list,
        current_bet: int,
        pot: int,
        asking_again_message: str = None,
    ) -> None:
        """
        Decision method prompts the user to choose an action for their turn.
        """
        # Skip player who is all-in
        if self.stack == 0:
            self.current_decision = 0
            return

        if asking_again_message is None:
            action = input(
                f"Awaiting {self.name}'s decision...\n"
                "\tcards on table:\t" + " ".join(map(str, table_cards)) + "\n"
                f"\tpot:\t\t${pot}\n"
                f"\tcurrent bet:\t${current_bet}\n"
                "\n"
                "\thand:\t\t" + " ".join(map(str, self.hand)) + "\n"
                f"\tstack:\t\t${self.stack}\n"
                f"\talready bet:\t${self.bet_this_round}\n"
                "Please make a decision: "
            )
        else:
            action = input(asking_again_message)
        try:
            action = int(action)
            if current_bet <= action <= self.stack:
                self.bet(action - self.bet_this_round)
            elif action < current_bet:
                self.decision(
                    table_cards,
                    current_bet,
                    pot,
                    asking_again_message="Your bet ain't high enough, cowbo"
                    "y. Try again: ",
                )
            elif action - self.bet_this_round > self.stack:
                self.decision(
                    table_cards,
                    current_bet,
                    pot,
                    asking_again_message="Not enough chips in the stack for"
                    " that one. Please bet a valid amount: ",
                )
        except ValueError:
            if action.upper() == "CALL":
                if self.bet_this_round < current_bet <= self.stack:
                    self.bet(current_bet - self.bet_this_round)
                elif current_bet == 0:
                    self.decision(
                        table_cards,
                        current_bet,
                        pot,
                        asking_again_message="You cannot call. Try something "
                        "else: ",
                    )
                else:
                    self.bet(self.stack)
            elif action.upper() == "CHECK":
                if current_bet == self.bet_this_round:
                    self.current_decision = 0
                    self.status = None
                else:
                    self.decision(
                        table_cards,
                        current_bet,
                        pot,
                        asking_again_message="You cannot check. Try something"
                        " else: ",
                    )
            elif action.upper() == "ALL IN":
                self.bet(self.stack)
            elif action.upper() == "FOLD":
                self.current_decision = "FOLD"
            else:
                self.decision(
                    table_cards,
                    current_bet,
                    pot,
                    asking_again_message="Invalid decision. Try something els"
                    "e: ",
                )


class NpcRandom(Player):
    """
    This is a NPC player that will randomly make decisions no matter what its
    hand and table cards are.
    """

    name: str = None

    def __init__(self, name, stack):
        self.name = name
        self.stack = stack

    def decision(
        self,
        table_cards: list,
        current_bet: int,
        pot: int,
        asking_again_message: str = None,
    ) -> None:
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

    def decision(
        self,
        table_cards: list,
        current_bet: int,
        pot: int,
        asking_again_message: str = None,
    ) -> None:
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
            p_win, p_std = self.analysis(table_cards)
            # FOLD when analysis result is negative
            if p_win * pot < (1 - p_win) * (current_bet - self.bet_this_round):
                self.current_decision = "FOLD"
            # CALL when analysis result is positive
            else:
                if current_bet <= self.stack:
                    self.bet(current_bet - self.bet_this_round)
                else:
                    self.bet(self.stack - self.bet_this_round)

    def analysis(self, table_cards: list[Card]) -> tuple[float, float]:
        deck = Deck()
        my_possible_hands = []
        other_possible_hands = []

        for hand in itertools.combinations(
            [
                card
                for card in deck.deck
                if card not in (self.hand + table_cards)
            ],
            5 - len(table_cards),
        ):
            other_possible_hands = [
                rank.BestHand(self.hand, table_cards + list(hand)).best_hand
            ]
        for hand in itertools.combinations(
            [
                card
                for card in deck.deck
                if card not in (self.hand + table_cards)
            ],
            5 - len(table_cards),
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
        return p_win.mean, float(np.std(p_win))


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

    def decision(
        self,
        table_cards: list,
        current_bet: int,
        pot: int,
        asking_again_message: str = None,
    ) -> None:
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
            p_win, p_std = self.analysis(table_cards)
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

    def analysis(self, table_cards: list[Card]) -> tuple[float, float]:
        deck = Deck()
        my_possible_hands = []
        other_possible_hands = []

        for hand in itertools.combinations(
            [
                card
                for card in deck.deck
                if card not in (self.hand + table_cards)
            ],
            5 - len(table_cards),
        ):
            other_possible_hands = [
                rank.BestHand(self.hand, table_cards + list(hand)).best_hand
            ]
        for hand in itertools.combinations(
            [
                card
                for card in deck.deck
                if card not in (self.hand + table_cards)
            ],
            5 - len(table_cards),
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
        return p_win.mean, float(np.std(p_win))

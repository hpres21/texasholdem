import random
from src.poker_game import Player


class NpcRandom(Player):
    name: str = None

    def __init__(self, name):
        self.name = name

    def decision(self, current_bet: int, pot: int) -> None:
        """
        Decision method prompts the npc to choose an action for their turn. The npc will decide randomly between all
        choices.
        """
        # Skip player who is all-in
        if self.stack == 0:
            self.current_decision = 0
            return

        possible_action = {"ALL IN", "FOLD", random.randint(current_bet, self.stack)}
        if current_bet > 0:
            possible_action.add("CALL")
        if current_bet == self.bet_this_round:
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
                    self.bet(self.stack)
            elif action.upper() == "CHECK":
                self.current_decision = 0
                self.status = None
            elif action.upper() == "ALL IN":
                self.bet(self.stack)
            elif action.upper() == "FOLD":
                self.current_decision = "FOLD"
            else:
                print("Invalid decision.")
                self.decision(current_bet, pot)


class NpcStrategy1(Player):
    name: str = None

    def __init__(self, name):
        self.name = name

    def decision(self, current_bet: int, pot: int) -> None:
        """
        Decision method prompts the npc to choose an action for their turn. The npc will decide based on the
        probability of winning.
        """
        # Skip player who is all-in
        if self.stack == 0:
            self.current_decision = 0
            return

        possible_action = {"ALL IN", "FOLD", random.randint(current_bet, self.stack)}
        if current_bet > 0:
            possible_action.add("CALL")
        if current_bet == self.bet_this_round:
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
                    self.bet(self.stack)
            elif action.upper() == "CHECK":
                self.current_decision = 0
                self.status = None
            elif action.upper() == "ALL IN":
                self.bet(self.stack)
            elif action.upper() == "FOLD":
                self.current_decision = "FOLD"
            else:
                print("Invalid decision.")
                self.decision(current_bet, pot)

    def winability(self):
        return 1
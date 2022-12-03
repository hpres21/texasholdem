from deck import Deck
from dataclasses import dataclass
from typing import Union
from table import Poker_Table

@dataclass
class Player:
    stack: int
    hand = []
    bet_this_round: int = 0
    current_decision: Union(int, str, None) = None
    
    def __repr__(self) -> str:
        return str((self.stack, self.bet_this_round, self.current_decision, self.hand))

    def draw_hand(self, deck: Deck)-> None:
        self.hand = [deck.draw() for _ in range(2)]

    def clear_hand(self)-> None:
        self.hand = []

    def decision(self, table: Poker_Table)-> None:
        """
        Decision method prompts the user to choose an action for their turn. 
        """
        action = input(f"You have {self.stack}, the current bet is {table.current_bet}. Please make a decision: ")
        try:
            action = int(action)
            if action >= 2*table.current_bet and action <= self.stack:
                self.current_decision = action - self.bet_this_round
                self.bet_this_round += self.current_decision
            else: 
                print("Please bet a valid amount")
                self.decision(table)
        except ValueError:
            if action.upper() == "CALL":
                if table.current_bet != self.bet_this_round:
                    self.current_decision = table.current_bet
                    self.bet_this_round += self.current_decision
                else:
                    print("You cannot Call")
                    self.decision(table)
            elif action.upper() == "CHECK":
                if table.current_bet == self.bet_this_round:
                    self.current_decision = 0
                else:
                    print("You cannot Check")
                    self.decision(table)
            elif action.upper() == "FOLD":
                self.current_decision = "FOLD"
                self.bet_this_round = 0
                self.current_decision = None
            else:
                print("Invalid decision.")
                self.decision(table)
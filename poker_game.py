from dataclasses import dataclass
from deck import Deck, Card
from typing import Union

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

    def decision(self, current_bet: int)-> None:
        """
        Decision method prompts the user to choose an action for their turn.
        """
        action = input(f"You have {self.stack}, the current bet is {current_bet}. Please make a decision: ")
        try:
            action = int(action)
            if action >= 2*current_bet and action <= self.stack:
                self.current_decision = action - self.bet_this_round
                self.bet_this_round += self.current_decision
            else:
                print("Please bet a valid amount")
                self.decision(current_bet)
        except ValueError:
            if action.upper() == "CALL":
                if current_bet.current_bet != self.bet_this_round:
                    self.current_decision = current_bet.current_bet
                    self.bet_this_round += self.current_decision
                else:
                    print("You cannot Call")
                    self.decision(current_bet)
            elif action.upper() == "CHECK":
                if current_bet.current_bet == self.bet_this_round:
                    self.current_decision = 0
                else:
                    print("You cannot Check")
                    self.decision(current_bet)
            elif action.upper() == "FOLD":
                self.current_decision = "FOLD"
                self.bet_this_round = 0
                self.current_decision = None
            else:
                print("Invalid decision.")
                self.decision(current_bet)

    def best_hand(self, board: list[Card]):
        ...


@dataclass
class Poker_Table:
    """
    Table class stores the information about the cards on the board, stack size, and players in the game.
    """
    max_num_players: int = 6
    big_blind: int = 2
    pot_size: int = 0
    players = []
    board = []
    current_bet: int  = 0

    def __repr__(self)-> str:
        """
        Not final form of function just for testing right now
        """
        return str((self.pot_size, self.current_bet, self.board, self.players))

    def add_player(self, player: Player)-> None:
        if len(self.players) <= self.max_num_players:
            self.players.append(player)
        else:
            print("Too many players. Wait for one to leave before you buy in.")

    def remove_player(self, player: Player)-> None:
        self.players.pop(self.players.index(player))
        print(f"Player {player} removed from game with ${player.stack}")

    def flop(self, deck: Deck)-> None:
        assert len(self.board) == 0
        drawn_cards = [deck.draw() for _ in range(3)]
        self.board.extend(drawn_cards)

    def draw_card(self, deck: Deck)-> None:
        assert len(self.board) <= 5
        self.board.append(deck.draw())

    def process_decision(self, player: Player)-> None:
        """
        Update table based on player's decision. All actions involve a bet >= 0, or a fold.
        """
        if player.current_decision == "FOLD":
            print("folding")
            self.players.pop(self.players.index(player))
        elif type(player.current_decision) == int:
            self.pot_size += player.current_decision
            player.stack -= player.current_decision
            self.current_bet = player.bet_this_round if player.bet_this_round > self.current_bet else self.current_bet

    def reset(self)-> None:
        self.pot_size = 0
        self.current_bet = 0
        self.players = []

    def end_round(self)-> None:
        assert len(self.players) == 1
        self.players[0].stack += self.pot_size
        self.end_round()

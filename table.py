from deck import Deck
from dataclasses import dataclass
from typing import Union
from player import Player

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

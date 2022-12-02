from deck import Deck
from dataclasses import dataclass

@dataclass
class Player:
    stack: int
    position: int
    hand = []
    is_big_blind = False
    is_small_blind = False
    is_dealer = False

    def draw_hand(self, deck):
        self.hand = [deck.draw() for _ in range(2)]

    def make_bet(self, table, bet):
        if bet <= self.stack and bet > 0:
            table.pot_size += bet
            self.stack -= bet
    
    def clear_hand(self):
        self.hand = []
    
    def set_big_blind(self):
        self.is_big_blind = True
        self.is_small_blind = False
        self.is_dealer = False
    
    def set_small_blind(self):
        self.is_small_blind = True
        self.is_big_blind = False
        self.is_dealer = False
    
    def set_dealer(self):
        self.is_dealer = True
        self.is_big_blind = False
        self.is_small_blind= False
    
    def clear_status(self):
        self.is_big_blind = False
        self.is_small_blind = False
        self.is_dealer = False


    

@dataclass
class Table:
    """
    Table class stores the information about the cards on the board, stack size, and players in the game. 
    """
    max_num_players: int = 6
    big_blind: int = 2
    pot_size = 0
    players = []
    board = []

    def __repr__(self):
        return str(self.board)

    def add_player(self, player):
        if len(self.players) <= self.max_num_players: 
            self.players.append(player)
        else: 
            print("Too many players. Wait for one to leave before you buy in.")
    
    def remove_player(self, player):
        self.players.pop(self.players.index(player))
        print(f"Player {player} removed from game with ${player.stack}")
    
    def flop(self, deck):
        assert len(self.board) == 0
        drawn_cards = [deck.draw() for _ in range(3)]
        self.board.extend(drawn_cards)
    
    def draw_card(self, deck):
        assert len(self.board) <= 5
        self.board.append(deck.draw())

from __future__ import annotations
from dataclasses import dataclass
from deck import Deck
from player import Player


@dataclass
class PokerTable:
    """
    Table class stores the information about the cards on the board,
    stack size, and players in the game.
    """

    max_num_players: int = 6
    big_blind: int = 2
    pot_size: int = 0
    players = []
    active_players = []
    board = []
    current_bet: int = 0
    deck = Deck()

    def __repr__(self) -> str:
        """
        Not final form of function just for testing right now
        """
        return str(
            (self.pot_size, self.current_bet, self.board, self.active_players)
        )

    def add_player(self, player: Player) -> None:
        if len(self.players) <= self.max_num_players:
            self.players.append(player)
            self.active_players.append(player)
        else:
            print("Too many players. Wait for one to leave before you buy in.")

    def sit_out_player(self, player: Player) -> None:
        """
        The Player has lost the current round, they will sit out.
        """
        self.active_players.pop(self.active_players.index(player))
        player.reset_action()

    def remove_player(self, player: Player) -> None:
        """
        player has lost all their chips. they can no longer play
        should only be called after sit_out_player
        """
        self.players.pop(self.players.index(player))

    def flop(self) -> None:
        assert len(self.board) == 0
        drawn_cards = [self.deck.draw() for _ in range(3)]
        self.board.extend(drawn_cards)

    def draw_card(self) -> None:
        assert len(self.board) <= 5
        self.board.append(self.deck.draw())

    def set_highest_bettor(self, player: Player) -> None:
        for p in self.active_players:
            if p.status != "big blind":
                p.status = None
        player.status = "highest bettor"

    def process_decision(self, player: Player) -> None:
        """
        Update table based on player's decision.
        All actions involve a bet >= 0, or a fold.
        """
        if player.current_decision == "FOLD":
            print(f"\n{player.name} folds with a stack of ${player.stack}\n")
            self.sit_out_player(player)
        elif type(player.current_decision) == int:
            self.pot_size += player.current_decision
            player.stack -= player.current_decision
            if player.bet_this_round > self.current_bet:
                self.current_bet = player.bet_this_round
                self.set_highest_bettor(player)
                print(
                    f"{player.name} bets ${player.current_decision},"
                    f" raise current bet to ${self.current_bet}"
                )
            else:
                print(f"{player.name} bets ${player.current_decision}")

    def end_action(self) -> None:
        """
        Ends round of betting
        """
        self.current_bet = 0
        for player in self.active_players:
            player.reset_action()

    def clear_players(self) -> None:
        self.players = []

    def reset(self) -> None:
        """
        Resets table status
        """
        self.pot_size = 0
        # self.players = []
        # self.active_players = []
        self.board = []
        self.current_bet = 0
        self.deck = Deck()

    def determine_winner(self) -> Player:
        """
        Calculate the winning active player
        """
        game_hands = [p.best_hand(self.board) for p in self.active_players]
        besthand = max(game_hands)
        i = game_hands.index(besthand)
        return self.active_players[i], game_hands

    def payout(self, player: Player) -> None:
        """
        Pay winning player
        """
        player.stack += self.pot_size
        self.pot_size = 0
        for p in self.players:
            p.bet_this_round = 0

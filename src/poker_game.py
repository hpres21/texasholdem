from __future__ import annotations
import random
from dataclasses import dataclass
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

    def decision(self, current_bet: int, pot: int) -> None:
        """
        Decision method prompts the user to choose an action for their turn.
        """
        # Skip player who is all-in
        if self.stack == 0:
            self.current_decision = 0
            return

        action = input(
            f"{self.name} has ({self.hand},  ${self.stack}). "
            f"The current pot is ${pot}. The current bet is ${current_bet}. "
            f"You have put in ${self.bet_this_round} already. "
            "Please make a decision: "
        )
        try:
            action = int(action)
            if current_bet <= action <= self.stack:
                self.bet(action - self.bet_this_round)
            else:
                print("Please bet a valid amount")
                self.decision(current_bet, pot)
        except ValueError:
            if action.upper() == "CALL":
                if self.bet_this_round < current_bet <= self.stack:
                    self.bet(current_bet - self.bet_this_round)
                elif current_bet == 0:
                    print("You cannot call")
                    self.decision(current_bet, pot)
                else:
                    self.bet(self.stack)
            elif action.upper() == "CHECK":
                if current_bet == self.bet_this_round:
                    self.current_decision = 0
                    self.status = None
                else:
                    print("You cannot check")
                    self.decision(current_bet, pot)
            elif action.upper() == "ALL IN":
                self.bet(self.stack)
            elif action.upper() == "FOLD":
                self.current_decision = "FOLD"
            else:
                print("Invalid decision.")
                self.decision(current_bet, pot)


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
        print(f"Player {player} removed from game with ${player.stack}")

    def remove_player(self, player: Player) -> None:
        """
        player has lost all their chips. they can no longer play
        should only be called after sit_out_player
        """
        self.players.pop(self.players.index(player))
        print(f"Player {player} removed from game with ${player.stack}")

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
        print(player.status)

    def process_decision(self, player: Player) -> None:
        """
        Update table based on player's decision.
        All actions involve a bet >= 0, or a fold.
        """
        if player.current_decision == "FOLD":
            print(f"{player.name} folds")
            self.sit_out_player(player)
        elif type(player.current_decision) == int:
            self.pot_size += player.current_decision
            player.stack -= player.current_decision
            if player.bet_this_round > self.current_bet:
                self.current_bet = player.bet_this_round
                self.set_highest_bettor(player)
            print(f"{player.name} bets ${player.current_decision}")

    def end_action(self) -> None:
        self.current_bet = 0
        for player in self.active_players:
            player.reset_action()

    def clear_players(self) -> None:
        self.players = []

    def reset(self) -> None:
        self.pot_size = 0
        self.players = []
        self.active_players = []
        self.board = []
        self.current_bet = 0
        self.deck = Deck()

    def determine_winner(self) -> Player:
        game_hands = [p.best_hand(self.board) for p in self.active_players]
        besthand = max(game_hands)
        i = game_hands.index(besthand)
        return self.active_players[i]

    def payout(self, player: Player) -> None:
        player.stack += self.pot_size
        self.pot_size = 0

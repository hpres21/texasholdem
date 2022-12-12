import random
from dataclasses import dataclass
from deck import Deck, Card
from rank import BestHand
from typing import Union


@dataclass
class Player:
    name: str = random.sample(["Henry", "Jiachen", "Jonathan"], 1)[0]
    stack: int = 0
    hand = []
    bet_this_round: int = 0
    current_decision: Union[int, str, None] = None
    status: str = None # 'little blind', 'big blind', 'dealer'

    def __repr__(self) -> str:
        return str(
            (self.name, self.stack, self.bet_this_round, self.current_decision, self.hand)
        )

    def draw_hand(self, deck: Deck) -> None:
        self.hand = [deck.draw() for _ in range(2)]

    def clear_hand(self) -> None:
        self.hand = []

    def decision(self, current_bet: int) -> None:
        """
        Decision method prompts the user to choose an action for their turn.
        """
        action = input(
            f"You have {self.stack}. The current bet is {current_bet}. "
            "Please make a decision: "
        )
        try:
            action = int(action)
            if action >= 2 * current_bet and action <= self.stack:
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

    def best_hand(self, board: list[Card]) -> BestHand:
        return BestHand(self.hand, board)


@dataclass
class PokerTable:
    """
    Table class stores the information about the cards on the board,
    stack size, and players in the game.
    """

    max_num_players: int = 6
    big_blind: int = 2
    pot_size: int = 0
    all_players = []
    current_players = []
    board = []
    current_bet: int = 0
    deck = Deck()

    def __repr__(self) -> str:
        """
        Not final form of function just for testing right now
        """
        return str((self.pot_size, self.current_bet, self.board, self.current_players))

    def add_player(self, player: Player) -> None:
        if len(self.all_players) <= self.max_num_players:
            self.all_players.append(player)
            self.current_players.append(player)
        else:
            print("Too many players. Wait for one to leave before you buy in.")

    def sit_out_player(self, player: Player) -> None:
        """
        player has lost the current round, they will sit out
        """
        self.current_players.pop(self.current_players.index(player))
        print(f"Player {player} removed from game with ${player.stack}")

    def banish_player(self, player: Player) -> None:
        """
        player has lost all their chips. they can no longer play
        should only be called after sit_out_player
        """
        self.all_players.pop(self.all_players.index(player))
        print(f"Player {player} removed from game with ${player.stack}")

    def flop(self) -> None:
        assert len(self.board) == 0
        drawn_cards = [self.deck.draw() for _ in range(3)]
        self.board.extend(drawn_cards)

    def draw_card(self) -> None:
        assert len(self.board) <= 5
        self.board.append(self.deck.draw())

    def process_decision(self, player: Player) -> None:
        """
        Update table based on player's decision.
        All actions involve a bet >= 0, or a fold.
        """
        if player.current_decision == "FOLD":
            print(f"{player.name} folds")
            self.players.pop(self.players.index(player))
        elif type(player.current_decision) == int:
            self.pot_size += player.current_decision
            player.stack -= player.current_decision
            if player.bet_this_round > self.current_bet:
                self.current_bet = player.bet_this_round
            print(f"{player.name} bets {player.current_decision} chips")

    def reset(self) -> None:
        self.pot_size = 0
        self.players = []
        self.board = []
        self.current_bet = 0
        self.deck = Deck()

    def determine_winner(self) -> Player:
        game_hands = [p.best_hand(self.board) for p in self.players]
        besthand = max(game_hands)
        i = game_hands.index(besthand)
        return self.players[i]

    def payout(self, player: Player) -> None:
        player.stack += self.pot_size
        # self.end_round()

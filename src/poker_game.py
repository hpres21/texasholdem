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
        self.players = []
        self.active_players = []
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
        return self.active_players[i]

    def payout(self, player: Player) -> None:
        """
        Pay winning player
        """
        player.stack += self.pot_size
        self.pot_size = 0

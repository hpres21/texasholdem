import numpy as np
from poker_game import Player, PokerTable
from npc import NpcRandom, NpcStrategy1
from printing import print_title, print_cowboy, print_cards


def run_player_decisions(table: PokerTable) -> int:
    """
    This function asks each player for their decision
    :during the current round of action
    """
    small_blind = table.big_blind // 2

    player = table.active_players[
        0
    ]  # first player in list is always little blind

    num_active_players = len(table.active_players)
    while num_active_players > 1 and player.status != "highest bettor":
        player_index = table.active_players.index(player)
        next_player = table.active_players[
            (player_index + 1) % num_active_players
        ]

        if player.status == "little blind":  # pre flop forced bet
            player.bet(small_blind)
            table.process_decision(player)
        elif player.status == "big blind":  # pre flop forced bet
            player.bet(table.big_blind)
            table.process_decision(player)
        elif player_index == 0 and table.current_bet == 0:
            player.decision(table.board, table.current_bet, table.pot_size)
            table.process_decision(player)
            player.status = "highest bettor"
        else:
            player.decision(table.board, table.current_bet, table.pot_size)
            table.process_decision(player)
        player = next_player
        num_active_players = len(table.active_players)
    return num_active_players


def end_round(table: PokerTable, winner: Player) -> None:
    table.payout(winner)
    table.reset()
    table.players = np.roll(table.players, -1)
    table.active_players = [p for p in table.players if p.stack > 0]


def run_round(pokertable: PokerTable):
    """
    This function holds the logic to play a single round of poker
    """

    # deal players their cards
    for player in pokertable.active_players:
        player.draw_hand(pokertable.deck)

    # pre flop
    num_remaining_players = run_player_decisions(pokertable)

    if num_remaining_players == 1:
        winner = pokertable.active_players[0]
        end_round(pokertable, winner)
        pokertable.reset()
        print(f"\n{winner.name} won the round.\n")
        return
    else:
        pokertable.end_action()
        pokertable.flop()
        print("\nThe dealer lays down cards.")
        print(print_cards(pokertable.board) + "\n")

    # flop
    num_remaining_players = run_player_decisions(pokertable)

    if num_remaining_players == 1:
        winner = pokertable.active_players[0]
        end_round(pokertable, winner)
        print(f"\n{winner.name} won the round.\n")
        return
    else:
        pokertable.end_action()
        pokertable.draw_card()
        print("\nThe dealer lays down a card.")
        print(print_cards(pokertable.board) + "\n")

    # turn
    num_remaining_players = run_player_decisions(pokertable)

    if num_remaining_players == 1:
        winner = pokertable.active_players[0]
        end_round(pokertable, winner)
        print(f"\n{winner.name} won the round.\n")
        return
    else:
        pokertable.end_action()
        pokertable.draw_card()
        print("\nThe dealer lays down a card.")
        print(print_cards(pokertable.board) + "\n")

    # river
    num_remaining_players = run_player_decisions(pokertable)

    if num_remaining_players == 1:
        winner = pokertable.active_players[0]
        end_round(pokertable, winner)
        return
    else:
        winner = pokertable.determine_winner()
        end_round(pokertable, winner)
        print(f"\n{winner.name} won the round.\n")
        return


def initialize_game(dict_of_player_types=None, stack_size=1000):
    """
    set up an instance of PokerTable in order to run a game.
    if dict_of_player_types is None, assume a human player is setting up the
    game and print a cute UI to help them add players to the table.
    otherwise, dict_of_player_types should be of the form
    {player_name: player_type}
    """
    if dict_of_player_types is None:
        print_title()
        input("Press Enter to continue...")
        print_cowboy()
        print("Welcome to the table, partner.")
        if stack_size is None:
            stack_size = int(input("Enter the stack size: "))
            print()
        n_players = int(input("Enter the number of players: "))
        print()
        pokertable = PokerTable(max_num_players=n_players)
        print("Enter type for each player:")
        print("\t'h'\thuman")
        print("\t'r'\trandom NPC")
        print("\t'1'\tstrategic npc 1")
        for i in range(n_players):  # add players to table6
            while True:
                try:
                    player_type = input(f"p{i} type: ")
                    if player_type not in ["h", "r", "1"]:
                        raise ValueError
                except ValueError:
                    print(
                        "Woah there! I don't reckon that's a valid player typ"
                        "e. Try again..."
                    )
                    continue
                else:
                    break
            if player_type == "h":
                human_name = input(f"Enter a name for p{i}: ")
                if human_name == "":
                    human_name = f"p{i}"
                pokertable.add_player(
                    Player(name=human_name, stack=stack_size)
                )
            elif player_type == "r":
                pokertable.add_player(
                    NpcRandom(name=f"p{i}", stack=stack_size)
                )
            elif player_type == "1":
                pokertable.add_player(
                    NpcStrategy1(name=f"p{i}", stack=stack_size)
                )
    else:
        pokertable = PokerTable(max_num_players=len(dict_of_player_types))
        for name, player_type in dict_of_player_types.items():
            if player_type == "h":
                pokertable.add_player(Player(name=name, stack=stack_size))
            elif player_type == "r":
                pokertable.add_player(NpcRandom(name=name, stack=stack_size))
            elif player_type == "1":
                pokertable.add_player(
                    NpcStrategy1(name=name, stack=stack_size)
                )
    return pokertable


def run_game(dict_of_player_types=None, stack_size=1000):
    pokertable = initialize_game(dict_of_player_types, stack_size)
    blind_index = 0
    while len(pokertable.players) > 1:
        # preflop
        pokertable.active_players[0].status = "little blind"
        pokertable.active_players[1].status = "big blind"
        run_round(pokertable)
        for player in pokertable.players:
            if player.stack <= 0:
                pokertable.sit_out_player(player)
                pokertable.remove_player(player)
                print(
                    f"\n{player.name} left the table 'cause they ran out of c"
                    "hips!\n"
                )
        blind_index += 1
    print_cowboy()
    print(
        f"\nCongratulations {pokertable.players[0].name}! You won the game.\n"
    )

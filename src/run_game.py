from poker_game import Player, PokerTable
from npc import NpcRandom, NpcStrategy1
from printing import print_title, print_cowboy

def run_player_decisions(table: PokerTable) -> int:
    """
    This function asks each player for their decision
    :during the current round of action
    """
    small_blind = table.big_blind // 2

    player = table.active_players[0]

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
            player.status = "highest bettor"
        else:
            player.decision(table.current_bet, table.pot_size)
            table.process_decision(player)
        player = next_player
        num_active_players = len(table.active_players)
    return num_active_players


def end_round(table: PokerTable, winner: Player) -> None:
    table.payout(winner)
    table.reset()


def run_round(pokertable: PokerTable):
    """
    This function holds the logic to play a single round of poker
    """
    # preflop
    pokertable.active_players[0].status = "little blind"
    pokertable.active_players[1].status = "big blind"

    for player in pokertable.active_players:
        player.draw_hand(pokertable.deck)

    num_remaining_players = run_player_decisions(pokertable)

    if num_remaining_players == 1:
        winner = pokertable.active_players[0]
        end_round(pokertable, winner)
        pokertable.reset()
        print(winner)
        return
    else:
        pokertable.end_action()
        pokertable.flop()
        print(pokertable.board)

    # flop
    num_remaining_players = run_player_decisions(pokertable)

    if num_remaining_players == 1:
        winner = pokertable.active_players[0]
        end_round(pokertable, winner)
        print(winner)
        return
    else:
        pokertable.end_action()
        pokertable.draw_card()
        print(pokertable.board)

    # turn
    num_remaining_players = run_player_decisions(pokertable)

    if num_remaining_players == 1:
        winner = pokertable.active_players[0]
        end_round(pokertable, winner)
        print(winner)
        return
    else:
        pokertable.end_action()
        pokertable.draw_card()
        print(pokertable.board)

    # river
    num_remaining_players = run_player_decisions(pokertable)

    if num_remaining_players == 1:
        winner = pokertable.active_players[0]
        end_round(pokertable, winner)
        return
    else:
        print(pokertable.board)
        winner = pokertable.determine_winner()
        end_round(pokertable, winner)
        print(winner)
        return


# initialize game
stack_size = 1000
print_title()
input("Press Enter to continue...")
print_cowboy()
print("Welcome to the table, partner.")
n_players = int(input("Enter the number of players: "))
print()
pokertable = PokerTable(max_num_players=n_players)
print("Enter type for each player:")
print("\t'h'\thuman")
print("\t'r'\trandom NPC")
print("\t'1'\tstrategic npc 1")
for i in range(n_players):  # add players to table6
    player_type = input(f"p{i} type: ")
    if player_type == 'h':
        human_name = input(f"Enter a name for p{i}: ")
        if human_name == "":
            human_name = f"p{i}"
        pokertable.add_player(Player(name = human_name, stack = stack_size))
    elif player_type == 'r':
        pokertable.add_player(NpcRandom(name = f"p{i}", stack = stack_size))
    elif player_type == '1':
        pokertable.add_player(NpcStrategy1(name = f"p{i}", stack = stack_size))
print(pokertable)
run_round(pokertable)

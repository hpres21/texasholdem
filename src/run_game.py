# import sys
# from src.deck import Card, Deck
# from src.rank import BestHand
from src.poker_game import Player, PokerTable

# initialize game
stack_size = 1000
n_players = 3
# n_players = int(input("Enter number of players: "))
pokertable = PokerTable(max_num_players=n_players)
for i in range(n_players):  # add players to table6
    pokertable.add_player(Player(name="p" + str(i), stack=stack_size))
print(pokertable)


def run_player_decisions(table: PokerTable) -> int:
    """
     This function asks each player for their decision for the current round of action
     """
    small_blind = table.big_blind // 2

    player = table.active_players[0]

    num_active_players = len(table.active_players)
    while num_active_players > 1 and player.status != "highest bettor":
        player_index = table.active_players.index(player)
        next_player = table.active_players[(player_index + 1) % num_active_players]

        if player.status == 'little blind':  # pre flop forced bet
            player.bet(small_blind)
            table.process_decision(player)
        elif player.status == 'big blind':  # pre flop forced bet
            player.bet(table.big_blind)
            table.process_decision(player)
        elif player_index == 0 and table.current_bet == 0:
            player.status = "highest bettor"
        else:
            player.decision(table.current_bet, table.pot_size)
            table.process_decision(player)
        print(player.status)
        player = next_player
        num_active_players = len(table.active_players)
    return num_active_players


def end_round(table: pokertable, winner: Player) -> None:
    pokertable.payout(winner)
    pokertable.reset()


def run_round(pokertable: PokerTable):
    # preflop
    pokertable.active_players[0].status = 'little blind'
    pokertable.active_players[1].status = 'big blind'

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


if __name__ == "main":
    run_round(pokertable)

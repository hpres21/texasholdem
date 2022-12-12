from deck import Card, Deck
from rank import BestHand
from poker_game import Player, PokerTable


# initialize game
stack_size = 1000
n_players = int(input("Enter number of players: "))
pokertable = PokerTable()
for i in range(n_players): # add players to table
    pokertable.add_player(Player(name = "p" + str(i), stack = stack_size))

# first round
pokertable.current_players[0].status = 'little blind'
pokertable.current_players[1].status = 'big blind'
for p in pokertable.current_players:
    if p.status == 'little blind': # pre flop
        p.current_decision = 1
        p.bet_this_round = 1
        p.status = None
    elif p.status == 'big blind': # pre flop
        p.current_decision = 2
        p.bet_this_round = 2
        p.status = None
    else:
        p.decision(pokertable.current_bet)
    pokertable.process_decision(p)
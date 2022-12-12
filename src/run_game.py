from deck import Card, Deck
from rank import BestHand
from poker_game import Player, PokerTable


stack_size = 1000
n_players = int(input("Enter number of players: "))
pokertable = PokerTable()
for i in range(n_players): # add players to table
    pokertable.add_player(Player(name = "p" + str(i + 1), stack = stack_size))

print("Finished setting up game.")
print(pokertable.players)
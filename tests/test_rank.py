import table
from deck import Card
import rank

pocket = [Card(value=10, suit='s'), Card(value=10, suit='h')]
board = [Card(value=10, suit='c'), Card(value=10, suit='d'), Card(value=9, suit='d'), Card(value=8, suit='d'), Card(value=7, suit='d')]

A = rank(pocket, board)
print(A.besthand)
print(A.rank)
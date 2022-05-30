import random
from Source.min_max import MinMax
import sys

from Source.exceptions import AgentException


class MinMaxAgent:
    def __init__(self, my_token='o'):
        self.my_token = my_token

    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')
        else:
            minmax = MinMax(connect4, self.my_token)

            move = minmax.choose_best_move()

            return move

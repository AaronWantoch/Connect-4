import random
import sys
import numpy
import math
from Source.connect4 import Connect4


class MCTree:

    def __init__(self, parent, actionIndex):
        self.t = 0
        self.n = 0
        self.actionIndex = actionIndex
        self.parent: MCTree = parent
        self.children = []

    def calc_UCB1(self):
        if self.n == 0:
            return sys.maxsize
        else:
            return self.t / self.n + 2 * math.sqrt(numpy.log(self.parent.n / self.n))

    def expantion(self, possibleDrops):
        for pd in possibleDrops:
            self.children.append(MCTree(self, pd))

    def rollout(self, connect4, myToken):
        while not(connect4.check_game_over()):
            connect4.drop_token(random.choice(connect4.possible_drops()))

        if connect4.wins == myToken:
            return 100
        elif connect4.wins != myToken:
            return -10
        else:
            return 0

    def update(self, value):
        self.t += value
        self.n += 1
        if self.parent is not None:
            self.parent.update(value)
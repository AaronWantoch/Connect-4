from sqlite3 import connect
from exceptions import GameplayException
from connect4 import Connect4
from randomadent import RandomAgent
import copy
import sys

class GameTree:
    #Values: -1 = o loses 0 = tie 1 = o wins
    def __init__(self, connect, token, leadingMove=None, height=0, alfa=-sys.maxsize - 1, beta=sys.maxsize):
        self.connect = connect
        self.who = token
        self.leadingMove = leadingMove
        self.children = []
        self.height = height
        self.alfa = alfa
        self.beta = beta
        self.v = self.value()

    def value(self):
        if self.height==6:
            self.v=self.aprox()
            return 0

        if self.connect.check_game_over():
            if self.connect.wins == None:
                self.v=0
            elif self.connect.wins == self.who:
                self.v=1
            else:
                self.v=-1
            return self.v
        


        possibilities = self.connect.possible_drops()
        for move in possibilities:
            connectCopy = copy.deepcopy(self.connect)
            connectCopy.drop_token(move)  
            child = GameTree(connectCopy, self.who, move, self.height+1, self.alfa, self.beta)
            self.children.append(child)
            if self.connect.who_moves == self.who:
                if child.v > self.alfa:
                    self.alfa = child.v
                else:
                    return self.alfa
            else:
                if child.v < self.beta:
                    self.beta = child.v
                else:
                    return self.beta

        if self.connect.who_moves != self.who:
            self.v = min(self.children, key=lambda node: node.v).v
        else:
            self.v = max(self.children, key=lambda node: node.v).v
        return self.v
    def aprox(self):
        total = 0
        result = 0
        for four in self.connect.iter_fours():
            if four.count(self.who)==3 and four.count('_')==1:
                result +=5 
            elif four.count(self.who)==2 and four.count('_')==2:
                result += 3
            elif four.count(self.who)==0 and four.count('_')==1:
                result -=5 
            elif four.count(self.who)==0 and four.count('_')==2:
                result -= 3
            total+=5

        return result/total


class TreeAgent: 
    def __init__(self, my_token='o'):
        self.my_token = my_token
    def decide(self, connect):
        tree = GameTree(connect, self.my_token)
        return max(tree.children, key=lambda node: node.v).leadingMove



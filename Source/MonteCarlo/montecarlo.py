import random
import sys
import copy
from Source.MonteCarlo.mctree import MCTree
from Source.connect4 import Connect4


class MonteCarlo:

    def __init__(self, connect: Connect4, myToken):
        self.game = connect
        self.simulation = Connect4()
        self.simulation.board = copy.deepcopy(connect.board)
        self.simulation.who_moves = myToken
        self.myToken = myToken
        self.limit = 10000000


    def final_decision(self, root):
        maxUCB1Child = None
        maxUCB1 = -sys.maxsize
        # find child that maximizes UCB1
        for c in root.children:
            ucb1 = c.calc_UCB1()
            if maxUCB1 < ucb1:
                maxUCB1Child = c
                maxUCB1 = ucb1

        return maxUCB1Child.actionIndex

    def choose_move(self, current, limit, root):

        if limit and not (self.game.check_game_over()) :
            if current.children:  # not a leaf node # looking for a max child
                maxUCB1Child = None
                maxUCB1 = -sys.maxsize
                # find child that maximizes UCB1
                for c in current.children:
                    ucb1 = c.calc_UCB1()
                    if maxUCB1 < ucb1:
                        maxUCB1Child = c
                        maxUCB1 = ucb1
                self.simulation.drop_token(maxUCB1Child.actionIndex)
                if self.simulation.game_over:
                    return self.final_decision( root)
                self.simulation.drop_token(random.choice(self.simulation.possible_drops()))
                if self.simulation.game_over:
                    return self.final_decision( root)
                return self.choose_move(maxUCB1Child, limit, root)

            else:  # a leaf node
                if current.n == 0:
                    current.update(current.rollout(self.simulation, self.myToken))
                    self.simulation = Connect4()
                    self.simulation.board = copy.deepcopy(self.game.board)
                    self.simulation.who_moves = self.myToken
                    return self.choose_move(root, limit - 1, root)
                else:
                    current.expantion(self.game.possible_drops())
                    self.simulation.drop_token(self.game.possible_drops()[0])
                    if self.simulation.game_over:
                        return self.final_decision(root)
                    self.simulation.drop_token(random.choice(self.simulation.possible_drops()))
                    if self.simulation.game_over:
                        return self.final_decision(root)
                    return self.choose_move(current.children[0], limit, root)
        else:
            return self.final_decision(root)

    def choose_best_move(self):
        root = MCTree(None, 0)
        for pd in self.simulation.possible_drops():
            root.children.append(MCTree(root, pd))
        move = self.choose_move(root, self.limit, root)
        return move

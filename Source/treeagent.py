from tree import GameTree

class TreeAgent:
    def __init__(self, my_token='o'):
        self.my_token = my_token
    def decide(self, connect):
        tree = GameTree(connect, self.my_token)
        return max(tree.children, key=lambda node: node.v).leadingMove
from Source.MonteCarlo.montecarlo import MonteCarlo
from Source.exceptions import AgentException


class MonteCarlo_Agent:
    def __init__(self, my_token='o'):
        self.my_token = my_token

    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')
        else:
            monteCarlo = MonteCarlo(connect4, self.my_token)
            move = monteCarlo.choose_best_move()
            print(move.__class__)
            return move

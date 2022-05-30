from Source.Genetic.minmax_custom_agent import MinMaxCustomAgent
from exceptions import GameplayException
from connect4 import Connect4
from random_agent import RandomAgent
from Source.MonteCarlo.montecarlo_agent import MonteCarlo_Agent

connect4 = Connect4()
# mój chad agent
#agent1 = MinMaxCustomAgent('o', 0.9, 9.2, 5.3, 0.5, -3.0, 1.9 )

# zwykły virgin grajek
#agent2 = MinMaxCustomAgent('x')

agent1 = MonteCarlo_Agent("o")
#agent1 = RandomAgent("x")
agent2 = MinMaxCustomAgent('x', 0.9, 9.2, 5.3, 0.5, -3.0, 1.9 )

while not connect4.game_over:
    connect4.draw()
    try:
        if connect4.who_moves == agent1.my_token:
            n_column = agent1.decide(connect4)
        else:
            n_column = agent2.decide(connect4)
        connect4.drop_token(n_column)
    except (ValueError, GameplayException):
        pass

connect4.draw()

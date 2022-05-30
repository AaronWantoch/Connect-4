from Source.Genetic.minmax_agent_custom import MinMaxCustomAgent
from Source.exceptions import GameplayException
from Source.connect4 import Connect4
from Source.minmax_agent import MinMaxAgent
from Source.random_agent import RandomAgent
from montecarlo_agent import MonteCarlo_Agent

connect4 = Connect4()
agent1 = RandomAgent("o")
agent2 = MonteCarlo_Agent("x")

winrand = 0
winmc = 0
for i in range(100):
    while not connect4.game_over:
        #connect4.draw()
        try:
            if connect4.who_moves == agent1.my_token:
                n_column = agent1.decide(connect4)
            else:
                n_column = agent2.decide(connect4)
                print(n_column)
            connect4.drop_token(n_column)
        except (ValueError, GameplayException):
            print('invalid move')
    if connect4.game_over:
        if connect4.wins == "o":
            winrand += 1
        else:
            winmc += 1

    #connect4.draw()

print(f"random:   {winrand}")
print(f"mc    :   {winmc}")


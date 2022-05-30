from Source.Genetic.minmax_custom_agent import MinMaxCustomAgent
from Source.exceptions import GameplayException
from Source.connect4 import Connect4
from Source.minmax_agent import MinMaxAgent
from Source.random_agent import RandomAgent
from montecarlo_agent import MonteCarlo_Agent

connect4 = Connect4()
agent1 = MonteCarlo_Agent("x")
agent2 = MinMaxCustomAgent("o")
xwin = 0
owin = 0
for i in range(100):
    print(i)
    while not connect4.game_over:
        #connect4.draw()
        try:
            if connect4.who_moves == agent1.my_token:
                n_column = agent1.decide(connect4)
            else:
                n_column = agent2.decide(connect4)
            connect4.drop_token(n_column)
        except (ValueError, GameplayException):
            pass
    if connect4.game_over:
        if connect4.wins == "o":
            owin += 1
        elif connect4.wins == "x":
            xwin += 1

    connect4 = Connect4()
    #connect4.draw()

print(f"owin:   {owin}")
print(f"xwin:   {xwin}")


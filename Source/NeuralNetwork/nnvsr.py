from exceptions import GameplayException
from connect4 import Connect4
from neural_network_env import Connect4Enviorment
from reinforcment_learning import RLAgent
from random_agent import RandomAgent
from Genetic.minmax_custom_agent import MinMaxCustomAgent

connect4 = Connect4(7, 6)
env = Connect4Enviorment(connect4, 'x', MinMaxCustomAgent('o', 0.9, 9.2, 5.3, 0.5, -3.0, 1.9))

rl_agent = RLAgent(connect4, env)
rl_agent.train()



env.close()

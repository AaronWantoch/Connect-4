from exceptions import GameplayException
from connect4 import Connect4
from neural_network_env import Connect4Enviorment
from reinforcment_learning import RLAgent
from random_agent import RandomAgent
from Genetic.minmax_custom_agent import MinMaxCustomAgent

connect4 = Connect4(7, 6)
env = Connect4Enviorment(connect4, 'o', MinMaxCustomAgent('x'))

rl_agent = RLAgent(connect4, env)
rl_agent.train(10000)
rl_agent.save_model()


env.close()

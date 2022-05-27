from exceptions import GameplayException
from connect4 import Connect4
from random_agent import RandomAgent
from neural_network_env import Connect4Enviorment
from reinforcment_learning import RLAgent

connect4 = Connect4(7, 6)
env = Connect4Enviorment(connect4, 'o')

rl_agent = RLAgent(connect4, env)
rl_agent.train()
random_agent = RandomAgent('x')


while not connect4.game_over:
    # Take a random action
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)
    # Render the game
    env.render()

    if done == True:
        break

    n_column = random_agent.decide(connect4)
    connect4.drop_token(n_column)
    env.render()

    if connect4.game_over:
        break

env.close()

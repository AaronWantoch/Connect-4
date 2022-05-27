import gym
import numpy as np
from gym import Env, spaces
from connect4 import Connect4
from dynamic_actions import DynamicActionsSpace

class Connect4Enviorment(Env):
    def __init__(self, connect, token):
        super(Connect4Enviorment, self).__init__()
        self.game = connect
        self.token = token

        # Define a 2-D observation space
        self.observation_shape = (self.game.height, self.game.width, 1)
        self.observation_space = spaces.Box(low=-np.ones(self.observation_shape),
                                            high=np.ones(self.observation_shape),
                                            dtype=np.int8)
        self.action_space = spaces.Discrete(self.game.width)


    def reset(self, **kwargs):
        # return the observation
        self.game = Connect4(self.game.width, self.game.height)
        return Connect4()

    def render(self, mode="human"):
        self.game.draw()

    def step(self, action):
        # consider sooner player wins bigger reward he gets
        self.game.drop_token(action)

        reward = 0
        done = False
        if self.game.game_over:
            if self.game.wins == self.token:
                reward = 1
            else:
                reward = -1
            done = True

        self.action_space = DynamicActionsSpace(self.game.possible_drops())

        return self.observation_space, reward, done, []

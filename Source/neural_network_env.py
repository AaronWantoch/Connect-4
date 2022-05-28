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
        self.observation_space = spaces.Dict({
            'board': spaces.Box(low=-1, high=1, shape=(self.game.height, self.game.width), dtype=np.uint8)
            })
        self.action_space = spaces.Discrete(self.game.width)



    def reset(self, **kwargs):
        # return the observation
        self.game = Connect4(self.game.width, self.game.height)
        self.canvas = {0: np.zeros(self.observation_shape)[:, :, 0]}

        return self.canvas

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

        return self.canvas, reward, done, []

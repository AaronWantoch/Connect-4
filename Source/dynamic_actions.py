import gym
import numpy as np
from gym import spaces


class DynamicActionsSpace(spaces.Discrete):
    def __init__(self, actions):
        self.n = len(actions)
        super().__init__(self.n)

        # initially all actions are available
        self.available_actions = np.array(actions)

    def sample(self):
        return np.random.choice(self.available_actions)

    def contains(self, x):
        return x in self.available_actions

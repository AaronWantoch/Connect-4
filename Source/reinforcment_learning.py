import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, Activation
from keras.optimizers import Adam

from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

class RLAgent:
    def __init__(self, game, env):
        self.game = game
        self.env = env
        self.build_model()
        self.build_agent()

    def build_model(self):
        model = Sequential()
        #model.add(Conv2D(128, (4, 4), input_shape=(1, self.game.height, self.game.width, 1), activation='relu'))

        model.add(Flatten(input_shape=(1, self.game.height, self.game.width)))
        model.add(Dense(self.game.height * self.game.width, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(16, activation='relu'))
        model.add(Dense(self.env.action_space.n, activation='linear'))

        self.model = model

    def build_agent(self):
        policy = BoltzmannQPolicy()
        memory = SequentialMemory(limit=50000, window_length=1)
        self.dqn = DQNAgent(model=self.model, memory=memory, policy=policy,
                            nb_actions=self.env.action_space.n, nb_steps_warmup=10, target_model_update=1e-2)

    def train(self):
        self.dqn.compile(Adam(lr=1e-3), metrics=['mae'])
        self.dqn.fit(self.env, nb_steps=10000, visualize=True, verbose=1)

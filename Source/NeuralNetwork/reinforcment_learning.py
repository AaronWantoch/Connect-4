import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, Activation
from keras.optimizers import Adam
from keras.models import model_from_json

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
        model.add(Conv2D(128, (4, 4), input_shape=(1, self.game.height, self.game.width, 1), activation='relu'))

        model.add(Flatten())
        model.add(Dense(64, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(self.env.action_space.n, activation='linear'))

        self.model = model

    def build_agent(self):
        policy = BoltzmannQPolicy()
        memory = SequentialMemory(limit=50000, window_length=1)
        self.dqn = DQNAgent(model=self.model, memory=memory, policy=policy,
                            nb_actions=self.env.action_space.n, nb_steps_warmup=10, target_model_update=1e-2)

    def train(self, steps):
        self.dqn.compile(Adam(lr=1e-3), metrics=['mae'])
        self.dqn.fit(self.env, nb_steps=steps, visualize=True, verbose=1)

    def save_model(self):
        # serialize model to JSON
        model_json = self.model.to_json()
        with open("NeuralNetwork/model.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        self.dqn.save_weights("NeuralNetwork/model.h5", overwrite=True)
        print("Saved model to disk")

    def load_model(self):
        # load json and create model
        json_file = open('NeuralNetwork/model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights("NeuralNetwork/model.h5")
        self.model = loaded_model
        print("Loaded model from disk")

        # evaluate loaded model on test data
        self.build_agent()
        self.dqn.compile(Adam(lr=1e-3), metrics=['mae'])

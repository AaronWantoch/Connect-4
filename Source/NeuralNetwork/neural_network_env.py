import gym
import numpy as np
from gym import Env, spaces
from connect4 import Connect4
from minmax_agent import MinMaxAgent
from dynamic_actions import DynamicActionsSpace
from random_agent import RandomAgent

class Connect4Enviorment(Env):
    ILLEGAL_MOVE_REWARD = -10
    WON_REWARD = 20
    LOST_REWARD = -5
    DRAW_REWARD = 0
    STEP_REWARD = 0

    # TODO: make canvas depend on board
    def __init__(self, connect, token, opponent_agent):
        super(Connect4Enviorment, self).__init__()
        self.game = connect
        self.token = token

        # Define a 2-D observation space
        self.observation_shape = (self.game.height, self.game.width, 1)
        self.observation_space = spaces.Box(low=-1, high=1, shape=self.observation_shape, dtype=np.uint8)

        self.action_space = spaces.Discrete(self.game.width)
        self.canvas = np.zeros(self.observation_shape)

        self.opponent_agent = opponent_agent

        self.total_games = 0
        self.games_won = 0

    def reset(self, **kwargs):
        if self.game.game_over:
            self.total_games += 1
            if self.game.wins == self.token:
                self.games_won += 1
        # return the observation
        self.game = Connect4(self.game.width, self.game.height)
        self.canvas = np.zeros(self.observation_shape)

        return self.canvas

    def render(self, mode="human"):
        if self.game.game_over:
            print()
            win_rate = 0
            if self.total_games != 0:
                win_rate = self.games_won / self.total_games
            print("Win ratio: ", win_rate)
            self.game.draw()

    def step(self, action):
        # TODO: Make it possible to play as second player
        # Make move for nn agent
        for i in range(2):
            if self.game.who_moves == self.token:
                if action not in self.game.possible_drops():
                    return self.canvas, Connect4Enviorment.ILLEGAL_MOVE_REWARD, False, {}

                self.update_canvas(action, 1)
                self.game.drop_token(action)

                # Check if he won
                if self.game.game_over:
                    if self.game.wins == self.token:
                        return self.canvas, Connect4Enviorment.WON_REWARD, True, {}
                    else:
                        return self.canvas, Connect4Enviorment.DRAW_REWARD, True, {}
            else:
                # Make move for opponent
                decision = self.opponent_agent.decide(self.game)
                self.update_canvas(decision, -1)
                self.game.drop_token(decision)
                # Check if agent lost
                if self.game.game_over:
                    if self.game.wins is not None:
                        return self.canvas, Connect4Enviorment.LOST_REWARD, True, {}
                    else:
                        return self.canvas, Connect4Enviorment.DRAW_REWARD, True, {}

        return self.canvas, Connect4Enviorment.STEP_REWARD, False, {}

    def update_canvas(self, action, value):
        row = self.game.get_row(action)
        self.canvas[row][action] = value

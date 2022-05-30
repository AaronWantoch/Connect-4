from exceptions import AgentException
from Genetic.min_max_custom import MinMaxCustom


class MinMaxCustomAgent:
    def __init__(self, my_token='o', column_multiplier=3, my_3=5, enemy_3=-4, my_2=2, enemy_2=-1,enemy_unguarded2=-5):
        self.my_token = my_token
        self.column_multiplier = column_multiplier
        self.my_3 = my_3
        self.enemy_3 = enemy_3
        self.my_2 = my_2
        self.enemy_2 = enemy_2
        self.enemy_unguarded2=enemy_unguarded2

        self.wins = 0
        self.loses = 0
        self.games_played = 0

    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')
        else:
            minmax = MinMaxCustom(self, connect4, self.my_token)

            move = minmax.choose_best_move()

            return move

    # to_string override
    def __str__(self):
        string = "\nMinMaxCustomAgent:"
        string += "\ncolumn_multiplier = "
        string += str(self.column_multiplier)
        string += "\nmy_3 = "
        string += str(self.my_3)
        string += "\nenemy_3 = "
        string += str(self.enemy_3)
        string += "\nmy_2 = "
        string += str(self.my_2)
        string += "\nenemy_2 = "
        string += str(self.enemy_2)
        string += "\nenemy_unguarded2 = "
        string += str(self.enemy_unguarded2)
        string += "\nwins = "
        string += str(self.wins)
        string += "\nloses = "
        string += str(self.loses)
        return string

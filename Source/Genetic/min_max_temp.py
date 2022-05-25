import sys
import copy


class MinMaxCustom:
    def __init__(self,agent, connect, token, depth=2, maximalization=True, alpha=-sys.maxsize - 1, beta=sys.maxsize):
        self.agent = agent
        self.game = connect
        self.token = token
        self.depth = depth
        self.maximalization = maximalization
        self.alpha = alpha
        self.beta = beta

    # calculates score for each move with given multipliers
    def calculate_move_score(self):
        score = 0

        # score for middle column
        mid_column = self.game.center_column()
        amount = mid_column.count(self.token)

        score += self.agent.column_multiplier * amount

        # check 2s and 3s
        enemy = ''
        if self.token == 'x':
            enemy = 'o'
        else:
            enemy = 'x'

        # if there is no possible moves
        if not self.game.possible_drops():
            return score

        # iterate iver all fours in game
        for four in self.game.iter_fours():
            # check threes
            if four.count(self.token) == 3 and four.count('_') >= 1:
                score += self.agent.my_3
            elif four.count(enemy) == 3 and four.count('_') >= 1:
                score -= self.agent.enemy_3
            # check twos
            elif four.count(self.token) == 2 and four.count('_') >= 1:
                score += self.agent.my_2
            elif four.count(enemy) == 2 and four.count('_') >= 1:
                score -= self.agent.enemy_2

        return score

    def choose_move(self):

        if self.game.check_game_over():
            if self.game.wins == self.token:
                return 1000, None
            elif self.game.wins != self.token:
                return -1000, None
            else:
                return 0, None

        if self.depth == 0:
            # return 0,None
            return self.calculate_move_score(), None

        if self.maximalization:
            best_score = -sys.maxsize - 1
            best_move = None

            for move in self.game.possible_drops():
                temp_game = copy.deepcopy(self.game)
                temp_game.drop_token(move)

                temp_minmax = MinMaxCustom(self.agent, temp_game, self.token, self.depth - 1, False, self.alpha,
                                           self.beta)

                score, _ = temp_minmax.choose_move()

                if score > best_score:
                    best_score = score
                    best_move = move

                self.alpha = max(self.alpha, score)
                if self.beta <= self.alpha:
                    break
            return best_score, best_move
        else:
            min_score = sys.maxsize

            for move in self.game.possible_drops():
                temp_game = copy.deepcopy(self.game)
                temp_game.drop_token(move)

                temp_minmax = MinMaxCustom(self.agent, temp_game, self.token, self.depth - 1, True, self.alpha, self.beta)

                score, _ = temp_minmax.choose_move()

                if score < min_score:
                    min_score = score
                    best_move = move

                self.beta = min(self.beta, score)
                if self.beta <= self.alpha:
                    break
            return min_score, best_move

    def choose_best_move(self):
        score, move = self.choose_move()
        return move

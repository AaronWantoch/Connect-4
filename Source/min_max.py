import sys
import copy


class MinMax:
    def __init__(self, connect, token, depth=2, maximalization=True, alpha=-sys.maxsize - 1, beta=sys.maxsize):
        self.game = connect
        self.token = token
        self.depth = depth
        self.maximalization = maximalization
        self.alpha = alpha
        self.beta = beta

    def calculate_move_score(self):
        score = 0
        mid_column = self.game.center_column()
        amount = mid_column.count(self.token)

        score += 3 * amount

        score += self.check_three_and_two()

        return score

    def check_three_and_two(self):
        score = 0
        enemy = ''
        if self.token == 'x':
            enemy = 'o'
        else:
            enemy = 'x'

        if not self.game.possible_drops():
            return 0

        for three in self.game.iter_fours():
            if three.count(self.token) == 3 and three.count('_') >= 1:
                score += 5
            elif three.count(enemy) == 3 and three.count('_') >= 1:
                score -= 4

        for two in self.game.iter_fours():
            if two.count(self.token) == 2 and two.count('_') >= 1:
                score += 2
            elif two.count(enemy) == 2 and two.count('_') >= 1:
                score -= 1

        return score

    def choose_move(self):

        if self.game.check_game_over():
            if self.game.wins == self.token:
                return 100, None
            elif self.game.wins != self.token:
                return -100, None
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

                temp_minmax = MinMax(temp_game, self.token, self.depth - 1, False, self.alpha, self.beta)

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

                temp_minmax = MinMax(temp_game, self.token, self.depth - 1, True, self.alpha, self.beta)

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


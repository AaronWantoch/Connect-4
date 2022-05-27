import random


# simulate okayed games to save time during developing
def simulate_played_games(population):
    for i in range(len(population)):
        population[i].games_played = len(population)-1
        wins = random.randint(0, 49)
        loses = random.randint(0, 49 - wins)
        population[i].wins = wins
        population[i].loses = loses


# custom fitness function
def calculate_fitness(agent):
    fit = agent.wins - (agent.loses/2)
    return fit


# sets tokens for 2 playing agents
def set_tokens(agent1, agent2):
    guess = ['x', 'o']
    choice = random.choice(guess)
    agent1.my_token = choice
    guess.remove(choice)
    agent2.my_token = guess[0]

# checks if s is subset of l
def is_slice_in_list(s,l):
    len_s = len(s) #so we don't recompute length of s on every iteration
    return any(s == l[i:len_s+i] for i in range(len(l) - len_s+1))




    # if four.count(self.token) == 3 and four.count('_') == 1:
    #     score += self.agent.my_3
    # elif four.count(self.token) == 2 and four.count('_') >= 1:
    #     score += self.agent.my_2
    #
    # # check for enemy's threes and twos
    # if four.count(enemy) == 3 and four.count('_') == 1:
    #     score += self.agent.enemy_3
    # elif four.count(enemy) == 2 and four.count('_') >= 1:
    #     score += self.agent.enemy_2

    # # check for unblocked twos
    # if four == ['_', self.token, self.token, '_']:
    #     score += 300
    # elif four == ['_', enemy, enemy, '_']:
    #     score -= 300


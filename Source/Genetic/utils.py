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


from Source.Genetic.minmax_agent_custom import MinMaxCustomAgent
from Source.Genetic.utils import *
from Source.connect4 import Connect4
from Source.exceptions import GameplayException


class GeneticTraining:
    def __init__(self, population_size=100, elite_size=10, mutation_rate=0.01):
        self.population_size = population_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate

    def initial_population(self):
        population = []
        # Create initial population
        for i in range(self.population_size):
            # randomize starting values
            mid_column_multiplier = random.randint(-10, 10)
            my_3 = random.randint(-30, 30)
            enemy_3 = random.randint(-30, 30)
            my_2 = random.randint(-30, 30)
            enemy_2 = random.randint(-30, 30)

            # create agent with randomized values
            agent = MinMaxCustomAgent('', mid_column_multiplier, my_3, enemy_3, my_2, enemy_2)
            # add him to population list
            population.append(agent)

        return population

    # play games in population
    def play_games(self, population):

        game_count = 0
        # each agent plays with all other
        for i in range(self.population_size):
            for j in range(i, self.population_size):
                # if not the same agent
                if i != j:
                    agent1 = population[i]
                    agent2 = population[j]
                    set_tokens(agent1, agent2)

                    print("Match against ", i, "and", j)

                    connect4 = Connect4()
                    # play the game
                    while not connect4.game_over:
                        try:
                            if connect4.who_moves == agent1.my_token:
                                n_column = agent1.decide(connect4)
                            else:
                                n_column = agent2.decide(connect4)
                            connect4.drop_token(n_column)
                        except (ValueError, GameplayException):
                            print('invalid move')
                    agent1.games_played += 1
                    agent2.games_played += 1

                    if agent1.my_token == connect4.wins:
                        agent1.wins += 1
                        agent2.loses += 1
                    elif agent2.my_token == connect4.wins:
                        agent2.wins += 1
                        agent1.loses += 1
            game_count += 1

    # calculates population fitness and returns dictionary
    def population_fitness(self, population):
        population_fitness = {}
        for i, individual in enumerate(population):
            population_fitness[i] = calculate_fitness(individual)

        return {k: v for k, v in sorted(population_fitness.items(), key=lambda item: item[1], reverse=True)}

    # returns agent with best fitness
    def best_solution(self, population):
        population_fitness = list(self.population_fitness(population))
        best_ind = population_fitness[0]
        return population[best_ind]

    def selection(self, population):
        selection = []
        population_fitness = self.population_fitness(population)

        probability = {}

        sum_fitness = sum(population_fitness.values())
        probab_prev = 0.0

        # fitting
        for key, value in sorted(population_fitness.items()):
            probability[key] = probab_prev + value / sum_fitness
            probab_prev = probability[key]

        # elites
        elites = 0
        for key in population_fitness.keys():
            if elites < self.elite_size:
                # pass selection and zero wins and loses
                population[key].wins = 0
                population[key].loses = 0
                selection.append(population[key])
                elites += 1
            else:
                break

        # rest of population
        for i in range(self.elite_size, self.population_size):
            rand = random.random()
            for key, value in probability.items():
                if rand <= value:
                    # pass selection and zero wins and loses
                    population[key].wins = 0
                    population[key].loses = 0
                    selection.append(population[key])

        return selection

    def crossover_population(self, population):
        after_crossover = []

        # skip elites
        for i in range(self.elite_size):
            after_crossover.append(population[i])

        # cross rest of population
        for i in range(self.elite_size, self.population_size):
            first_key = random.choice(population)
            second_key = random.choice(population)

            column_multiplier = round((first_key.column_multiplier + second_key.column_multiplier) / 2,1)
            my_3 = round((first_key.my_3 + second_key.my_3) / 2,1)
            enemy_3 = round((first_key.enemy_3 + second_key.enemy_3) / 2,1)

            my_2 = round((first_key.my_2 + second_key.my_2) / 2,1)
            enemy_2 = round((first_key.enemy_2 + second_key.enemy_2) / 2,1)

            # child has average of his parents values
            child = MinMaxCustomAgent('', column_multiplier, my_3, enemy_3, my_2, enemy_2)

            after_crossover.append(child)

        return after_crossover

    def mutate_population(self, population):

        # for all population
        for i in range(len(population)):
            guess = random.random()

            # if mutation happens
            if guess <= self.mutation_rate:
                # get random to mutate
                mutated = random.choice(population)

                available_mutations = [mutated.column_multiplier, mutated.my_3, mutated.enemy_3, mutated.my_2,
                                       mutated.enemy_2]

                mutated_times = random.randint(0, len(available_mutations))

                for j in range(mutated_times):
                    mutation_multiplier = random.uniform(0.80, 1.20)
                    mutated_index = random.randint(0, len(available_mutations) - 1)
                    available_mutations[mutated_index] = round(available_mutations[mutated_index]*mutation_multiplier,1)
        return population

    def next_generation(self, population):
        selection = self.selection(population)
        children = self.crossover_population(selection)
        next_generation = self.mutate_population(children)
        return next_generation

from Source.Genetic.utils import simulate_played_games
from genetic_training import GeneticTraining


def start_genetic_learning(generations=10, population_size=50, elite_size=5, mutation_rate=0.1):
    genetic = GeneticTraining(population_size=population_size, elite_size=elite_size, mutation_rate=mutation_rate)

    population = genetic.initial_population()
    #simulate_played_games(population)
    genetic.play_games(population)
    best_solution = genetic.best_solution(population)
    file.write("\nBest after initial population:")
    file.write(str(best_solution))
    file.write("\n\n")

    for i in range(1, generations):
        print("Generation number:", i)
        population = genetic.next_generation(population)
        #simulate_played_games(population)
        genetic.play_games(population)
        best_solution = genetic.best_solution(population)
        file.write("\nBest after " + str(i) + " generation:")
        file.write(str(best_solution))
        file.write("\n\n")
    file.write("----Finished genetic algorithm----\n")
    return best_solution


if __name__ == '__main__':
    file = open("genetic_history.txt", "w")
    print()
    print("Starting genetic algorithm")
    file.write("----Starting genetic algorithm----\n")

    best_solution = start_genetic_learning()
    print()
    print("Best agent:", best_solution)

    file.write("\nBest agent:")
    file.write(str(best_solution))

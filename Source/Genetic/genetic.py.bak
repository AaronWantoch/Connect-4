import numpy as np
import random
from utils import fitness


class Genetic:
    def __init__(self, coords, population_size=100, elite_size=10, mutation_rate=0.01):
        self.coords = coords
        self.population_size = population_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate

    def population_fitness(self, population):
        population_fitness = {}
        for i, individual in enumerate(population):
            # 1/fitness -> change to maximization problem
            population_fitness[i] = 1/fitness(self.coords, individual)

        return {k: v for k, v in sorted(population_fitness.items(), key=lambda item: item[1], reverse=True)}

    def best_solution(self, population):
        population_fitness = list(self.population_fitness(population))
        best_ind = population_fitness[0]
        return population[best_ind]

    def initial_population(self):
        population = []
        # Create initial population
        for i in range(self.population_size):
            solution = np.random.permutation(len(self.coords))
            population.append(solution)
        return population


    def selection(self, population):
        selection=[]
 
        population_fitnes=self.population_fitness(population)
        fitnes_list=list(self.population_fitness(population))

        propability={}

        sum_fitness=sum(population_fitnes.values())
        propab_prev=0.0

        for i in range(self.elite_size):
            index=fitnes_list[i]
            selection.append(population[index])


        for key in population_fitnes:
            propability[key]=propab_prev+(population_fitnes[key]/sum_fitness)
            propab_prev=propability[key]

        for i in range(self.elite_size,len(population)):
            rand=random.random()
            for key,value in propability.items():
                if rand<=value:
                    selection.append(population[key])
                    break

        return selection


    def crossover_population(self, population):

        after_crossover=[]

        # TODO: elityzm top 10 

        for i in range(self.elite_size,self.population_size):
            first_key=random.choice(population)
            second_key=random.choice(population)

            #generate indexes
            seq_len=random.randint(0,len(first_key)-1)
            seq_start_index=random.randint(0,len(first_key)-seq_len)
            seq_end_index=seq_start_index+seq_len-1

            #slice
            slice_obj=slice(seq_start_index,seq_end_index+1)
            slice_array=first_key[slice_obj]

            #offspring
            offspring=[]*len(second_key)
            offspring=[x for x in second_key if x not in slice_array]


            #save last values of second_key
            last_values=[]
            for i in range(seq_end_index+1,len(second_key)-1):
                last_values.append(offspring.pop())

            last_values.reverse()
                

            #add slice to offspring
            offspring.extend(slice_array)

            #add last_values to offspring
            offspring.extend(last_values)

            after_crossover.append(offspring)

        return after_crossover

    def mutate_population(self, population):

        #for all population
        for i in range(len(population)):
            guess=random.random()

            #if mutation happens
            if(guess<=self.mutation_rate):
                #get random to mutate
                mutated_index=random.randint(0,len(population)-1)
                mutated=population[mutated_index]

                #get 2 random gene indekses
                index1=random.randint(0,len(mutated)-1)
                index2=random.randint(0,len(mutated)-1)

                #swap them
                temp=mutated[index1]
                mutated[index1]=mutated[index2]
                mutated[index2]=temp

                #add mutated to population
                population[mutated_index]=mutated

        return population

    def next_generation(self, population):
        selection = self.selection(population)
        children = self.crossover_population(selection)
        next_generation = self.mutate_population(children)
        return next_generation

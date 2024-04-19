import random
class GeneticAlgorithm:
    def __init__(self, population_size, chromosome_length, crossover_rate, mutation_rate, items, knapsack_capacity, tournament_size):
        self.population_size = population_size
        self.chromosome_length = chromosome_length
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.items = items
        self.knapsack_capacity = knapsack_capacity
        self.population = self.initialize_population()
        self.tournament_size = tournament_size

    # create the initial population of solutions (all random)
    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            chromosome = [random.randint(0,1) for _ in range(self.chromosome_length)]
            population.append(chromosome)
        return population

    # evaluates the fitness of a solution (chromosome)
    def fitness(self, chromosome):
        weight = 0
        value = 0
        for i in range(self.chromosome_length):
            if chromosome[i] == 1:
                weight += self.items[i][0] #note this should correspond to weight of knapsack item
                value += self.items[i][1] #value of the item
        if weight > self.knapsack_capacity: #check if the total weight is above what we allow
            return 0
        else:
            return value

    # do tournament selection
    # current selected will be equal to the population size
    # notes: change tournament size to have more chromosomes compete against each other. definitely want this less than
    # 1/2 of the population size. lamda function here basically uses our fitness function as a key
    # chromosome is an arbitrary variable
    def selection(self):
        selected = []
        while len(selected) < self.population_size:
            tournament_contestants = random.sample(self.population, self.tournament_size)
            winner = max(tournament_contestants, key=lambda chromosome: self.fitness(chromosome))
            selected.append(winner)
        return selected;

    # uniform crossover
    # crossover rate is how often chromosomes will crossover (do 0.5)
    def crossover(self, parent1, parent2):
        child1 = []
        child2 = []
        for i in range(self.chromosome_length):
            if random.random() < self.crossover_rate:
                child1.append(parent1[i])
                child2.append(parent2[i])
            else:
                child1.append(parent2[i])
                child2.append(parent1[i])
        return child1, child2

    #bitflip mutation
    def mutation(self, chromosome):
        for i in range(self.chromosome_length):
            if random.random() < self.mutation_rate:
                chromosome[i] = 1 - chromosome[i]
        return chromosome

    def evolve(self):
        selected_parents = self.selection()
        new_population = []
        while len(new_population) < self.population_size:
            parent1, parent2 = random.choices(selected_parents, k=2)
            if random.random() < self.crossover_rate:
                child1, child2 = self.crossover(parent1, parent2)
            else:
                child1, child2 = parent1[:], parent2[:] #copy
            child1 = self.mutation(child1)
            child2 = self.mutation(child2)
            new_population.extend([child1, child2])
        self.population = new_population



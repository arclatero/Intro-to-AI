import numpy as np
import random
import math

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

class GeneticAlgorithm:
    def __init__(self, 
                 population_size=100,
                 generations=100,
                 mutation_rate=0.05,
                 crossover_rate=0.8,
                 elitism_count=2,
                 tournament_size=5):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_count = elitism_count
        self.tournament_size = tournament_size
        
        self.population = []
        self.best_individual = None
        self.best_fitness = float('-inf')
        self.fitness_history = []
        self.avg_fitness_history = []
    
    def initialize_population(self, gene_factory, bounds):
        self.population = []
        self.bounds = bounds
        
        for _ in range(self.population_size):
            individual = [gene_factory(bounds[i]) for i in range(len(bounds))]
            self.population.append(individual)
    
    def evaluate_fitness(self, fitness_function):
        fitness_scores = []
        
        for individual in self.population:
            fitness = fitness_function(individual)
            fitness_scores.append(fitness)
            
            if fitness > self.best_fitness:
                self.best_fitness = fitness
                self.best_individual = individual.copy()
        
        self.population = [x for _, x in sorted(zip(fitness_scores, self.population), 
                                                  key=lambda pair: pair[0], reverse=True)]
        fitness_scores.sort(reverse=True)
        
        self.fitness_history.append(fitness_scores[0])
        self.avg_fitness_history.append(np.mean(fitness_scores))
        
        return fitness_scores
    
    def tournament_selection(self, fitness_scores):
        tournament_indices = random.sample(range(len(self.population)), 
                                          self.tournament_size)
        tournament_fitness = [fitness_scores[i] for i in tournament_indices]
        
        best_idx = tournament_indices[tournament_fitness.index(max(tournament_fitness))]
        return self.population[best_idx].copy()
    
    def single_point_crossover(self, parent1, parent2):
        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()
        
        point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        
        return child1, child2
    
    def uniform_crossover(self, parent1, parent2):
        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()
        
        child1, child2 = [], []
        for i in range(len(parent1)):
            if random.random() < 0.5:
                child1.append(parent1[i])
                child2.append(parent2[i])
            else:
                child1.append(parent2[i])
                child2.append(parent1[i])
        
        return child1, child2
    
    def gaussian_mutation(self, individual, bounds):
        mutated = individual.copy()
        
        for i in range(len(mutated)):
            if random.random() < self.mutation_rate:
                sigma = (bounds[i][1] - bounds[i][0]) * 0.1
                mutated[i] += random.gauss(0, sigma)
                mutated[i] = max(bounds[i][0], min(bounds[i][1], mutated[i]))
        
        return mutated
    
    def random_reset_mutation(self, individual, bounds):
        mutated = individual.copy()
        
        for i in range(len(mutated)):
            if random.random() < self.mutation_rate:
                mutated[i] = random.uniform(bounds[i][0], bounds[i][1])
        
        return mutated
    
    def evolve(self, fitness_function, gene_factory, bounds, 
               mutation_type='gaussian', crossover_type='single'):
        self.initialize_population(gene_factory, bounds)
        
        print(f"\nStarting Evolution:")
        print(f"  Population Size: {self.population_size}")
        print(f"  Generations: {self.generations}")
        print(f"  Mutation Rate: {self.mutation_rate}")
        print(f"  Crossover Rate: {self.crossover_rate}")
        
        for gen in range(self.generations):
            fitness_scores = self.evaluate_fitness(fitness_function)
            
            if gen % 10 == 0 or gen == self.generations - 1:
                print(f"  Generation {gen}: Best Fitness = {fitness_scores[0]:.6f}, "
                      f"Avg = {np.mean(fitness_scores):.6f}")
            
            new_population = []
            
            for i in range(self.elitism_count):
                new_population.append(self.population[i].copy())
            
            while len(new_population) < self.population_size:
                parent1 = self.tournament_selection(fitness_scores)
                parent2 = self.tournament_selection(fitness_scores)
                
                if crossover_type == 'single':
                    child1, child2 = self.single_point_crossover(parent1, parent2)
                else:
                    child1, child2 = self.uniform_crossover(parent1, parent2)
                
                if mutation_type == 'gaussian':
                    child1 = self.gaussian_mutation(child1, bounds)
                    child2 = self.gaussian_mutation(child2, bounds)
                else:
                    child1 = self.random_reset_mutation(child1, bounds)
                    child2 = self.random_reset_mutation(child2, bounds)
                
                new_population.append(child1)
                if len(new_population) < self.population_size:
                    new_population.append(child2)
            
            self.population = new_population
        
        return self.best_individual, self.best_fitness
    
    def get_statistics(self):
        return {
            'best_fitness': self.fitness_history,
            'avg_fitness': self.avg_fitness_history,
            'best_individual': self.best_individual
        }


# Example 1: Sphere Function Optimization
print("\n" + "="*50)
print("EXAMPLE 1: Function Optimization")
print("="*50)

def sphere_function(x):
    return -sum(xi**2 for xi in x)

bounds = [(-10, 10), (-10, 10), (-10, 10), (-10, 10)]

def gene_factory(bound):
    return random.uniform(bound[0], bound[1])

ga1 = GeneticAlgorithm(
    population_size=100,
    generations=50,
    mutation_rate=0.1,
    crossover_rate=0.8,
    elitism_count=2
)

best_solution, best_fitness = ga1.evolve(
    fitness_function=lambda x: sphere_function(x),
    gene_factory=gene_factory,
    bounds=bounds,
    mutation_type='gaussian',
    crossover_type='single'
)

print(f"\nResult:")
print(f"  Best Solution: {[f'{v:.4f}' for v in best_solution]}")
print(f"  Best Fitness: {-best_fitness:.6f}")
print(f"  Theoretical Maximum: 0.0")


# Example 2: Traveling Salesman Problem
print("\n" + "="*50)
print("EXAMPLE 2: Traveling Salesman Problem")
print("="*50)

cities = {
    'A': (0, 0), 'B': (1, 3), 'C': (2, 1), 'D': (3, 4),
    'E': (4, 2), 'F': (5, 5), 'G': (6, 1), 'H': (7, 3),
    'I': (8, 0), 'J': (9, 4)
}
cities_list = list(cities.values())

def calculate_distance(city1, city2):
    return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)

def calculate_total_distance(tour):
    total = 0
    for i in range(len(tour) - 1):
        total += calculate_distance(cities_list[tour[i]], cities_list[tour[i+1]])
    total += calculate_distance(cities_list[tour[-1]], cities_list[tour[0]])
    return total

def tsp_fitness_function(tour):
    return -calculate_total_distance(tour)

class TSGeneticAlgorithm:
    def __init__(self, population_size=200, generations=100, mutation_rate=0.15):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.best_tour = None
        self.best_fitness = float('-inf')
        self.fitness_history = []
    
    def initialize_population(self, n_cities):
        self.population = []
        for _ in range(self.population_size):
            tour = list(range(n_cities))
            random.shuffle(tour)
            self.population.append(tour)
    
    def evaluate_fitness(self):
        fitness_scores = []
        for tour in self.population:
            fitness = tsp_fitness_function(tour)
            fitness_scores.append(fitness)
            
            if fitness > self.best_fitness:
                self.best_fitness = fitness
                self.best_tour = tour.copy()
        
        self.population = [x for _, x in sorted(zip(fitness_scores, self.population), 
                                                  key=lambda pair: pair[0], reverse=True)]
        fitness_scores.sort(reverse=True)
        
        self.fitness_history.append(-fitness_scores[0])
        return fitness_scores
    
    def order_crossover(self, parent1, parent2):
        size = len(parent1)
        start, end = sorted(random.sample(range(size), 2))
        
        child1 = [None] * size
        child2 = [None] * size
        
        child1[start:end+1] = parent1[start:end+1]
        child2[start:end+1] = parent2[start:end+1]
        
        def fill_child(child, parent):
            current_pos = (end + 1) % size
            for gene in parent:
                if gene not in child:
                    while child[current_pos % size] is not None:
                        current_pos += 1
                    child[current_pos % size] = gene
            return child
        
        child1 = fill_child(child1, parent2)
        child2 = fill_child(child2, parent1)
        
        return child1, child2
    
    def swap_mutation(self, tour):
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(len(tour)), 2)
            tour[i], tour[j] = tour[j], tour[i]
        return tour
    
    def evolve(self, n_cities):
        self.initialize_population(n_cities)
        
        print(f"\nTSP Evolution:")
        print(f"  Cities: {n_cities}")
        print(f"  Population: {self.population_size}")
        print(f"  Generations: {self.generations}")
        
        for gen in range(self.generations):
            fitness_scores = self.evaluate_fitness()
            
            if gen % 20 == 0 or gen == self.generations - 1:
                print(f"  Generation {gen}: Best Distance = {self.fitness_history[-1]:.2f}")
            
            new_population = self.population[:5]
            
            while len(new_population) < self.population_size:
                candidates = random.sample(self.population[:50], 3)
                parent1 = max(candidates, key=lambda t: tsp_fitness_function(t))
                
                candidates = random.sample(self.population[:50], 3)
                parent2 = max(candidates, key=lambda t: tsp_fitness_function(t))
                
                child1, child2 = self.order_crossover(parent1, parent2)
                
                child1 = self.swap_mutation(child1)
                child2 = self.swap_mutation(child2)
                
                new_population.extend([child1, child2])
            
            self.population = new_population[:self.population_size]
        
        return self.best_tour, self.best_fitness

tsp_ga = TSGeneticAlgorithm(population_size=200, generations=100, mutation_rate=0.15)
best_tour, best_fitness = tsp_ga.evolve(len(cities_list))

print(f"\nTSP Result:")
print(f"  Best Tour: {best_tour}")
print(f"  Best Distance: {-best_fitness:.2f}")

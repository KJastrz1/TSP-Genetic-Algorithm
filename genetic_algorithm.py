import random
from individual import Individual


class GeneticAlgorithm:
    def __init__(
        self,
        graph,   
        num_nodes=10,
        start_node=0,         
        mutation_rate=0.01,
        crossover_rate=0.9,        
        tournament_size=5,
        num_generations=100,
        population_size=100,
        population=None,
    ):
        
        self.num_nodes = num_nodes
        self.start_node = start_node
        self.graph = graph
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.num_generations = num_generations
        self.tournament_size = tournament_size
        self.population_size = population_size
        if population:
            self.population = population
        else:
            self.population = self.initialize_population()
        self.check_if_none()

    def initialize_population(self):
        return [
            Individual.random(self.num_nodes, self.graph, self.start_node)
            for _ in range(self.population_size)
        ]
        
    def check_if_none(self):
        for ind in self.population:
            if len(ind.route)!=self.num_nodes-1:
                 print("individual has no full route", ind.route)                
            for i in range(len(ind.route)):
                if ind.route[i] is None:
                    print("individual with none edge:", ind.route)
                
        

    def evolve_population(self):
        new_population = []
        for _ in range(self.population_size):

            parent1 = self.tournament_selection()
            parent2 = self.tournament_selection()

            if random.random() < self.crossover_rate:
                child = parent1.crossover(parent2)
            else:
                child = parent1 if parent1.cost < parent2.cost else parent2

            child.mutate(self.mutation_rate)
            child.calculate_cost()
            new_population.append(child)

        self.population = new_population

    def tournament_selection(self):
        if len(self.population) < self.tournament_size:
            tournament = self.population 
        else:
            tournament = random.sample(self.population, self.tournament_size)
        best_individual = min(tournament, key=lambda individual: individual.cost)
        return best_individual

    def selection_whole_population(self):
        new_population = []
        for _ in range(self.population_size):
            new_individual = self.tournament_selection()
            new_population.append(new_individual)
        self.population = new_population

    def run(self):
        for generation in range(self.num_generations):
            self.evolve_population()
            best_cost = min(ind.cost for ind in self.population)
            # print(f"Generation {generation+1}: Best Cost = {best_cost}")

        return min(self.population, key=lambda ind: ind.cost)

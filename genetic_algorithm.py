import random
from individual import Individual


class GeneticAlgorithm:
    def __init__(
        self,
        num_nodes,
        start_node,
        graph,
        population_size=100,
        mutation_rate=0.01,
        crossover_rate=0.9,
        num_generations=100,
        tournament_size=5,
    ):
        self.population_size = population_size
        self.num_nodes = num_nodes
        self.start_node=start_node
        self.graph = graph
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.num_generations = num_generations
        self.tournament_size = tournament_size
        self.population = self.initialize_population()

    def initialize_population(self):
        return [
            Individual.random(self.num_nodes, self.graph, self.start_node)
            for _ in range(self.population_size)
        ]

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
        tournament = random.sample(self.population, self.tournament_size)
        best_individual = min(tournament, key=lambda individual: individual.cost)
        return best_individual

    def run(self):
        for generation in range(self.num_generations):
            self.evolve_population()
            best_cost = min(ind.cost for ind in self.population)
            print(f"Generation {generation+1}: Best Cost = {best_cost}")

        return min(self.population, key=lambda ind: ind.cost)

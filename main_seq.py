import time

from genetic_algorithm import GeneticAlgorithm
from graph import load_graph_from_file


if __name__ == "__main__":
    start_time = time.time()
    num_nodes = 30
    start_node = 0
    population_size = 3000
    num_generations = 100
    mutation_rate = 0.01
    crossover_rate = 0.9
    tournament_size = 5

    graph = load_graph_from_file("graph.pkl")

    genetic_algorithm = GeneticAlgorithm(
        num_nodes=num_nodes,
        start_node=start_node,
        graph=graph,
        mutation_rate=mutation_rate,
        crossover_rate=crossover_rate,
        tournament_size=tournament_size,
        num_generations=num_generations,
        population_size=population_size,
    )

    best_individual = genetic_algorithm.run()
    print(
        f"Best route starting from node {start_node}: {[start_node] + best_individual.route + [start_node]}"
    )
    print(f"Cost of the best route: {best_individual.cost}")

    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")

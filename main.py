from mpi4py import MPI
import time

from genetic_algorithm import GeneticAlgorithm
from graph import load_graph_from_file


def calculate_tour_cost(graph, tour):
    length = 0
    for i in range(len(tour) - 1):
        length += graph.edges[tour[i], tour[i + 1]]["weight"]
    return length


if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    num_nodes = 30
    start_node = 0
    population_size = 3000
    num_generations = 100
    mutation_rate = 0.01
    crossover_rate = 0.9
    tournament_size = 5

    graph = load_graph_from_file("graph.pkl")

    if rank == 0:
        start_time = time.time()

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

        pop_per_process = population_size // (size - 1)

        for generation in range(num_generations):
            for i in range(1, size):
                comm.send(
                    genetic_algorithm.population[
                        (i - 1) * pop_per_process : i * pop_per_process
                    ],
                    dest=i,
                    tag=11,
                )

            new_population = []
            for i in range(1, size):
                new_population.extend(comm.recv(source=i, tag=12))

            genetic_algorithm.population = new_population
            if generation % 5 == 0:
                genetic_algorithm.selection_whole_population()

        best_route = min(genetic_algorithm.population, key=lambda ind: ind.cost)
        print(f"Best route Cost: {best_route.cost}")

        end_time = time.time()
        print(f"Total execution time: {end_time - start_time:.2f} seconds")

    else:
        for _ in range(num_generations):
            population = comm.recv(source=0, tag=11)

            local_genetic_algorithm = GeneticAlgorithm(
                num_nodes=num_nodes,
                start_node=start_node,
                graph=graph,
                mutation_rate=mutation_rate,
                crossover_rate=crossover_rate,
                tournament_size=tournament_size,
                num_generations=num_generations,
                population=population,
            )
            local_genetic_algorithm.evolve_population()
            comm.send(local_genetic_algorithm.population, dest=0, tag=12)

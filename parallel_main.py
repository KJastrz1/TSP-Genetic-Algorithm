from mpi4py import MPI
import time
import random

from genetic_algorithm import GeneticAlgorithm
from graph import load_graph_from_file

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    total_population = 4000
    num_nodes = 30
    start_node = 0
    population_size = total_population // size
    num_generations = 100
    mutation_rate = 0.01
    crossover_rate = 0.9
    tournament_size = 5
    migration_interval = 10
    num_migrants = 50

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

    start_time = time.time()
    requests = []

    for generation in range(num_generations):
        genetic_algorithm.evolve_population()

        if generation % migration_interval == 0 and generation != 0:
            migrants = sorted(genetic_algorithm.population, key=lambda ind: ind.cost)[
                :num_migrants
            ]
            for i in range(size):
                if i != rank:
                    req = comm.isend(migrants, dest=i, tag=13)
                    requests.append(req)

            new_individuals = []
            for i in range(size - 1):
                new_individuals.extend(comm.recv(source=MPI.ANY_SOURCE, tag=13))

            for migrant in new_individuals:
                genetic_algorithm.population[
                    random.randint(0, len(genetic_algorithm.population) - 1)
                ] = migrant

            MPI.Request.Waitall(requests)
            requests.clear()

    local_best = min(genetic_algorithm.population, key=lambda ind: ind.cost)
    local_best_data = (local_best.cost, rank)

    global_best_cost, global_best_rank = comm.allreduce(local_best_data, op=MPI.MINLOC)
    
    if rank == global_best_rank:       
        global_best_route = local_best.route
    else:
        global_best_route = None
 
    global_best_route = comm.bcast(global_best_route, root=global_best_rank)
    
    if rank == 0:
        print(f"Best route Cost: {global_best_cost}")
        end_time = time.time()
        print(f"Total execution time: {end_time - start_time:.2f} seconds")

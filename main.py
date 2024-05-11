import random
import networkx as nx
import matplotlib.pyplot as plt
from genetic_algorithm import GeneticAlgorithm


def generate_complete_graph(num_nodes, weight_range=(1, 100)):
    G = nx.complete_graph(num_nodes)
    for u, v in G.edges():
        G.edges[u, v]["weight"] = random.randint(weight_range[0], weight_range[1])
    return G


def plot_graph_step(graph, tour, current_node, pos):
    plt.clf()
    nx.draw(graph, pos, with_labels=True, node_color="lightblue", node_size=500)
    path_edges = list(zip(tour, tour[1:]))
    nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color="r", width=2)
    nx.draw_networkx_nodes(
        graph, pos, nodelist=[current_node], node_color="g", node_size=500
    )

    edge_labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    plt.pause(0.5)


def calculate_tour_cost(graph, tour):
    length = 0
    for i in range(len(tour) - 1):
        length += graph.edges[tour[i], tour[i + 1]]["weight"]
    return length


if __name__ == "__main__":
    num_nodes = 10
    start_node = 0
    population_size = 100
    num_generations = 100
    mutation_rate = 0.01
    crossover_rate = 0.9
    tournament_size = 5

    graph = generate_complete_graph(num_nodes)
    genetic_algorithm = GeneticAlgorithm(
        num_nodes,
        start_node,
        graph,
        population_size,
        mutation_rate,
        crossover_rate,
        num_generations,
        tournament_size,
    )
    best_individual = genetic_algorithm.run()
    print(
        f"Best route starting from node {start_node}: {[start_node] + best_individual.route + [start_node]}"
    )
    print(f"Cost of the best route: {best_individual.cost}")

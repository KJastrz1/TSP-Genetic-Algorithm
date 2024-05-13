import pickle
import random
import random
import networkx as nx

def save_graph_to_file(graph, file_path):
    with open(file_path, "wb") as file:
        pickle.dump(graph, file)
    print(f"Graph saved to {file_path}")

def load_graph_from_file(file_path):
    with open(file_path, "rb") as file:
        graph = pickle.load(file)
    return graph

def generate_complete_graph(num_nodes, weight_range=(1, 100)):
    graph = nx.complete_graph(num_nodes)
    for u, v in graph.edges():
        graph.edges[u, v]["weight"] = random.randint(weight_range[0], weight_range[1])
    return graph

if __name__ == "__main__":
    graph=generate_complete_graph(30)
    save_graph_to_file(graph,'graph.pkl')
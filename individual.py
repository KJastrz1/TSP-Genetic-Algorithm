import random


class Individual:
    def __init__(self, route, graph, start_node):
        self.route = route
        self.graph = graph
        self.cost = None
        self.start_node = start_node
        self.calculate_cost()

    @classmethod
    def random(cls, num_cities, graph, start_node):
        route = list(range(num_cities))
        route.remove(start_node)
        random.shuffle(route)
        return cls(route, graph,start_node)

    def calculate_cost(self):
        self.cost = self.graph.edges[self.start_node, self.route[0]]["weight"]
        for i in range(len(self.route) - 1):
            self.cost += self.graph.edges[self.route[i], self.route[i + 1]]["weight"]
        self.cost += self.graph.edges[self.route[-1], self.start_node]["weight"]

    def mutate(self, mutation_rate):
        for i in range(len(self.route)):
            if random.random() < mutation_rate:
                j = random.randint(0, len(self.route) - 1)
                self.route[i], self.route[j] = self.route[j], self.route[i]

    def crossover(self, other):       
        start, end = sorted(random.sample(range(len(self.route)), 2))    
        child_route = [None] * len(self.route)   
        child_route[start:end+1] = self.route[start:end+1]
    
        used_cities = set(child_route[start:end+1])
        left_fill = []
        right_fill = []


        for node in other.route:
            if node not in used_cities:
                if len(left_fill) < start:
                    left_fill.append(node)
                elif len(right_fill) < len(self.route) - end - 1:
                    right_fill.append(node)                
                used_cities.add(node)
    
        child_route[:start] = left_fill
        child_route[end+1:] = right_fill

        return Individual(child_route, self.graph, self.start_node)



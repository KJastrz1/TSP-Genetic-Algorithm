# Genetic Algorithm for the Traveling Salesman Problem (TSP)

## Overview
The Traveling Salesman Problem (TSP) is a well-known and extensively studied NP-hard problem in combinatorial optimization. The challenge is to find the shortest possible route that visits a set of cities, with each city visited exactly once, and returns to the origin city. This problem grows exponentially harder as the number of cities increases, highlighting its NP-hard nature.

## Problem Complexity
The complexity of the TSP arises from its combinatorial nature; the number of possible tours (solutions) increases factorially with the number of cities involved (n!), making exhaustive search impractical even for relatively small numbers of cities. This exponential growth of possible solutions renders TSP intractable for traditional optimization methods as the input size increases, prompting the need for heuristic or approximation algorithms capable of finding good enough solutions within reasonable time frames.

## Project Description
This project implements a genetic algorithm (GA) to address the TSP, leveraging parallel processing to enhance the efficiency and effectiveness of the solution process. The GA uses a population-based approach to evolve solutions over generations, employing selection, crossover, and mutation operations to explore the solution space.

### Features
- **Parallel Genetic Algorithm**: Utilizes MPI (Message Passing Interface) for parallel processing, distributing the workload across multiple processors to speed up the computation.
- **Adaptive Mutation and Crossover Rates**: Implements adaptive mechanisms to fine-tune the genetic operators based on runtime performance metrics.
- **Migration Strategy**: Incorporates a migration strategy among parallel sub-populations to maintain genetic diversity and avoid premature convergence.

### Parameters
- total_population = 4000
- num_nodes = 30 
- num_generations = 100
- mutation_rate = 0.01
- crossover_rate = 0.9
- tournament_size = 5
- migration_interval = 10  Determines how often (in terms of generations) individuals are migrated between different MPI processes. 
- num_migrants = 50  Specifies the number of individuals that are migrated at each migration event. 
  
### Installation
1. **Clone or Download repository**
2. **Install MPI Implementation**:
   - For Ubuntu: `sudo apt-get install mpich`
   - For macOS: `brew install mpich`
   - For Windows install [MS MPI](https://www.microsoft.com/en-us/download/details.aspx?id=57467)
3. **Create virtual enviroment**:
   `python -m venv .venv`
4. **Activate virtual enviroment**:
   Unix or macOS:
   `source .venv/bin/activate`
   Windows:
   `.\.venv\Scripts\activate`
5. **Install Python Dependencies**:
   `pip install -r requirements.txt`
6. **Run program**:
   `mpirun -n 4 python parallel_main.py`
   For Windows:
   `mpiexec -n 4 python parallel_main.py`

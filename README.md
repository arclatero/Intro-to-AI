# Intro-to-AI

Clatero, Anecito Jr. R.


#A*
A* (A-Star) Search Algorithm is an informed search algorithm used to find the shortest path between nodes in a graph or grid It uses the evaluation function (f(n) = g(n) + h(n))
Where:
g(n) = cost from the start node to the current node
h(n) = heuristic estimate from the current node to the goal
f(n) = total estimated cost
A* combines actual distance and heuristic estimation to efficiently find optimal paths.

#Example 1 – Robot Navigation
This example simulates a robot moving through a warehouse grid.
<img width="914" height="908" alt="astar1" src="https://github.com/user-attachments/assets/f21a667f-3f7a-4a33-9eba-874d4cbcc7a6" />

#Example 2 – Tree Search
This example demonstrates A* on a graph tree structure. Each edge has a cost, and each node has a heuristic value estimating the distance to the goal.
The algorithm finds the lowest-cost path from A to K.
<img width="909" height="737" alt="astar2" src="https://github.com/user-attachments/assets/c91d9bfd-3307-4583-8a48-c089d08439cd" />


#A-Priori
Apriori Algorithm is a popular data mining algorithm used for Association Rule Learning. It identifies patterns in transaction datasets to discover relationships between items.

#Example 1 – Market Basket Analysis
This example analyzes online shopping transactions.
<img width="1239" height="677" alt="apriori1" src="https://github.com/user-attachments/assets/e0ec3a3f-1b39-4a77-8c5e-1173a92dcb50" />
<img width="771" height="897" alt="apriori-example-a" src="https://github.com/user-attachments/assets/26fcb390-1100-4e7f-8910-c59f9c2ee6f0" />

#Example 2 – Student Course Selection
This example analyzes student course enrollment patterns. The algorithm discovers which courses students frequently take together.
<img width="1312" height="675" alt="apriori2" src="https://github.com/user-attachments/assets/6b10d5bb-d572-4433-ab08-48eee398a769" />
<img width="854" height="880" alt="apriori-example-b" src="https://github.com/user-attachments/assets/e55a93af-7183-4ef5-a2b4-1792e26fa28c" />


#Genetic Algorithm
Genetic Algorithm (GA) is an optimization algorithm inspired by Darwin's theory of natural selection. It evolves solutions through generations using; Population initialization, Fitness evaluation, Selection, Crossover, Mutation, Replacement.
The best individuals survive and improve over time.

#Example 1 – Function Optimization
This example uses GA to optimize a mathematical function.
<img width="720" height="410" alt="genetic-algo-example1" src="https://github.com/user-attachments/assets/abe8f819-ab57-4d69-9dfe-796122fa1d69" />


#Example 2 – Traveling Salesman Problem (TSP)
The Traveling Salesman Problem is a classic optimization problem.
<img width="720" height="383" alt="genetic-algo-example2" src="https://github.com/user-attachments/assets/ffe5c34a-da25-4064-95e3-b9cdc53c6ae3" />

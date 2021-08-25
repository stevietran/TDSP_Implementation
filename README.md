# Cost-Optimal Path with Time Constraint over Time-Dependent Graphs

This is an implementation of the [Paper](https://api.semanticscholar.org/CorpusID:15323505) on finding a cost optimal path over a time-dependent graph.

## Assumption of the library
- We assume fixed travel time of each edge
- We find route with minimum cost and check capacity for every edge in this route to ensure capacity is sufficent to deliver the package
- The departure time of package depends on the capacity functions. Each package only can be delivered at the end interval of each segment.
- The algorithm will find all possible route delivering the package from start node to end node. Among these routes, we consider each option from one which has the minimum cost and where every edge satisfy the capacity defined for each node. 

## Main concepts of the algorithm
Lambda is defined as the time return from shortest path algorithmn where it is the earliest time the package can reach its destination from the start node. The algorithm requires shortest path algorithm to solve this time for all nodes except the defined start node which the time is zero by default. In the module, lamdas is a dictionary containing earliest arrival times from start node to all other node indexed by their node ids.

ATMC-function (arrival time and min cost function) g_i of vertex i represents a minumum cost that one can arrive at vertex i at time t  from the source.

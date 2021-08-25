from algorithms.tdsp import Tdsp
from models.Graph import GraphNode, GraphEdge, Graph
import sys

def main(args):
    # Nodes nodes = [1, 2, 3, 4]
    node1 = GraphNode(1)
    node2 = GraphNode(2)
    node3 = GraphNode(3)
    node4 = GraphNode(4)

    # Edges
    node1 = GraphNode(1)
    node2 = GraphNode(2)
    edge1 = GraphEdge(1, node1, node2)
    node1.addNeighbour(node2)
    node2.addParent(node1)

    edge2 = GraphEdge(2, node1, node3)
    node1.addNeighbour(node3)
    node3.addParent(node1)

    edge3 = GraphEdge(3, node2, node3)
    node2.addNeighbour(node3)
    node3.addParent(node2)

    edge4 = GraphEdge(4, node2, node4)
    node2.addNeighbour(node4)
    node4.addParent(node2)

    edge5 = GraphEdge(5, node3, node4)
    node3.addNeighbour(node4)
    node4.addParent(node3)

    # Set up cost, travel time of each edge
    edge1.setCost([0, 60], [10])
    edge1.setTime([0, 60], [10])

    edge2.setCost([0, 15, 45, 60], [20, 5, 35])
    edge2.setTime([0, 60], [15])

    edge3.setCost([0, 15, 60], [15, 5])
    edge3.setTime([0, 60], [5])

    edge4.setCost([0, 5, 20, 60], [10,20, 15])
    edge4.setTime([0, 60], [20])

    edge5.setCost([0, 25, 60], [5, 35])
    edge5.setTime([0, 60], [10])
    
    Gt = Graph([node1, node2, node3, node4], [edge1, edge2, edge3, edge4, edge5])
    # print(Gt.findEdge(node1, node2))

    model = Tdsp()

    # New test 1 passed
    model.start = 2
    model.goal = 4
    model.graph = Gt
    t_d = 0
    t_a = 60

    #model.print()
    print("Solution Found: ")
    res = model.solve(t_d, t_a)
    print(res)

if __name__ == '__main__':
    main(sys.argv)
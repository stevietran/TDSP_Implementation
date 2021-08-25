from copy import deepcopy
from models.PiecewiseFunction import FuncDomain, PiecewiseFunc

class GraphNode(object):
    def __init__(self, nodenumber):
        self.__neighbours = []
        self.__parentNode = []
        self.__costToStart = float("inf")
        self.lamda = None
        self.tau = float("inf")
        self.S = FuncDomain(0, 0)
        self.T = None
        self.nodeNumber = nodenumber
        self.atmc = None
        self.w = 0
        self.ETA = 0 #lambda
        self.minAtmc = 0
    
    def addNeighbour(self, next):
        self.__neighbours.append(next)

    def __hash__(self):
        return hash(self.nodeNumber)

    def __eq__(self, other):
        return self.nodeNumber == other.nodeNumber

    def setCostToStart(self, cost):
        self.__costToStart = cost

    def addParent(self, node):
        self.__parentNode.append(node)

    def getCostToStart(self):
        return self.__costToStart

    def getParentNode(self):
        return self.__parentNode

    def getNeighbours(self):
        return self.__neighbours

    def setLambda(self, value, t_a):
        self.lamda = value
        self.atmc = PiecewiseFunc([self.lamda, t_a], [float("inf")])
        self.T = FuncDomain(self.lamda, t_a)
    
    def setAtmcStart(self):
        self.atmc.setValue([0])
        self.tau = 0
        self.S = deepcopy(self.T)

    def getAtmcTime(self, value):
        return self.atmc.findTime(value)

    # For testing
    def printNeighbours(self):
        print(self.__neighbours)

class GraphEdge(object):
    def __init__(self, value, node_from, node_to):
        self.value = value
        self.node_from = node_from
        self.node_to = node_to
        self.cost_func = None
        self.time_func = None
        self.atmc = None
        self.ETA = 0
        self.S = FuncDomain(0,0)
        self.T = None
        self.R = None
    
    def setCost(self, step, value):
        self.cost_func = PiecewiseFunc(step, value) 
    
    def setTime(self, step, value):
        self.time_func = PiecewiseFunc(step, value)

    def getCost(self):
        return self.cost_func
    
    def getTime(self):
        return self.time_func

class Graph(object):
    def __init__(self, nodes = [], edges = []):
        self.nodes = nodes
        self.edges = edges

    def insertNode(self, new_node):
        self.nodes.append(new_node)

    def insertEdge(self, new):
        self.edges.append(new)

    def findEdge(self, node1, node2):
        for edge in self.edges:
            if edge.node_from == node1 and edge.node_to == node2:
                return edge

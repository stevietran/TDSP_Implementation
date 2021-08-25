from copy import deepcopy
import algorithms.dijkstra as ds
from os import path as path
from models.PiecewiseFunction import FuncDomain
from models.Queue import PriorityQueue

class Tdsp(object):
    def __init__(self):
        self.pq = PriorityQueue()
        self.start = None
        self.goal = None
        self.graph = None
        self.path_to_goal = []
        self.nodes = set()
        self.nodes_dict = {}
        self.t_e = None

    def atmcHelper(self, edge, t):
        return edge.node_from.atmc[t - edge.time_func[t]] + edge.cost_func[t - edge.time_func[t]]

    def findLambda(self):
        edges = []
        for item in self.graph.edges:
            travel_time = item.time_func.getValues()[0]
            a = tuple((item.node_from.nodeNumber, item.node_to.nodeNumber, travel_time))
            edges.append(a)
        
        g = ds.build_graph(edges)

        d, prev = ds.dijkstra(g, self.start)

        # print("List of prev node for each destination: {}".format(prev))
        
        # print("List of distance each destination: {}".format(d))
    
        return (d)

    def solve(self, t_d, t_a):
        # print("TO BE DONE") 
        # Find lambda and create atmc
        lamdas = self.findLambda()

        for node in self.graph.nodes:
            num = node.nodeNumber
            node.setLambda(lamdas[num], t_a)

            # Initialize start node 
            if num == self.start:
                node.setAtmcStart()
            
            # creat queue
            self.pq.add_task(node, node.tau)
        
        currNode = self.pq.pop_task()
        #print("Current node: {}".format(currNode.nodeNumber))

        while not self.pq.isEmpty() and currNode.nodeNumber != self.goal:
            # Find earliest time point equal tau
            t_i = currNode.getAtmcTime(currNode.tau)
            #print("Current node t_i: {}".format(t_i))
            currNode.S = FuncDomain(t_i, t_a)
            for neighbor in currNode.getNeighbours():
                edge = self.graph.findEdge(currNode, neighbor)
                # Assume travel time is a constant for each edge
                travel_time = edge.time_func.getValues()[0]
                if t_i <= t_a - travel_time:
                    edge.R = FuncDomain(t_i, t_a - travel_time)
                    
                    # find min cost function of edge
                    edge.atmc = deepcopy(edge.cost_func)
                    edge.atmc.shiftLeft(travel_time)
                    edge.atmc.addConstant(currNode.tau)
                    atmcDomain = edge.R - edge.S
                    atmcDomain.addConstant(travel_time)
                    edge.atmc.setInterval(atmcDomain.xMin, atmcDomain.xMax)

                    # New edge S
                    edge.S = deepcopy(edge.R)
                    
                    # find min cost function of node
                    neighbor.atmc = deepcopy(neighbor.atmc.minTwo(edge.atmc))
                    domain = neighbor.T - neighbor.S
                    neighbor.tau = neighbor.atmc.findMin(domain)
                    
                    # Update task
                    #print("Updated neighbor node {0}: {1}, {2}. Tau: {3}".format(neighbor.nodeNumber, neighbor.atmc.getSteps(), neighbor.atmc.getValues(), neighbor.tau))
                    self.pq.add_task(neighbor, neighbor.tau)
            if currNode.S == currNode.T:
                currNode = self.pq.pop_task()
                #print("New node: {}".format(currNode.nodeNumber))
            else:
                domain = currNode.T - currNode.S
                #currNode.atmc.setInterval(domain.xMin, domain.xMax)
                currNode.tau = currNode.atmc.findMin(domain)
                self.pq.add_task(currNode, currNode.tau)
                #print("Add current node again: {0}. tau: {1}".format(currNode.nodeNumber, currNode.tau))
                currNode = self.pq.pop_task()
                #print("New node: {}".format(currNode.nodeNumber))
        
        node_e = self.findNodeById(self.goal)
        self.t_e = node_e.getAtmcTime(node_e.tau)
        self.pathFinder(t_d, t_a)
        
        resNodes = [self.goal]
        resW = [0]
        resArivalTime = [self.t_e]
        #print("Found path:")
        for node in self.path_to_goal:
            resNodes.append(node.nodeNumber)
            resW.append(node.w)
            resArivalTime.append(node.ETA)
            #print("Node: {0}. Waiting time: {1}.".format(node.nodeNumber,node.w))
        
        return {"Path": resNodes, "Arrival Time": resArivalTime, "Waiting Time": resW}
    
    def pathFinder(self, t_d, t_a):
        currNode = self.findNodeById(self.goal)
        t_i = self.t_e
        # print("Node: {0}. Arrival Time: {1}".format(currNode.nodeNumber, t_i))
        while currNode.nodeNumber != self.start:
            found = False
            for node in currNode.getParentNode():
                edge = self.graph.findEdge(node, currNode)
                time_func = edge.getTime()
                travel_time = time_func.getFuncValue(t_i)
                
                cost_func = edge.getCost()
                cost = cost_func.getFuncValue(t_i - travel_time)

                for t_j in range(0, t_i - travel_time + 1): 
                    atmc_i = currNode.atmc.getFuncValue(t_i)
                    atmc_j = node.atmc.getFuncValue(t_j)
                    if atmc_i == atmc_j + cost:
                        self.path_to_goal.append(node)
                        node.w = t_i - travel_time - t_j

                        currNode = node
                        found = True
                        t_i = t_j
                        node.ETA = t_j
                        break
            
                if found:
                    break

    def findNodeById(self, id):
        for node in self.graph.nodes:
            if node.nodeNumber == id:
                return node

    def print(self):
        print("Node list:")
        for i in range(len(self.graph.nodes)):
            print("Node {0}: {1}".format(i, self.graph.nodes[i]))
        print("Edge list:")
        for i in range(len(self.graph.edges)):
            print("Edge {0}: {1}".format(i, self.graph.edges[i]))

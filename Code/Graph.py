from random import randint, choice
from copy import deepcopy

from Meal import *
from Node import *

# import networkx as nx

class Graph:

    def __init__(self, nbrChefs, nbrClients):
        self.nbrChefsTotal = nbrChefs
        self.nbrChefsCurrent = 0
        self.nbrClientsTotal = nbrClients
        self.nbrClientsCurrent = 0
        self.nbrEmptyVertices = randint(nbrClients, (3*nbrClients))

        self.nbrVertices = self.nbrEmptyVertices + nbrChefs + nbrClients + 1 # +1 == DeliveryDepot
        self.nbrEdges = int(  (randint(15,25)/10) * self.nbrVertices  )

        self.edges = [] ; self.vertices = [] ; self.chefs = [] ; self.clients = [] ; self.meals = []
        self.deliveryDepot = False

        self.maxDistance = 64
        self.adjacencyMatrix = [[ None for j in range (self.nbrVertices) ] for i in range (self.nbrVertices)]
        self.generateGraph()

        self.copyAdjacencyMatrix = deepcopy(self.adjacencyMatrix)

        self.Floyd_Warshall(self.copyAdjacencyMatrix)

        self.assureTriangleInequality()

        self.Floyd_Warshall(self.adjacencyMatrix)

        self.createRandomMeals()


    def getClients(self):
    	return self.clients


    def getChefs(self):
    	return self.chefs


    def getDeliveryDepot(self):
    	return self.deliveryDepot


    def getMeals(self):
    	return self.meals



    def generateGraph(self):
        createdVertices = 0
        createdEdges = 0
        self.deliveryDepot = Node(NodeType.DeliveryDepot, createdVertices)
        self.vertices.append(self.deliveryDepot)
        createdVertices += 1

        # creating a connected graph with  #edges = #vertices - 1
        while createdVertices < self.nbrVertices:
            newNode = self.getRandomNode(createdVertices)
            self.connectVertices(choice(self.vertices), newNode)
            self.vertices.append(newNode)
            createdVertices += 1
            createdEdges += 1

        # adding the remaining edges
        while createdEdges < self.nbrEdges:
            found = False
            NodeA = NodeB = None
            while not found:
                NodeA = choice(self.vertices)
                self.vertices.remove(NodeA)
                NodeB = choice(self.vertices)
                self.vertices.append(NodeA)

                found = (NodeA != NodeB) and (NodeB not in NodeA.neighbours)

            self.connectVertices(NodeA, NodeB)
            createdEdges += 1


    def createRandomMeals(self):

    	for client in self.clients:

	    	destination = client
	    	chef = choice(self.chefs)
	    	drt = self.dist(destination, chef)
	    	ddt = randint(8,24) # TODO
	    	deviation = randint(3, max(5,ddt//2))

	    	self.meals.append( Meal(chef, destination, drt, ddt, deviation) )
    		


    def getRandomNode(self, index):
        #if self.nbrChefsCurrent == self.nbrChefsTotal and self.nbrClientsCurrent == self.nbrClientsTotal:
        #    print("lolo")
        if self.nbrChefsCurrent == self.nbrChefsTotal: # only Clients left
            self.nbrClientsCurrent += 1
            newClient = Node(NodeType.Client, index)
            self.clients.append(newClient)
            return newClient

        elif self.nbrClientsCurrent == self.nbrClientsTotal: # only Chefs left
            self.nbrChefsCurrent += 1
            newChef = Node(NodeType.Chef, index)
            self.chefs.append(newChef)
            return newChef

        else:
            randNbr = randint(1, self.nbrVertices-1) # choose randomly a Chef or Client |  - 1 == DeliveryDepot
            if randNbr <= self.nbrClientsTotal:
                self.nbrClientsCurrent += 1
                newClient = Node(NodeType.Client, index)
                self.clients.append(newClient)
                return newClient

            else:
                self.nbrChefsCurrent += 1
                newChef = Node(NodeType.Chef, index)
                self.chefs.append(newChef)
                return newChef


    def connectVertices(self, NodeA, NodeB):
        NodeA.addNeighbour(NodeB)
        NodeB.addNeighbour(NodeA)
        weight = randint(1, self.maxDistance)
        self.adjacencyMatrix[NodeA.index][NodeB.index] = weight
        self.adjacencyMatrix[NodeB.index][NodeA.index] = weight
        #
        # for line in self.adjacencyMatrix:
        #     for i in line:
        #         print( " | {:2d}".format(i), end="" )
        #     print(" |")
        # print(min(NodeA.index, NodeB.index), max(NodeA.index, NodeB.index))



    def Floyd_Warshall(self, adjacencyMatrix):
        """
        None is infinity
        """
        for i in range(self.nbrVertices):
            adjacencyMatrix[i][i] = 0
        for k in range(self.nbrVertices):
            for i in range(self.nbrVertices):
                for j in range(self.nbrVertices):
                    if adjacencyMatrix[i][k] is not None and adjacencyMatrix[k][j] is not None:

                        if adjacencyMatrix[i][j] is None:
                            adjacencyMatrix[i][j] = adjacencyMatrix[i][k] + adjacencyMatrix[k][j]

                        elif adjacencyMatrix[i][j] > adjacencyMatrix[i][k] + adjacencyMatrix[k][j]:
                            adjacencyMatrix[i][j] = adjacencyMatrix[i][k] + adjacencyMatrix[k][j]


    def assureTriangleInequality(self):
    	for i in range(self.nbrVertices):
    		for j in range(self.nbrVertices):
    			if self.adjacencyMatrix[i][j] is not None:
    				if self.adjacencyMatrix[i][j] > self.copyAdjacencyMatrix[i][j]:
    					self.adjacencyMatrix[i][j] = self.copyAdjacencyMatrix[i][j]


    def dist(self, nodeA, nodeB):
    	#print( "A" + str(type(nodeA)) )
    	#print( "B" + str(type(nodeB)) )

    	if (0 <= nodeA.index < self.nbrVertices) and (0 <= nodeB.index < self.nbrVertices):
    		return self.adjacencyMatrix[nodeA.index][nodeB.index]
    	else:
        	return -1





"""
if __name__ == "__main__":
    G = Graph(2, 5)
    for v in G.vertices:
       print((v.index, v.type, len(v.neighbours)))

    for Mat in [G.adjacencyMatrix]:
        print("\n---------------------------------------------\n")
        for line in Mat:
           for i in line:
               print( " | "+str(i), end=" ") #{:3d}".format(i), end="" )
           print(" |")

    print("\nNbr Vertices", G.nbrVertices, "| Nbr Edges", G.nbrEdges)
"""



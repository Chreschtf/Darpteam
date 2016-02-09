from random import randint, choice
from copy import deepcopy
from math import hypot

# import networkx as nx

class Graph:
    def __init__(self, nbrNodes):
    	self.adjacencyMatrix = [[ None for j in range (nbrNodes) ] for i in range (nbrNodes)]
    	self.nbrNodes = nbrNodes
    	self.nbrEdges = int(  (randint(15,25)/10) * self.nbrNodes  )
    	self.nodes = []
    	self.generateGraph()

    	self.copyAdjacencyMatrix = deepcopy(self.adjacencyMatrix)
    	self.Floyd_Warshall(self.copyAdjacencyMatrix)
    	self.assureTriangleInequality()
    	self.shortestPathMatrix = deepcopy(self.adjacencyMatrix)
    	self.Floyd_Warshall(self.adjacencyMatrix)


    def randomCoords(self, iOther, jOther):
    	sum_I_J = randint(4, 14)
    	i = randint(2,sum_I_J-2)
    	j = sum_I_J - i

    	r = randint(0,1)
    	i = -i if r == 1 else i
    	r = randint(0,1)
    	j = -j if r == 1 else j

    	while not((0 <= i+iOther <= 50) and (0 <= j+jOther <= 50)):
    		sum_I_J = randint(4, 14)
    		i = randint(2,sum_I_J-2)
    		j = sum_I_J - i

    		r = randint(0,1)
    		i = -i if r == 1 else i
    		r = randint(0,1)
    		j = -j if r == 1 else j
    	i = iOther+i; j = jOther+j
    	return (i,j)



    def generateGraph(self):
        createdNodes = 0
        createdEdges = 0
        
        maxCoord = 50
        i = randint((maxCoord//2)-4,(maxCoord//2)+4); j = randint((maxCoord//2)-4,(maxCoord//2)+4)
        self.nodes.append(Node(i,j, createdNodes))
        createdNodes += 1

        # creating a connected graph with  #edges = #Nodes - 1
        while createdNodes < self.nbrNodes:
            nodeA = choice(self.nodes)
            (i,j) = self.randomCoords(nodeA.i, nodeA.j)
            nodeB = Node(i,j, createdNodes)
            self.nodes.append(nodeB)
            self.connectNodes(nodeA, nodeB)
            createdNodes += 1
            createdEdges += 1

        # adding the remaining edges
        while createdEdges < self.nbrEdges:
            found = False
            NodeA = choice(self.nodes)
            nbrTries = 0
            while len(nodeA.neighbours) > 4 and nbrTries < self.nbrNodes*2:
            	NodeA = choice(self.nodes)
            	nbrTries += 1
            self.nodes.sort(key=lambda obj: abs(obj.i - NodeA.i)+abs(obj.j - NodeA.j))

            i = 1 # self.nodes[0] is NodeA itself
            while i < len(self.nodes) and (self.nodes[i] in NodeA.neighbours):
            	i += 1

            if i < len(self.nodes):
            	self.connectNodes(NodeA, self.nodes[i])
            	createdEdges += 1



    def connectNodes(self, NodeA, NodeB):
        NodeA.addNeighbour(NodeB)
        NodeB.addNeighbour(NodeA)
        weight = hypot(NodeA.i-NodeB.i , NodeA.j-NodeB.j)
        self.adjacencyMatrix[NodeA.index][NodeB.index] = weight
        self.adjacencyMatrix[NodeB.index][NodeA.index] = weight



    def Floyd_Warshall(self, adjacencyMatrix):
        """
        None is infinity
        """
        for i in range(self.nbrNodes):
            adjacencyMatrix[i][i] = 0
        for k in range(self.nbrNodes):
            for i in range(self.nbrNodes):
                for j in range(self.nbrNodes):
                    if adjacencyMatrix[i][k] is not None and adjacencyMatrix[k][j] is not None:

                        if adjacencyMatrix[i][j] is None:
                            adjacencyMatrix[i][j] = adjacencyMatrix[i][k] + adjacencyMatrix[k][j]

                        elif adjacencyMatrix[i][j] > adjacencyMatrix[i][k] + adjacencyMatrix[k][j]:
                            adjacencyMatrix[i][j] = adjacencyMatrix[i][k] + adjacencyMatrix[k][j]



    def assureTriangleInequality(self):
    	for i in range(self.nbrNodes):
    		for j in range(self.nbrNodes):
    			if self.adjacencyMatrix[i][j] is not None:
    				if self.adjacencyMatrix[i][j] > self.copyAdjacencyMatrix[i][j]:
    					self.adjacencyMatrix[i][j] = self.copyAdjacencyMatrix[i][j]



    def dist(self, nodeA, nodeB):
    	if (0 <= nodeA.index < self.nbrNodes) and (0 <= nodeB.index < self.nbrNodes):
    		return self.adjacencyMatrix[nodeA.index][nodeB.index]
    	else:
        	return -1


"""
if __name__ == "__main__":
    G = Graph(8)
    for v in G.nodes:
       print((v.index, "	", v.i, v.j, "		"), end="")
       print([neigh.index for neigh in v.neighbours])


    for Mat in [G.adjacencyMatrix]:
        print("\n---------------------------------------------\n")
        for line in Mat:
           for i in line:
               print( " | "+str(i), end=" ") #{:3d}".format(i), end="" )
           print(" |")

    print("\nNbr Nodes", G.nbrNodes, "| Nbr Edges", G.nbrEdges)

"""


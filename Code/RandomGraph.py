from random import randint, choice
from enum import Enum


class Graph:

    def __init__(self, nbrChefs, nbrClients):
        self.nbrVertices = nbrChefs + nbrClients + 1 # +1 == DeliveryDepot
        self.nbrEdges = int(  (randint(15,25)/10) * self.nbrVertices  )

        self.nbrChefsTotal = nbrChefs
        self.nbrChefsCurrent = 0
        self.nbrClientsTotal = nbrClients
        self.nbrClientsCurrent = 0
        self.deliveryDepot = False

        self.edges = []
        self.vertices = []
        self.chefs = []
        self.clients = []

        self.maxDistance = 64
        self.adjacencyMatrix = [[ 999999 for j in range (self.nbrVertices) ] for i in range (self.nbrVertices)]
        #self.predecessors = [[ 0 for j in range (self.nbrVertices) ] for i in range (self.nbrVertices)]
        self.generateGraph()

        self.Floyd_Warshall()


    def generateGraph(self):
        createdVertices = 0
        createdEdges = 0
        self.vertices.append(Vertex(VertexType.DeliveryDepot, createdVertices))
        createdVertices += 1

        # creating a connected graph with  #vertices = #edges - 1
        while createdVertices < self.nbrVertices:
            # newEdge = Edge(self.maxDistance)
            newVertex = self.getRandomVertex(createdVertices)
            self.connectVertices(choice(self.vertices), newVertex)
            self.vertices.append(newVertex)
            createdVertices += 1
            createdEdges += 1

        # adding the remaining edges
        while createdEdges < self.nbrEdges:
            found = False
            vertexA = vertexB = None
            while not found:
                vertexA = choice(self.vertices)
                self.vertices.remove(vertexA)
                vertexB = choice(self.vertices)
                self.vertices.append(vertexA)

                found = (vertexA != vertexB) and (vertexB not in vertexA.neighbours)

            self.connectVertices(vertexA, vertexB)
            createdEdges += 1
        for vertex in self.vertices:
            if len(vertex.neighbours) == 0:
                print('Ups!')


    def getRandomVertex(self, index):
        if self.nbrChefsCurrent == self.nbrChefsTotal and self.nbrClientsCurrent == self.nbrClientsTotal:
            print("lolo")
        if self.nbrChefsCurrent == self.nbrChefsTotal:
            self.nbrClientsCurrent += 1
            return Vertex(VertexType.Client, index)
        elif self.nbrClientsCurrent == self.nbrClientsTotal:
            self.nbrChefsCurrent += 1
            return Vertex(VertexType.Chef, index)
        else:
            randNbr = randint(1, self.nbrVertices-1) # - 1 == DeliveryDepot
            if randNbr <= self.nbrClientsTotal:
                self.nbrClientsCurrent += 1
                return Vertex(VertexType.Client, index)
            else:
                self.nbrChefsCurrent += 1
                return Vertex(VertexType.Chef, index)


    def connectVertices(self, vertexA, vertexB):
        vertexA.addNeighbour(vertexB)
        vertexB.addNeighbour(vertexA)
        #
        # for line in self.adjacencyMatrix:
        #     for i in line:
        #         print( " | {:2d}".format(i), end="" )
        #     print(" |")
        # print(min(vertexA.index, vertexB.index), max(vertexA.index, vertexB.index))
        weight = randint(1, self.maxDistance)
        self.adjacencyMatrix[vertexA.index][vertexB.index] = weight
        self.adjacencyMatrix[vertexB.index][vertexA.index] = weight


    def Floyd_Warshall(self):
        """
        None is infinity
        """
        for i in range(self.nbrVertices):
            self.adjacencyMatrix[i][i] = 0
        for k in range(self.nbrVertices):
            for i in range(self.nbrVertices):
                for j in range(self.nbrVertices):
                    if self.adjacencyMatrix[i][k] is not None and self.adjacencyMatrix[k][j] is not None:

                        if self.adjacencyMatrix[i][j] is None:
                            self.adjacencyMatrix[i][j] = self.adjacencyMatrix[i][k] + self.adjacencyMatrix[k][j]

                        elif self.adjacencyMatrix[i][j] > self.adjacencyMatrix[i][k] + self.adjacencyMatrix[k][j]:
                            self.adjacencyMatrix[i][j] = self.adjacencyMatrix[i][k] + self.adjacencyMatrix[k][j]


    def getDist(self, i, j):
        if (0 <= i < self.nbrVertices) and (0 <= j < self.nbrVertices):
            return self.adjacencyMatrix[i][j]
        else:
            return -1


    """
    def constructPredecessors(self):
        for i in range(len(self.adjacencyMatrix)):
            for j in range(len(self.adjacencyMatrix)):
                if self.adjacencyMatrix[i][j] is not None and self.adjacencyMatrix[i][j] != 0:
                    self.predecessors[i][j] = i
                else:
                    self.predecessors[i][j] = -1


    def getPath(self, i, j, path=list()):
        if i == j:
            path.insert(0, i)
            return path
        elif self.predecessors[i][j] == 0:
            print(" no predecessor !!")
        else:
            path.insert(0, j)
            return self.getPath(i, self.predecessors[i][j], path)
    """



class VertexType(Enum):
    Chef = 1
    Client = 2
    DeliveryDepot = 3



class Vertex:

    def __init__(self, type, index):
        self.neighbours = []
        self.type = type
        self.index = index


    def addNeighbour(self, newNeighbour):
        self.neighbours.append(newNeighbour)



"""
if __name__ == "__main__":
    G = Graph(15, 20)
    for v in G.vertices:
       print((v.index, v.type))

    for Mat in [G.adjacencyMatrix]:
        print("\n---------------------------------------------\n")
        for line in Mat:
           for i in line:
               print( " | {:3d}".format(i), end="" )
           print(" |")

    print("\nNbr Vertices", G.nbrVertices, "| Nbr Edges", G.nbrEdges)
"""

"""
class Edge:
    def __init__(self, maxDistance):
        self.weight = randint(1, maxDistance)
"""




from NodeType import *

class Node:
    def __init__(self, _type, index):
        self.neighbours = []
        self._type = _type
        self.index = index


    def addNeighbour(self, newNeighbour):
        self.neighbours.append(newNeighbour)



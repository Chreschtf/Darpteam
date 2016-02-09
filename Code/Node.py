from NodeType import *

class Node:
    def __init__(self, i, j, index):
    	self.i = i
    	self.j = j
    	self.neighbours = []
    	#self._type = _type
    	self.index = index




    def addNeighbour(self, newNeighbour):
        self.neighbours.append(newNeighbour)


    #def setType(self, _type):
    #	self._type = _type



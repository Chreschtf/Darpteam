from Node import *
from Stop import *
class Block:
    def __init__(self,t0,tE):
        self.start=t0
        self.end=tE


        self.stops=[]

    def addStop(self,node,time):
        self.stops.append(Stop(node,time))

    def
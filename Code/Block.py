from Node import *
from Stop import *
class Block:
    def __init__(self,t0,tE):
        self.start=t0
        self.end=tE


        self.stops=[]

        self.prevSlack=0
        self.nextSlack=0

    def addStop(self,node,time):
        self.stops.append(Stop(node,time))

    def getFirstStop(self):
        return self.stops[0]

    def getLastStop(self):
        return self.stops[-1]

    def getStopAt(self,i):
        return self.stops[i]

    def getEnd(self):
        return self.end

    def getStart(self):
        return self.start

    def case1(self,meal):
        pass
    def case2(self,meal):
        pass
    def case3(self,meal):
        pass
    def case4(self,meal):
        pass

    def getPrevSlack(self):
        return self.prevSlack

    def getNextSlack(self):
        return self.nextSlack
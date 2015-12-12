from Node import *
from Stop import *
class Block:
    def __init__(self,stop1,stop2,prevTime,nextTime):
        self.start=stop1.getST()
        self.end=stop2.getST()


        self.stops=[stop1,stop2]

        self.prevSlack=self.start-prevTime
        self.nextSlack=self.end-nextTime

    def addStop(self,node,time):
        self.stops.append(Stop(node,time))

    def getFirstStop(self):
        return self.stops[0]

    def getLastStop(self):
        return self.stops[-1]

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

    def __str__(self):
        txt="Block : \n"
        txt+="Start time : {0} , End time : {1}\n".format(self.start,self.end)
        txt+="Stops : \n["
        for stop in self.stops:
            txt+=str(stop)+" "
        txt=txt[:-1]+"]"
        return txt
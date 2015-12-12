from Node import *
from Stop import *
class Block:
    def __init__(self,stop1,stop2,_prevSlack,_nextSlack):
        self.start=stop1.getST()
        self.end=stop2.getST()


        self.stops=[stop1,stop2]

        self.prevSlack=_prevSlack
        self.nextSlack=_nextSlack

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

    def calcUPnDOWN(self):

        #setting BDOWN and BUP
        for r in range(len(self.stops)):
            bup=float("inf")
            bdown=float("inf")
            for t in range(r+1):
                bup=min(bup,self.stops[t].getST()-self.stops[t].getET())
                bdown=min(bdown,self.stops[t].getLT()-self.stops[t].getST())
            self.stops[r].setBUP(min(bup,self.prevSlack))
            self.stops[r].setBDOWN(bdown)

            aup=float("inf")
            adown=float("inf")
            for t in range(r,len(self.stops)):
                aup=min(aup,self.stops[t].getST()-self.stops[t].getET())
                adown=min(adown,self.stops[t].getLT()-self.stops[t].getST())
            self.stops[r].setAUP(aup)
            self.stops[r].setADOWN(min(adown,self.nextSlack))



    def __str__(self):
        txt="Block : \n"
        txt+="Start time : {0} , End time : {1}\n".format(self.start,self.end)
        txt+="Stops : \n[\n"
        for stop in self.stops:
            txt+=str(stop)+" "
        txt=txt[:-1]+"]\n"
        txt+="Prev Slack : {0} , Next Slack : {1}".format(self.prevSlack,
                                                          self.nextSlack)
        return txt
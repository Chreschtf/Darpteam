from Node import *
from Stop import *
class Block:
    def __init__(self,stop1,stop2,_prevSlack,_nextSlack):
        self.start=stop1.getST()
        self.end=stop2.getST()


        self.stops=[stop1,stop2]

        self.prevSlack=_prevSlack
        self.nextSlack=_nextSlack

        self.r=0
        self.a=float("inf")

        self.a=min(self.a,stop1.getA(),stop2.getA())
        self.r=max(self.r,stop2.getR(),stop1.getR())


        self.shiftSchedule(self.r)
        self.calcUPnDOWN()

    def calcAandR(self):
        r=0
        a=float("inf")
        for stop in self.stops:
            r=max(stop.getR(),r)
            a=min(stop.getA(),a)
        self.r=r
        self.a=a

    def getA(self):
        return self.a

    def getR(self):
        return self.r

    def getFirstStop(self):
        return self.stops[0]

    def getLastStop(self):
        return self.stops[-1]

    def getStopAt(self,i):
        return self.stops[i]

    def getEnd(self):
        return self.stops[-1].getST()

    def getStart(self):
        return self.stops[0].getST()

    def setPrevSlack(self,slack):
        self.prevSlack=slack

    def setNextSlack(self,slack):
        self.nextSlack=slack

    def addLastStop(self,stop):
        self.stops.append(stop)

    def setFirstStop(self,stop):
        self.stops.insert(0,stop)

    def insertStop(self,i,stop):
        self.stops.insert(i,stop)

    def getPrevSlack(self):
        return self.prevSlack

    def getNextSlack(self):
        return self.nextSlack

    def blockFusion(self,block):
        """
        combining 2 blocks
        """
        self.stops.extend(block.stops)

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

    def shiftSchedule(self,shift):
        #self.prevSlack+=shift
        #self.nextSlack-=shift
        for stop in self.stops:
            stop.shiftST(shift)

        self.start=self.stops[0].getST()
        self.end=self.stops[-1].getST()

    def shiftScheduleBefore(self,stop,shift):
        #self.prevSlack+=shift
        i=0
        while self.stops[i]!=stop:
            self.stops[i].shiftST(shift)
            i+=1
        self.start=self.stops[0].getST()

    def shiftScheduleAfter(self,stop,shift):
        #self.nextSlack-=shift
        i=len(self.stops)-1
        while self.stops[i]!=stop:
            self.stops[i].shiftST(shift)
            i-=1
        self.end=self.stops[-1].getST()

    def shiftScheduleBetween(self,stop1,stop2,shift):
        i=self.stops.index(stop1)+1
        end=self.stops.index(stop2)
        while i<end:
            self.stops[i].shiftST(shift)
            i+=1


    def calcDeviation(self):
        deviation=0
        for stop in self.stops:
            deviation+=abs(stop.getST()-stop.getDT())

        return deviation

    def calcServiceTime(self):
        return self.stops[-1].getST()-self.stops[0].getST()


    def getNbrOfMeals(self):
        return len(self.stops)//2

    def getChargeBefore(self,i):
        charge=0
        j=0
        while j<=i:
            if self.stops[j].isPickup():
                charge+=1
            else:
                charge-=1
            j+=1
        return charge

    def removePastStops(self,time):
        i=0
        meals=dict()
        while i<len(self.stops) and self.stops[i].getST()<time:
            i += 1
            meals.setdefault(stop.getMeal(),[]).append(stop)
        for meal in meals:
            if len(meals[meal])==2:
                self.stops.remove(meals[meal][0])
                self.stops.remove(meals[meal][1])


    def getCharge(self):
        return self.getNbrOfMeals()

    def respectCharge(self,maxCharge):
        charge=0
        respect=True
        i=0
        while i<len(self.stops) and respect:
            if self.stops[i].isPickup():
                charge+=1
            else:
                charge-=1
            respect=charge<=maxCharge
            i+=1
        return respect

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

    def __lt__(self, other):
        return len(self.stops)<len(other.stops)

    def __len__(self):
        return len(self.stops)

    def __contains__(self, meal):
        contains=False
        i=0
        while not contains and i<len(self.stops):
            if stop.getMeal()==meal:
                contains=True
            i+=1
        return contains
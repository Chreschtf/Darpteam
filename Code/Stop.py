class Stop:
    def __init__(self, _node, _time, _meal,_pickup):
        self.node = _node
        self.st = _time  # scheduled time
        self.meal = _meal
        self.pickup=_pickup

        self.bup = 0  # max time preceding stops can be advanced  [0..r]
        self.bdown = 0  # max time preceding stops can be delayed  [0..r]
        self.aup = 0  # max time following stops can be advanced  [r..d]
        self.adown = 0  # max time following stops can be delayed  [r..d]
        #
        # self.r=abs(min(self.st-self.getET(),0))
        # self.a=self.getLT()-self.st



    def getST(self):
        return self.st

    def getDT(self):
        if self.pickup:
            return 0
        else:
            return self.meal.getDDT()

    def getR(self):
        return abs(min(self.st-self.getET(),0))

    def getA(self):
        return self.getLT()-self.st


    def getET(self):
        if self.pickup:
            return self.meal.getEPT()
        else:
            return self.meal.getEDT()

    def getLT(self):
        if self.pickup:
            return self.meal.getLPT()
        else:
            return self.meal.getLDT()

    def getNode(self):
        return self.node

    def getBUP(self):
        return self.bup

    def getBDOWN(self):
        return self.bdown

    def getAUP(self):
        return self.aup

    def getADOWN(self):
        return self.adown

    def setST(self,newST):
        self.st=newST

    def setBUP(self,newBUP):
        self.bup=newBUP

    def setBDOWN(self,newBDOWN):
        self.bdown=newBDOWN

    def setAUP(self,newAUP):
        self.aup=newAUP

    def setADOWN(self,newADOWN):
        self.adown=newADOWN

    def getMeal(self):
        return self.meal

    def shiftST(self,shift):
        self.st+=shift

    def isPickup(self):
        return self.pickup


    def __str__(self):
        txt="Coords : {0} , time : {1} , ".format(self.node.coords,self.st)
        txt+="BUP : {0} , BDOWN : {1} , AUP : {2} , ADOWN : {3}\n".format(
            self.bup,self.bdown,self.aup,self.adown)
        return txt

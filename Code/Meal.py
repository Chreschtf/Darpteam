from Node import *

class Meal:
    def __init__(self,_chef,_destination,_drt,_ddt,_deviation):
        self.mrt = 60  #_drt  #maximal ride time
        self.chef = _chef
        self.destination = _destination
        self.deviation = _deviation   # maximum allowed deviation from desired
                                    # pickup or  delivery time
        self.ddt = _ddt   #desired delivery time
        self.ldt = self.ddt   #lates delivery time
        self.edt = _ddt-_deviation  #earliest delivery time
        self.ept = self.edt-self.mrt  #earliest pickup time
        self.drt = _drt   #direct ride time
        self.lpt = self.ldt -self.drt #latest pickup time


        self.disutility = 0
        self.newDisutility = 0

    def getDisutility(self):
        return self.disutility

    def getDDT(self):
        return self.ddt

    def getMRT(self):
        return self.ldt-self.ept

    def getEPT(self):
        return self.ept

    def getLDT(self):
        return self.ldt

    def getEDT(self):
        return self.edt

    def getLPT(self):
        return self.lpt

    def getDRT(self):
        return self.drt

    def getChef(self):
        return self.chef

    def getDestination(self):
        return self.destination

    def getDeviation(self):
        return self.deviation

    def __lt__(self, other):
        return self.ept<other.ept



from Node import *
from Graph import *

class Meal:
    def __init__(self,_mrt,_chef,_destination,_drt,_ddt,_earlier):
        self.mrt=_mrt   #maximal ride time
        self.chef=_chef
        self.destination=_destination
        self.ddt=_ddt   #desired delivery time
        self.ldt=self.ddt   #lates delivery time
        self.edt=_ddt-_earlier  #earliest delivery time
        self.ept=self.edt-self.mrt  #earliest pickup time
        self.drt=_drt   #direct ride time
        self.lpt=self.ldt -self.drt #latest pickup time

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
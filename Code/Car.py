from Block import *
from Meal import *

class Car:
    def __init__(self,_maxCharge,_start,duration,_depot):
        self.maxCharge=_maxCharge
        self.start=_start
        self.end=_start+duration
        self.depot=_depot

        self.schedule=[]
        self.schedule.append(Block(self.start,self.start))
        self.schedule.append(Block(self.end,self.end))
        self.schedule[0].addStop(self.depot,self.start)
        self.schedule[1].addStop(self.depot,self.end)

    def findFeasibleInsertions(self,meal):
        """
        Trying to fit the meal into the existing working schedule while not violating
        any constraints.

        :param meal:
        :return:
        """
        ept=meal.getEPT()
        ldt=meal.getLDT()
        #+1 (-1) car on ne recoit (livre) pas de repas au dépot
        if ept<=self.start and max(ept,self.start+1)<=meal.getLPT():
            ept=self.start+1
        if self.end<=ldt and min(ldt,self.end-1)<=meal.getEDT():
            ldt=self.end-1

        if self.start<ept and ldt<self.end:
        #meal delivery constraints must fit into car work schedule




        # for i in range(len(self.schedule)):     #pickup
        #     for j in range(i+1,len(self.schedule)):
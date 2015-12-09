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
        #+1 (-1) because we do not pickup (deliver) at the depot
        if ept<=self.start and max(ept,self.start+1)<=meal.getLPT():    #adjusting bounds
            ept=self.start+1
        if self.end<=ldt and min(ldt,self.end-1)<=meal.getEDT():        #adjusting bounds
            ldt=self.end-1

        #meal delivery constraints must fit into car work schedule
        #if they do not, the previous test/changes weren't able to adjust bounds
        # which means that it is infeasible for this car to cater this meal
        if self.start<ept and ldt<self.end:
            #we now try to find a Block where we can insert the pickup and
            # delivery of the meal
            for i in range(len(self.schedule)):
                if self.schedule[i]



        # for i in range(len(self.schedule)):     #pickup
        #     for j in range(i+1,len(self.schedule)):
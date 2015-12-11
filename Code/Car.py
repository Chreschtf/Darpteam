from Block import *
from Meal import *
from Stop import *

class Car:
    def __init__(self,_maxCharge,_start,duration,_depot,_graph):
        self.maxCharge=_maxCharge
        self.start=_start       #start of working schedule
        self.end=_start+duration    #end of working schedule
        self.depot=_depot
        self.graph=_graph

        self.schedule=[]

        #self.schedule.append(Stop(self.depot,self.start))
        #self.schedule.append(Stop(self.depot,self.end))



    def findFeasibleInsertions(self,meal):
        """
        Trying to fit the meal into the existing working schedule while not violating
        any constraints.

        :param meal:
        :return:
        """
        # ept=meal.getEPT()
        # ldt=meal.getLDT()
        # lpt=meal.getLPT()
        # edt=meal.getEDT()
        # #+1 (-1) because we do not pick-up (deliver) at the depot
        # if ept<=self.start and max(ept,self.start+1)<=meal.getLPT():    #adjusting bounds
        #     ept=self.start+1
        # if self.end<=ldt and min(ldt,self.end-1)<=meal.getEDT():        #adjusting bounds
        #     ldt=self.end-1
        #
        # #meal delivery constraints must fit into car work schedule
        # #if they do not, the previous test/changes weren't able to adjust bounds
        # # which means that it is infeasible for this car to cater this meal
        # if self.start<ept and ldt<self.end:
        #     #we now try to insert the pickup and delivery stop of the meal
        #
        #     for i in range(len(self.schedule)):


        #case0 : first Block is being created if possible
        if self.schedule==[]:
            self.case0(meal)
            #optimisation
            #return

        #case1 : pickup and delivery are inserted at the end of the
        # working schedule.
        lastDestination = self.schedule[-1].getLastStop().getNode()
        if self.schedule[-1].getEnd() \
            +self.graph.dist(lastDestination,meal.getChef()) < meal.getLPT() \
                and \
            self.schedule[-1].getEnd() \
            + self.graph.dist(lastDestination,meal.getChef()) \
            + self.graph.dist(meal.getChef(),meal.getDestination()) \
            + self.graph.dist(meal.getDestination(),self.depot) <self.end :
            self.schedule[-1].case1(meal)
            #optimisation

        #case 2 : pickup and delivery are consecutive stops in a block
        #case 4 : pickup and delivery are separated by at least one stop
        for block in self.schedule:
            block.case2(meal)
            block.case4(meal)

        #case 3 : pickup in the last block, delivery becomes last stop in
        # schedule
        self.schedule[-1].case3(meal)


        # pickup and delivery are in different blocks
        i=0
        #detirmining block for pickup :
        while i<len(self.schedule)-1 and (
                meal.getEPT() < self.schedule[i].getEnd()+ self.schedule[
                i].getNextSlack() or
                meal.getLPT() < self.schedule[i].getEnd()+ self.schedule[
                i].getNextSlack()):
            j=i+1
            #determining block for delivery :

            while j<len(self.schedule) and (
            self.schedule[i].getStart()-self.schedule[i].getPrevSlack() < \
                meal.getEDT()  or
            self.schedule[i].getStart()-self.schedule[i].getPrevSlack() < \
                meal.getDPT() ):
                j+=1


            i+=1



        for i in range(len(self.schedule)-1):
            #if ?
            for j in range(i+1,len(self.schedule)):
                pass




    def case0(self,meal):
        pass

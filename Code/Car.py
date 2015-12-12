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

        self.currentSchedule=[]
        self.feasibleSchedules=[]

    def getFeasibleSchedules(self):
        return self.feasibleSchedules

    def addIntoSameBlock(self,meal,utilityC):
        """
        Trying to fit the meal into the existing working schedule while
        pickup and delivery happen in the same block

        :param meal:
        :return:
        """


        if self.currentSchedule!=[]:
            #case1 : pickup and delivery are inserted at the end of the
            # working schedule.
            lastDestination = self.currentSchedule[-1].getLastStop().getNode()
            if self.currentSchedule[-1].getEnd() \
                +self.graph.dist(lastDestination,meal.getChef()) < meal.getLPT() \
                    and \
                self.currentSchedule[-1].getEnd() \
                + self.graph.dist(lastDestination,meal.getChef()) \
                + self.graph.dist(meal.getChef(),meal.getDestination()) \
                + self.graph.dist(meal.getDestination(),self.depot) <self.end :
                self.currentSchedule[-1].case1(meal)
                #optimisation

            #case 2 : pickup and delivery are consecutive stops in a block
            #case 4 : pickup and delivery are separated by at least one stop
            for block in self.currentSchedule:
                block.case2(meal)
                block.case4(meal)

            #case 3 : pickup in the last block, delivery becomes last stop in
            # schedule
            self.currentSchedule[-1].case3(meal)

            #return



        #case0 : first Block is being created if possible
        self.case0(meal,utilityC)
        #optimisation
        #return



    def addIntoDifferentBlocks(self,meal):


        # pickup and delivery are in different blocks
        i=0
        #detirmining block for pickup :
        while i<len(self.currentSchedule)-1 and (
                meal.getEPT() < self.currentSchedule[i].getEnd()+
                        self.currentSchedule[i].getNextSlack() or
                meal.getLPT() < self.currentSchedule[i].getEnd()+
                        self.currentSchedule[i].getNextSlack()):
            j=i+1
            #determining block for delivery :

            while j<len(self.currentSchedule) and (
            self.currentSchedule[i].getStart()-self.currentSchedule[i].getPrevSlack() < \
                meal.getEDT()  or
            self.currentSchedule[i].getStart()-self.currentSchedule[i].getPrevSlack() < \
                meal.getDPT() ):
                j+=1


            i+=1



        for i in range(len(self.currentSchedule)-1):
            #if ?
            for j in range(i+1,len(self.currentSchedule)):
                pass




    def case0(self,meal,utilityC):
        """
        First insertion to the schedule
        """

        stop1=Stop(meal.getChef(),
                   meal.getLDT()-self.graph.dist(meal.getChef(),meal.getDestination()),
                   meal,
                   True)
        stop2=Stop(meal.getDestination(),
                   meal.getLDT(),
                   meal,
                   False)
        prevSlack=stop1.getST()-self.start-\
                  self.graph.dist(self.depot,meal.getChef())
        nextSlack=self.end-stop2.getST()-self.graph.dist(self.depot,meal.getDestination())
        block=Block(stop1,stop2,prevSlack,nextSlack)
        block.calcUPnDOWN()
        self.feasibleSchedules.append(block)


from Block import *
from Meal import *
from Stop import *

from copy import deepcopy

class Car:
    def __init__(self,_maxCharge,_start,duration,_depot,_graph):
        self.maxCharge=_maxCharge
        self.start=_start       #start of working schedule
        self.end=_start+duration    #end of working schedule
        self.depot=_depot
        self.graph=_graph

        self.meals=[]

        self.currentSchedule=[]
        self.feasibleSchedules=[]

        self.serviceTime=0

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def getFeasibleSchedules(self):
        return self.feasibleSchedules

    def setCurrentSchedule(self,schedule):
        self.currentSchedule=schedule
        for i in range(len(self.currentSchedule)-1):
            stop1=self.currentSchedule[i].getLastStop()
            stop2=self.currentSchedule[i+1].getFirstStop()
            timeDiff=stop2.getST()- stop1.getST()
            dist=self.graph.dist(stop1.getNode(),stop2.getNode())
            slack=timeDiff-dist
            self.currentSchedule[i].setNextSlack(slack)
            self.currentSchedule[i+1].setPrevSlack(slack)


    def getServiceTime(self):
        return self.serviceTime

    def addIntoSameBlock(self,meal,scheduler):
        """
        Trying to fit the meal into the existing working schedule while
        pickup and delivery happen in the same block

        :param meal:
        :return:
        """

        self.feasibleSchedules=[]
        if self.currentSchedule!=[]:
            #case1 : pickup and delivery are inserted at the end of the
            # working schedule.
            self.case1(meal,scheduler)

            #case 2 : pickup and delivery are consecutive stops in a block
            self.case2(meal)

            #case 3 : pickup in the last block, delivery becomes last stop in
            # schedule
            self.currentSchedule[-1].case3(meal)
            #case 4 : pickup and delivery are separated by at least one stop
            self.case4(meal)

            return True



        #case0 : first Block is being created if possible
        self.case0(meal,scheduler)
        #return



    def addIntoDifferentBlocks(self,meal):

        # pickup and delivery are in different blocks
        i=0
        #choice of block for pickup :
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




    def case0(self,meal,scheduler):
        """
        First insertion to the schedule
        """
        if self.start+self.graph.dist(self.depot,meal.getChef())+meal.getDRT()+self.graph.dist(
                meal.getDestination(),self.depot)<=self.end:
            stop1=Stop(meal.getChef(),
                       self.start+meal.getDRT(),
                       meal,
                       True)
            stop2=Stop(meal.getDestination(),
                       self.start+meal.getDRT() \
                       +meal.getDRT(),
                       meal,
                       False)
            prevSlack=stop1.getST()-self.start-\
                      self.graph.dist(self.depot,meal.getChef())
            nextSlack=self.end-stop2.getST()-self.graph.dist(self.depot,meal.getDestination())
            block=Block(stop1,stop2,prevSlack,nextSlack)
            self.feasibleSchedules.append([block])


    def case1(self,meal,scheduler):
        """
        Following logic of algorithm case 1
        """
        #verify charge

        schedule=deepcopy(self.currentSchedule)
        block=schedule[-1]
        lastNode=block.getLastStop().getNode()
        if block.getEnd()+self.graph.dist(lastNode,meal.getChef())< meal.getLPT() and\
            block.getEnd()+ self.graph.dist(lastNode,meal.getChef()) \
            +meal.getDRT() + self.graph.dist(meal.getDestination(),self.depot) < \
            self.end:
            tpu=block.getEnd()+self.graph.dist(lastNode,meal.getChef())
            td=tpu+meal.getDRT()
            #ddt or dpt
            shift=0
            w=0
            if td <= meal.getLDT():
                tpu=meal.getLDT()-meal.getDRT()
                td=meal.getLDT()
                w=tpu-block.getEnd()-self.graph.dist(lastNode,meal.getChef())
                if scheduler.getConstant("c2")!=0:
                    shift=max((scheduler.getConstant("c6")+
                               scheduler.getConstant("c8")*scheduler.getUi(meal.getEPT()))/2*scheduler.getConstant("c2"),0)
                    shift=min(shift,w,meal.getDeviation())
                    tpu-=shift
                    td-=shift

                else:
                    if scheduler.getConstant("c1")<scheduler.getConstant("c6")\
                        +scheduler.getConstant("c8")*scheduler.getUi(meal.getEPT()):
                        w=max(0,w-meal.getDeviation())
                        tpu=block.getEnd()+self.graph.dist(lastNode,meal.getChef())+w
                        td=tpu+meal.getDRT()

            else:
                shift=tpu-meal.getLDT()
                if shift > block.getLastStop().getBUP():
                    return False
                else:
                    td=meal.getLDT()
                    tpu=td-meal.getDRT()
                    ps=-shift
                    block.shiftSchedule(ps)
                    # for stop in block:
                    #     stop.shiftST(ps)

            stop1=Stop(meal.getChef(),tpu,meal,True)
            stop2=Stop(meal.getDestination(),td,meal,False)
            if w!=0: # after the current last stop there will be slack time -> create new block
                bb=Block(stop1,stop2,w,self.end-stop2.getST()-self.graph.dist(self.depot,
                                                                          stop2.getNode()))
                block.setNextSlack(w)
                schedule.append(bb)
                self.feasibleSchedules.append(schedule)
                return True

            if block.getNbrOfMeals()<self.maxCharge:
            # the 2 stops become the last 2 stops in the block and the schedule
                nextSlack=block.getNextSlack()

                block.addLastStop(stop1)
                block.addLastStop(stop2)

    def shiftStopsBefore(self,stop,ps):
        pass

    def shiftStopsAfter(self,stop,ds):
        pass


    def case2(self,meal):
        """

        """
        i=0
        while i<len(self.currentSchedule):
            schedule=deepcopy(self.currentSchedule)
            block=schedule[i]
            for j in range(len(block)-1):
                p=block.getStopAt(j)
                q=block.getStopAt(j+1)
                #checking charge-feasibility before launching the algorithm
                if block.getNbrOfMealsBefore(j)<self.maxCharge and self.case2Algo(p,q,meal):
                    schedule=deepcopy(self.currentSchedule)
                    block=schedule[i]
            i+=1



    def case2Algo(self,p,q,meal,j):

        deltaP=self.graph.dist(p.getNode(),meal.getChef())+meal.getDRT()+ \
               self.graph.dist(meal.getDestination(),q.getNode())-\
                self.graph.dist(p.getNode(),q.getNode())

        if deltaP <= p.getBUP()+q.getADOWN():
            tpu=0
            td=0
            ps=0
            ds=0
            gt=0
            et=0
            lt=0
            shift=0
            if deltaP>q.getADOWN():
                ps=0
                ds=deltaP
                tpu=p.getST()
                td=tpu+meal.getDRT()
            else:
                ds=q.getADOWN()
                ps=q.getADOWN()-deltaP
                tpu=p.getST()+ps+self.graph.dist(p.getNode(),meal.getChef())
                td=tpu+meal.getDRT()
            #ddt, so :
            gt =td
            et=meal.getEDT()
            lt=meal.getLDT()
            if gt<et:
                shift=et-gt
                if shift <=(q.getADOWN()-ds) or shift<=p.getBDOWN()-ps:
                    tpu+=shift
                    td+=shift
                    ds+=shift
                    ps+=shift
                    stop1=Stop(meal.getChef(),tpu,meal,True)
                    stop2=Stop(meal.getDestination(),td,meal,False)



            elif gt>lt:
                shift=gt-lt






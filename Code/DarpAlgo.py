from Car import *

class DarpAlgo:
    def __init__(self,_meals,_cars):
        self.meals=_meals
        self.cars=_cars

        #utilitiy constants :
        self.utilityC=dict()
        self.utilityC["c1"]=1
        self.utilityC["c2"]=1
        self.utilityC["c3"]=1
        self.utilityC["c4"]=1
        self.utilityC["c5"]=1
        self.utilityC["c6"]=1
        self.utilityC["c7"]=1
        self.utilityC["c8"]=1
        self.c1=1
        self.c2=1
        self.c3=1
        self.c4=1
        self.c5=1
        self.c6=1
        self.c7=1
        self.c8=1

    def createSchedules(self):
        for i in range(len(self.meals)):
            bestSchedules=[]
            for j in range(len(self.cars)):
                self.addToCar(self.meals[i],self.cars[j],self.utilityC)
                jSchedules=self.cars[i].getFeasibleSchedules()
                # if jSchedules!=[]: #feasible insertion -> new schedule(s)
                #     bestSchedule,minCost=self.findOptimalSchedule(jSchedules)
                #     bestSchedules.append([minCost,j,bestSchedule])
                print(jSchedules[0])
            if bestSchedules!=[]: #determine best overall schedule
                pass






    def addToCar(self,meal,car,utilityC):
        car.addIntoSameBlock(meal,utilityC)

    def findOptimalSchedule(self,schedules):
        pass
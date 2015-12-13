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
                #jSchedules=self.cars[i].getFeasibleSchedules()
                # if jSchedules!=[]: #feasible insertion -> new schedule(s)
                #     bestSchedule,minCost=self.findOptimalSchedule(jSchedules)
                #     bestSchedules.append([minCost,j,bestSchedule])
                bestSchedule=self.findBestCarSchedule(self.cars[j],
                                                      self.meals[i])
                bestSchedules.append(j)
                print(bestSchedule[1][0])
            if bestSchedules!=[]: #determine best overall schedule
                pass


    def addToCar(self,meal,car,utilityC):
        car.addIntoSameBlock(meal,utilityC)


    def scheduleOptimisation(self,schedule):

        for i in range(len(schedule)):
            deviation=schedule[i].calcDeviation()
            meals=schedule[i].getNbrOfMeals()
            min=round(self.c1/(2*self.c2)+deviation/meals)
            lb=0
            ub=schedule[i].getA()-schedule[i].getR()
            a=min
            if min<lb:
                a=lb
            elif min>ub:
                a=ub

            schedule[i].shiftSchedule(a)
        #update slack

    def findBestCarSchedule(self,car,meal):


        bestInsertion=[float("inf")]
        feasInserts=car.getFeasibleSchedules()
        for schedule in feasInserts:
            self.scheduleOptimisation(schedule)
            incDisutility=self.calcIncrementalCost(schedule,meal)
            bestInsertion=min(bestInsertion,[incDisutility,schedule])
        return bestInsertion


    def calcIncrementalCost(self,schedule,meal):

        meals=dict()
        for block in schedule:
            for stop in block.stops:
                meals.setdefault(stop.getMeal(),[]).append(stop)

        duNewMeal=self.disutilityFuncMeal(meal,meals[meal][0],
                                          meals[meal][1])
        meals.pop(meal)
        duOthers=0
        for meal in meals:
            duOthers+=self.disutilityFuncMeal(meal,meals[meal][0],
                                          meals[meal][1]) \
                        -meal.getDisutility()

        return duNewMeal+duOthers




    def disutilityFuncMeal(self,meal,stop1,stop2):
        x=meal.getDDT() - stop2.getST()
        y=stop2.getST()-stop1.getST() - meal.getDRT()
        dud=self.c1*x+self.c2*x*x
        dur=self.c3*y+self.c4*y*y
        return dud+dur




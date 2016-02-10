from Car import *

class DarpAlgo:
    def __init__(self,_meals,_cars):
        self.meals=_meals
        self.cars=_cars

        #utilitiy constants :
        self.constants=dict()
        self.constants["c1"]=1
        self.constants["c2"]=1
        self.constants["c3"]=1
        self.constants["c4"]=1
        self.constants["c5"]=0
        self.constants["c6"]=0
        self.constants["c7"]=0
        self.constants["c8"]=0
        self.constants["W1"]=60
        self.constants["W2"]=60

    def createSchedules(self):
        for i in range(len(self.meals)):
            bestSchedules=[]
            for j in range(len(self.cars)):
                self.addToCar(self.meals[i],self.cars[j],self)
                bestSchedule=self.findBestCarSchedule(self.cars[j],self.meals[i])
                if bestSchedule!=[float("inf")]: #determine best overall schedule
                    bestSchedule.append(j)
                    bestSchedules.append(bestSchedule)
            if bestSchedules!=[]:
                bestSchedules.sort()
                schedule=bestSchedules[0]
                self.cars[schedule[2]].setCurrentSchedule(schedule[1])
        i=0


    def addToCar(self,meal,car,utilityC):
        car.addIntoSameBlock(meal,utilityC)


    def scheduleOptimisation(self,schedule):

        for block in schedule:
            deviation = block.calcDeviation()
            meals = block.getNbrOfMeals()
            min = round(self.constants["c1"]/(2*self.constants["c2"])+deviation/meals)
            lb = 0
            ub = block.getA()-block.getR()
            a = min
            if min<lb:
                a = lb
            elif min>ub:
                a = ub

            block.shiftSchedule(a)

    def findBestCarSchedule(self,car,meal):


        bestInsertion = [float("inf")]
        feasInserts = car.getFeasibleSchedules()
        for schedule in feasInserts:
            self.scheduleOptimisation(schedule)
            incDisutility=self.calcIncrementalCost(schedule,meal,car)
            bestInsertion=min(bestInsertion,[incDisutility,schedule])
        return bestInsertion


    def calcIncrementalCost(self,schedule,meal,car):

        meals=dict()
        #assigning to every meal its pickup and delivery stops:
        for block in schedule:
            for stop in block.stops:
                meals.setdefault(stop.getMeal(),[]).append(stop)

        duNewMeal = self.disutilityFuncMeal(meal,meals[meal][0],meals[meal][1])
        meals.pop(meal)
        duOthers=0
        for meal in meals:
            duOthers += self.disutilityFuncMeal(meal,meals[meal][0],
                                          meals[meal][1]) \
                        -meal.getDisutility()

        return duNewMeal + duOthers

    def disutilityFuncCar(self,schedule,car):
        #calculating service time change:
        z=0
        for block in schedule:
            z+=block.calcServiceTime()
        z-=car.getServiceTime()
        vc=self.constants["c5"]
        pass


    def disutilityFuncMeal(self,meal,stop1,stop2):
        x = meal.getDDT() - stop2.getST()
        y = stop2.getST() - stop1.getST() - meal.getDRT()
        dud = self.constants["c1"]*x + self.constants["c2"]*x*x
        dur = self.constants["c3"]*y + self.constants["c4"]*y*y
        return dud + dur

    def getConstant(self,const):
        return self.constants.get(const,0)

    def getUi(self,ept):
        custInSys = 0
        carsAvailable = 0
        for meal in self.meals:
            if ept-self.constants["W1"] <=meal.getEPT() <= ept+self.constants["W2"] or\
                ept-self.constants["W1"] <=meal.getLDT() <= ept+self.constants["W2"]:
                custInSys += 1
        for car in self.cars:
            if car.getStart() <= ept+self.constants["W2"] or\
                ept-self.constants["W1"] <=car.getEnd():
                carsAvailable += 1

        #carsAvailable !=0 because otherwise the initial algorithm would not proceed in the first place
        return custInSys/carsAvailable



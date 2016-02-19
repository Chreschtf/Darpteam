from Car import *

class DarpAlgo:
    def __init__(self,_meals,_cars):
        _meals.sort()
        self.meals=_meals
        self.cars=_cars
        self.mealsNotInserted=[]

        #utilitiy constants :
        self.constants=dict()
        self.constants["c1"]=1
        self.constants["c2"]=1
        self.constants["c3"]=1
        self.constants["c4"]=1
        self.constants["c5"]=1
        self.constants["c6"]=2
        self.constants["c7"]=1
        self.constants["c8"]=2
        self.constants["W1"]=60
        self.constants["W2"]=60

    def createSchedules(self):
        self.mealsNotInserted=[]
        for i in range(len(self.meals)):
            bestSchedules=[]
            for j in range(len(self.cars)):
                self.addToCar(self.meals[i],self.cars[j])
                bestSchedule=self.findBestCarSchedule(self.cars[j],self.meals[i])
                if bestSchedule!=[float("inf")]: #determine best overall schedule
                    bestSchedule.append(j)
                    bestSchedules.append(bestSchedule)
            if bestSchedules!=[]:
                bestSchedules.sort()
                schedule=bestSchedules[0]
                self.cars[schedule[2]].setCurrentSchedule(schedule[1])
            else:
                self.mealsNotInserted.append(self.meals[i])
                #i=0


    def addToCar(self,meal,car):
        car.addIntoSameBlock(meal,self)
        car.addIntoDifferentBlocks(meal)


    def scheduleOptimisation(self,schedule,meal):
        I=0
        if len(schedule)==1:
            I=0
        elif meal in schedule[0]:
            I=-1
        elif meal in schedule[-1]:
            I=1

        Rmin=0
        Amax=float("inf")
        deviation=0
        nbrOfCustomers=0
        for block in schedule:
            block.calcAandR()
            Rmin=max(block.getR(),Rmin)
            Amax=min(block.getA(),Amax)
            deviation += block.calcDeviation()
            nbrOfCustomers += block.getNbrOfMeals()
        ui=self.getUi(meal.getEPT())
        aStar = round(-(-self.constants["c1"]*nbrOfCustomers-2*self.constants["c2"]*deviation + \
                        (self.constants["c6"]+self.constants["c8"]*ui)*I)/ \
                      (2*self.constants["c2"])*nbrOfCustomers)
        lb = 0
        ub = Amax-Rmin
        a = aStar
        if aStar<lb:
            a = lb
        elif aStar>ub:
            a = ub
        for block in schedule:
            block.shiftSchedule(a)

    def findBestCarSchedule(self,car,meal):


        bestInsertion = [float("inf")]
        feasInserts = car.getFeasibleSchedules()
        for schedule in feasInserts:
            self.scheduleOptimisation(schedule,meal)
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
            duOthers += self.disutilityFuncMeal(meal,meals[meal][0],meals[meal][1]) \
                        -meal.getDisutility()
        duOperator=self.disutilityFuncCar(schedule,meal,car)
        return duNewMeal + duOthers+duOperator

    def disutilityFuncCar(self,schedule,meal,car):
        #VCi = C5*z + C6*w + Ui*( C7*z + C8*w)
        #in our case : vc =z(c5-c6)+ui*z*(c7-c8) since change in service time z = - change in vehicle slack time w

        #calculating service time change:
        #
        z=0
        for block in schedule:
            z+=block.calcServiceTime()
        z-=car.getServiceTime()
        ui=self.getUi(meal.getEPT())
        return z*(self.constants["c5"]-self.constants["c6"])+ui*z*(self.constants["c7"]-self.constants["c8"])


    def disutilityFuncMeal(self, meal, pickup, delivery):
        x = meal.getDDT() - delivery.getST()
        y = delivery.getST() - pickup.getST() - meal.getDRT()
        dud = self.constants["c1"]*x + self.constants["c2"]*x*x
        dur = self.constants["c3"]*y + self.constants["c4"]*y*y
        return dud + dur

    def getConstant(self,const):
        return self.constants.get(const,0)

    def getUi(self,ept):
        custInSys = 0
        carsAvailable = 0
        for meal in self.meals:
            if ept-self.constants["W1"] <=meal.getEPT() <= ept+self.constants["W2"] or \
                                            ept-self.constants["W1"] <=meal.getLDT() <= ept+self.constants["W2"]:
                custInSys += 1
        for car in self.cars:
            if car.getStart() <= ept+self.constants["W2"] or \
                                    ept-self.constants["W1"] <=car.getEnd():
                carsAvailable += 1

        #carsAvailable !=0 because otherwise the initial algorithm would not proceed in the first place
        return custInSys/carsAvailable

    def removePastStops(self,time):
        for car in self.cars:
            car.removePastStops(time)

    def dynamicInsertion(self,time,meals):
        self.meals=meals
        self.removePastStops(time)
        self.createSchedules()


    def getNotInsertedMeals(self):
        return self.mealsNotInserted



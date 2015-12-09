class DarpAlgo:
    def __init__(self,_meals,_cars):
        self.meals=_meals
        self.cars=_cars

    def createSchedule(self):
        for i in range(self.meals):
            bestSchedules=[]
            for j in range(self.cars):
                jSchedules=[]
                self.addToCar(self.meals[i],self.cars[j],jSchedules)
                if jSchedules!=[]: #feasible insertion -> new schedule(s)
                    bestSchedule,minCost=self.findOptimalSchedule(jSchedules)
                    bestSchedules.append([minCost,j,bestSchedule])

            if bestSchedules!=[]: #determine best overall schedule
                pass






    def addToCar(self,meal,car,schedules):
        pass

    def findOptimalSchedule(self,schedules):
        pass
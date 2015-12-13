from DarpAlgo import *
from Car import *
from Meal import *
from Graph import *
from Node import *

from random import randint

if __name__=="__main__":
    g=Graph()
    depot=Node([5,5])
    chef1=Node([2,2])
    chef2=Node([3,3])
    client1=Node([4,4])
    client2=Node([1,1])
    car1=Car(3,0,100,depot,g)
    car2=Car(3,0,100,depot,g)
    meal1=Meal(3,chef1,client1,g.dist(chef1,client1),7,2)
    meal2=Meal(3,chef2,client2,g.dist(chef2,client2),14,2)
    meals=[]
    meals.append(meal1)
    meals.append(meal2)
    cars=[]
    cars.append(car1)
    #cars.append(car2)
    darp=DarpAlgo(meals,cars)
    darp.createSchedules()

    # cars=[]
    # meals=[]
    # for i in range(10):
    #     chef,client=Node([randint(0,10),randint(0,10)]),Node([randint(0,10),randint(0,10)])
    #     car=Car(randint(2,6),0,100,depot,g)
    #     meal=Meal(randint(2,5),chef,client,)

from DarpAlgo import *
from Car import *
from Graph import *
from Meal import *
from Node import *

from random import randint

if __name__=="__main__":
    n=17
    g=Graph(n)
    nodes = g.nodes
    depot = nodes[0]
    meals=[]
    i=1
    while i<n:
        chef1=nodes[i]
        client1=nodes[i+1]
        meal=Meal(chef1,client1,g.dist(chef1,client1),randint(230,260),200)
        meals.append(meal)
        i+=2
    car1=Car(12,0,800,depot,g)
    #car2=Car(6,0,900,depot,g)
    cars=[]
    cars.append(car1)
    #cars.append(car2)
    meals.sort()
    darp=DarpAlgo (meals,cars)
    darp.createSchedules()
    i=0
    # cars=[]
    # meals=[]
    # for i in range(10):
    #     chef,client=Node([randint(0,10),randint(0,10)]),Node([randint(0,10),randint(0,10)])
    #     car=Car(randint(2,6),0,100,depot,g)
    #     meal=Meal(randint(2,5),chef,client,)

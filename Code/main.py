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
    client1=Node([4,4])
    car1=Car(3,0,100,depot,g)
    meal1=Meal(3,chef1,client1,g.dist(chef1,client1),5,2)
    darp=DarpAlgo([meal1],[car1])
    darp.createSchedules()

    # cars=[]
    # meals=[]
    # for i in range(10):
    #     chef,client=Node([randint(0,10),randint(0,10)]),Node([randint(0,10),randint(0,10)])
    #     car=Car(randint(2,6),0,100,depot,g)
    #     meal=Meal(randint(2,5),chef,client,)

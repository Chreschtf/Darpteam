# /usr/bin/env python 3
# -*- coding: utf-8 -*-
import DarpAlgo
import Car
import Graph
import Meal
import Node
import os
from GraphDrawer import *
from random import randint


try:
	import Tkinter as Tk
except ImportError:
	import tkinter as Tk

class App:

	def __init__(self, master):
		
		mainFrame = Tk.Frame(master)
		mainFrame.pack(fill=Tk.BOTH,expand=True)
		
		self.parametersFrame = Tk.Frame(mainFrame,bg="pink")
		self.parametersFrame.pack(side=Tk.RIGHT,anchor="n",expand=True,fill=Tk.BOTH)
		self.mealsFrame = Tk.Frame(self.parametersFrame)
		self.mealsFrame.pack(side=Tk.TOP,anchor="nw")
		self.carsFrame = Tk.Frame(self.parametersFrame)
		self.carsFrame.pack(side=Tk.TOP,anchor="nw")
		
		
		self.displayFrame = Tk.Frame(mainFrame)
		self.displayFrame.pack(side=Tk.LEFT)
		
		self.dupeImage = Tk.PhotoImage(file=os.path.join("GUIELEM","duplicate.gif"))
		"""
		self.cooksEntry = Tk.Entry(self.parametersFrame)
		self.clientsEntry = Tk.Entry(self.parametersFrame)	
		self.cooksLabel = Tk.Label(self.parametersFrame,text="Amount of Cooks")
		self.clientsLabel = Tk.Label(self.parametersFrame,text="Amount of Clients")
		"""
		
		
		#e.delete(0, END)
		#e.insert(0, "a default value")

		self.button = Tk.Button(
		self.parametersFrame, text="Start", fg="red", command=self.start_darp
		)
		self.button.pack(side=Tk.BOTTOM)
		
		#self.cooksLabel.pack(side=Tk.TOP)
		#self.cooksEntry.pack(side=Tk.TOP)
		#self.clientsLabel.pack(side=Tk.TOP)
		#self.clientsEntry.pack(side=Tk.TOP)
		
		self.createMeals()
		self.createCars()
		
		
		self.canvas = Tk.Canvas(self.displayFrame, width=480, height=480)
		self.canvas.pack()
		
		self.drawGraph()

		#self.hi_there = Tk.Button(self.parametersFrame, text="Hello", command=self.say_hi)
		#self.parametersFrame.quit est la commande pour quitter

	def start_darp(self):
		try:
			cooks=int(self.cooksEntry.get())
			clients=int(self.clientsEntry.get())
			print("Lancement de l'algo avec",cooks,"cuisiniers et",clients,"clients")
			
			
			graphe=Graph.Graph(cooks,clients)
			#TODO : personalisation (endroit, type de repas etc.)
			depot = graphe.getDeliveryDepot() #TODO : multidepot
			
			print(len(self.carFrames),"voitures")
			
			allCars = []
			
			
			for i in range(len(self.carFrames)):
				currentFrame = self.carFrames[i]
				try:
					currentCapacity = int(currentFrame.CAPACITY.get())
					currentStarttime = int(currentFrame.STARTTIME.get())
					currentDuration = int(currentFrame.DURATION.get())
					print("La voiture ",i,"a un capacité de ",currentCapacity,
					", a une starttime de ",currentStarttime," et a une durée de shift de ",
					currentDuration)
					
					newCar = Car.Car(currentCapacity,currentStarttime,currentDuration,depot,graphe)
					allCars.append(newCar)
					
					
				except ValueError:
					print("Veuillez entrer un nombre valide pour la voiture",i)
					
			if(len(allCars) == len(self.carFrames)):
				darp = DarpAlgo.DarpAlgo(graphe.getMeals(),allCars)
			
				print("Starting DARP...")
				darp.createSchedules()
			
				print("The program has not crashed")
			
		except ValueError:
			print("Veuillez entrer un nombre valide")
		
	def createMeals(self):
		self.mealsFrames = []
		mealHeaderFrame = Tk.Frame(self.mealsFrame)
		mealHeaderFrame.pack(side=Tk.TOP,anchor="w")
		mealButton_PLUS = Tk.Button(mealHeaderFrame,text="+",fg="red",command=self.addMeal)
		mealButton_PLUS.pack(side=Tk.LEFT)
		label_DEPARTURE = Tk.Label(mealHeaderFrame,text="Departure")
		label_DEPARTURE.pack(side=Tk.LEFT)
		label_DEVIATION = Tk.Label(mealHeaderFrame,text="Deviation")
		label_DEVIATION.pack(side=Tk.LEFT)
		
	def addMeal(self):
		tempMealFrame=Tk.Frame(self.mealsFrame)
		self.mealsFrames.append(tempMealFrame)
		tempMealFrame.pack(side=Tk.TOP)
		
		tempMealFrame.DEPARTURE = Tk.StringVar()
		tempMealFrame.DEVIATION = Tk.StringVar()
		
		entry_DEPARTURE = Tk.Entry(tempMealFrame,textvariable=tempMealFrame.DEPARTURE,width=12)
		entry_DEPARTURE.pack(side=Tk.LEFT)
		entry_DEVIATION = Tk.Entry(tempMealFrame,textvariable=tempMealFrame.DEVIATION,width=12)
		entry_DEVIATION.pack(side=Tk.LEFT)
		
		def duplicateMeal():
			mymeal = self.addMeal()
			mymeal.DEPARTURE.set( tempMealFrame.DEPARTURE.get() )
			mymeal.DEVIATION.set( tempMealFrame.DEVIATION.get() )
		
		duplicateButton = Tk.Button(tempMealFrame,image=self.dupeImage,command=duplicateMeal)
		duplicateButton.pack(side=Tk.LEFT)
		
		def removeMeal(): 
			"""
			Must be inside this function because otherwise we don't have
			access to tempCarFrames since it's not an attribute and it 
			can't be an attribute because it must be a local variable.
			"""
			self.mealsFrames.remove(tempMealFrame)
			tempMealFrame.destroy()
		
		deleteCarButton = Tk.Button(tempMealFrame,text="X",fg="red",command=removeMeal)
		deleteCarButton.pack(side=Tk.LEFT)
		
		
		return tempMealFrame
			
	def createCars(self):
		self.carFrames = []
		carHeaderFrame = Tk.Frame(self.carsFrame)
		carHeaderFrame.pack(side=Tk.TOP,anchor="w",expand=True)
		carButton_PLUS = Tk.Button(carHeaderFrame,text="+",fg="red",command=self.addCar)
		carButton_PLUS.pack(side=Tk.LEFT)
		label_MAXCAPACITY = Tk.Label(carHeaderFrame,text="Capacity",width=10)
		label_MAXCAPACITY.pack(side=Tk.LEFT)
		label_STARTTIME = Tk.Label(carHeaderFrame,text="Start",width=10)
		label_STARTTIME.pack(side=Tk.LEFT)
		label_DURATION = Tk.Label(carHeaderFrame,text="Duration",width=10)
		label_DURATION.pack(side=Tk.LEFT)
		label_DUPE=Tk.Label(carHeaderFrame,width=3,text="")
		label_DUPE.pack(side=Tk.LEFT)
		label_DEL=Tk.Label(carHeaderFrame,width=3,text="")
		label_DEL.pack(side=Tk.LEFT)
		
		
	def addCar(self):
		"""Adds a car frame to the list and return the frame"""
		
		tempCarFrame=Tk.Frame(self.carsFrame)
		self.carFrames.append(tempCarFrame)
		tempCarFrame.pack(side=Tk.TOP)
		
		tempCarFrame.CAPACITY=Tk.StringVar()
		tempCarFrame.STARTTIME=Tk.StringVar()
		tempCarFrame.DURATION=Tk.StringVar()
		
		
		#carIcon = Tk.Button(tempCarFrame,text="",width=3)
		#carIcon.pack(side=Tk.LEFT)
		entry_MAXCAPACITY = Tk.Entry(tempCarFrame,textvariable=tempCarFrame.CAPACITY,width=12)
		entry_MAXCAPACITY.pack(side=Tk.LEFT)
		entry_STARTTIME = Tk.Entry(tempCarFrame,textvariable=tempCarFrame.STARTTIME,width=12)
		entry_STARTTIME.pack(side=Tk.LEFT)
		entry_DURATION = Tk.Entry(tempCarFrame,textvariable=tempCarFrame.DURATION,width=12)
		entry_DURATION.pack(side=Tk.LEFT)

		def duplicateCar():
			mycar = self.addCar()
			mycar.CAPACITY.set( tempCarFrame.CAPACITY.get() )
			mycar.STARTTIME.set( tempCarFrame.STARTTIME.get() )
			mycar.DURATION.set( tempCarFrame.DURATION.get() )
		
		duplicateButton = Tk.Button(tempCarFrame,image=self.dupeImage,command=duplicateCar)
		duplicateButton.pack(side=Tk.LEFT)
		
		def removeCar(): 
			"""
			Must be inside this function because otherwise we don't have
			access to tempCarFrames since it's not an attribute and it 
			can't be an attribute because it must be a local variable.
			"""
			self.carFrames.remove(tempCarFrame)
			tempCarFrame.destroy()
		
		deleteCarButton = Tk.Button(tempCarFrame,text="X",fg="red",command=removeCar)
		deleteCarButton.pack(side=Tk.LEFT)
		
		
		return tempCarFrame

	def drawGraph(self):
		canvas=self.canvas
		
		points = []
		
		nodesamount=5
		for i in range(nodesamount):
			points.append((randint(-100,100),randint(50,100)))
		
		minX = float("inf")
		minY = float("inf")
		maxX = -float("inf")
		maxY = -float("inf")
		
		
		for (x,y) in points:
			minX=min(minX,x)
			minY=min(minY,y)
			
			maxX=max(maxX,x)
			maxY=max(maxY,y)
			
		deltaX= maxX-minX
		deltaY= maxY-minY
		
		margin=25
		screensize=480-2*margin
		
		newpoints = []
		for (x,y) in points:
			newpoints.append(((x-minX)/deltaX*screensize+margin,(y-minY)/deltaY*screensize+margin))
		
		myNodes = []
		for j,(x,y) in enumerate(newpoints):
			myNodes.append(NodeDrawing(x,y,str(j),canvas))
			
		adjacenceMatrix= [[None]*nodesamount for i in range(nodesamount)]
			
		for i in range(nodesamount):
			for j in range(nodesamount):
				adjacenceMatrix[i][j]=randint(0,1)
		
		linesDrawer = NodeLines(canvas,newpoints,adjacenceMatrix)
		
root = Tk.Tk()

app = App(root)

root.mainloop()
try:
	root.destroy() #if it wasn't already
except:
	exit() #quit anyway

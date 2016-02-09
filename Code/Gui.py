# /usr/bin/env python 3
# -*- coding: utf-8 -*-
import DarpAlgo
import Car
import Graph
import Meal
import Node
import os

try:
	import Tkinter as Tk
except ImportError:
	import tkinter as Tk

class App:

	def __init__(self, master):
		
		mainFrame = Tk.Frame(master)
		mainFrame.pack()
		
		self.parametersFrame = Tk.Frame(mainFrame)
		self.parametersFrame.pack(side=Tk.RIGHT)
		
		self.displayFrame = Tk.Frame(mainFrame)
		self.displayFrame.pack(side=Tk.LEFT)
		
		self.cooksEntry = Tk.Entry(self.parametersFrame)
		self.clientsEntry = Tk.Entry(self.parametersFrame)	
		self.cooksLabel = Tk.Label(self.parametersFrame,text="Amount of Cooks")
		self.clientsLabel = Tk.Label(self.parametersFrame,text="Amount of Clients")

		#e.delete(0, END)
		#e.insert(0, "a default value")

		self.button = Tk.Button(
		self.parametersFrame, text="Start", fg="red", command=self.start_darp
		)
		self.button.pack(side=Tk.BOTTOM)
		
		self.cooksLabel.pack(side=Tk.TOP)
		self.cooksEntry.pack(side=Tk.TOP)
		self.clientsLabel.pack(side=Tk.TOP)
		self.clientsEntry.pack(side=Tk.TOP)
		self.createCars()
		
		
		self.canvas = Tk.Canvas(self.displayFrame, width=480, height=480)
		self.canvas.pack()
		self.canvas.create_line(0, 0, 480, 480)

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
		
			
	def createCars(self):
		self.carFrames = []
		carHeaderFrame = Tk.Frame(self.parametersFrame)
		carHeaderFrame.pack(side=Tk.TOP)
		self.button_PLUS = Tk.Button(carHeaderFrame,text="+",fg="red",command=self.addCar)
		self.button_PLUS.pack(side=Tk.LEFT)
		self.label_MAXCAPACITY = Tk.Label(carHeaderFrame,text="Capacity",width=10)
		self.label_MAXCAPACITY.pack(side=Tk.LEFT)
		self.label_STARTTIME = Tk.Label(carHeaderFrame,text="Start",width=10)
		self.label_STARTTIME.pack(side=Tk.LEFT)
		self.label_DURATION = Tk.Label(carHeaderFrame,text="Duration",width=10)
		self.label_DURATION.pack(side=Tk.LEFT)
		self.label_DUPE=Tk.Label(carHeaderFrame,width=3,text="")
		self.label_DUPE.pack(side=Tk.LEFT)
		self.label_DEL=Tk.Label(carHeaderFrame,width=3,text="")
		self.label_DEL.pack(side=Tk.LEFT)
		
		
		self.dupeImage = Tk.PhotoImage(file=os.path.join("GUIELEM","duplicate.gif"))
		self.addCar() #au moins une voiture?
		
	def addCar(self):
		"""Adds a car frame to the list and return the frame"""
		
		tempCarFrame=Tk.Frame(self.parametersFrame)
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
			if(len(self.carFrames)>1):
				self.carFrames.remove(tempCarFrame)
				tempCarFrame.destroy()
		
		deleteCarButton = Tk.Button(tempCarFrame,text="X",fg="red",command=removeCar)
		deleteCarButton.pack(side=Tk.LEFT)
		
		
		return tempCarFrame
		
		
root = Tk.Tk()

app = App(root)

root.mainloop()
try:
	root.destroy() #if it wasn't already
except:
	exit() #quit anyway
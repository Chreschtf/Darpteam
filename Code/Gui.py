# /usr/bin/env python 3
# -*- coding: utf-8 -*-
import DarpAlgo
import Car
import Graph
import Meal
import Node
import os
import GraphDrawer
from random import randint
from random import choice
import DataFileWriter
import DataFileParser

#TODO Ajouter les cars et les meals et les mettre à jour quand on load un file.
#Mettre à jour la valeur maximale des spinbox (depot, meals.cook, meals.client) quand le graphe change de taille (après un load/après un generate)


try:
	import Tkinter as Tk
except ImportError:
	import tkinter as Tk

from tkinter import messagebox

try:
	from tkinter.filedialog import askopenfilename #python 3
except ImportError:
	from Tkinter.filedialog import askopenfilename #ne fonctionne pas en python 2




class App:
	def timestring_to_minutes(self,tstring):
		x=tstring.split(":")
		return int(x[0])*60+int(x[1])
		
		
	def minutes_to_timestring(self,minutes):
		return str(int(minutes/60)).zfill(2)+":"+str(int(minutes%60)).zfill(2)

	def is_amountstring_ok(self,astring):	
		try:
			return(int(astring)>=0)
		except ValueError:
			return False
			
	def is_time_ok(self,hours,minutes,timestart=0):
		return (0<=hours<24 and 0<=minutes<60 and timestart<=hours*60+minutes)
		
	def is_timestring_ok(self,tstring,tstart=0):
		try:
			h,m=tstring.split(":")
			return self.is_time_ok(int(h),int(m),tstart)
		except ValueError:
			return False
	
	def is_node_ok(self,nodeNumber):
		return self.graph!=None and (0<=nodeNumber<len(self.graph.getSortedNodes()))
			
	def is_nodestring_ok(self,nstring):
		try:
			return self.is_node_ok(int(nstring))
		except ValueError:
			return False
			
	def nodestring_to_node(self,nstring):
		if(self.is_nodestring_ok(nstring)):
			return  self.graph.getSortedNodes()[int(nstring)]
		else:
			raise ValueError("No such node")
			
			
	def checkNode(self,event):
		if(self.is_nodestring_ok(event.widget.get())):
			event.widget.configure(bg = "#F0F0ED")
		else:
			event.widget.configure(bg = "#ff6666")

	def checkValue(self,event):
		if(self.is_amountstring_ok(event.widget.get())):
			event.widget.configure(bg = "#F0F0ED")
		else:
			event.widget.configure(bg = "#ff6666")

	def checkHour(self,event):
		splitdata=event.widget.get().split(":")
		"""if(len(splitdata)==1):
			splitdata.append("00")
			aa=event.widget.cget("textvariable")
			print(aa,repr(aa))
			event.widget.delete(0, Tk.END)
			event.widget.insert(0, ":".join(splitdata))
			#event.widget.winfo_parent()
			#print(aa.get())
			#event.widget.cget("textvariable").set(":".join(splitdata))
		"""
					
		if(self.is_timestring_ok(event.widget.get())):
			event.widget.configure(bg = "#F0F0ED")
		else:
			event.widget.configure(bg = "#ff6666")
			
	def __init__(self, master):
		self.graph = None
		self.guiGraph = None
		
		
		self.hoursInDay = [str(h).zfill(2)+":"+str(m).zfill(2) for h in range(24) for m in range(60)]
		
		#MAINFRAME
		mainFrame = Tk.Frame(master)
		mainFrame.pack(fill=Tk.BOTH,expand=True)
		
		#PARAMETERS FRAME on the right    self.parametersFrame
		self.parametersFrame = Tk.Frame(mainFrame,bg="pink")
		self.parametersFrame.pack(side=Tk.RIGHT,anchor="n",fill=Tk.BOTH)
		
		
		
		self.nodesFrame = Tk.Frame(self.parametersFrame)
		self.nodesFrame.pack(side=Tk.TOP,anchor="nw")
		
		
		self.nodesLabel = Tk.Label(self.nodesFrame,text="Amount of Nodes: ")
		#self.nodesEntry = Tk.Entry(self.nodesFrame,width=4)
		self.nodesAmount = Tk.StringVar()
		
		self.nodesEntry = Tk.Spinbox(self.nodesFrame, from_=3, to=150, width=4,textvariable=self.nodesAmount)
		self.nodesButton = Tk.Button(self.nodesFrame, text="Generate",command = self.generateGraph)
		self.nodesAmount.set(15)
		
		self.nodesLabel.pack(side=Tk.LEFT,anchor="w")
		self.nodesEntry.pack(side=Tk.LEFT,anchor="w")
		self.nodesButton.pack(side=Tk.LEFT,anchor="w")
		
		self.depotFrame = Tk.Frame(self.parametersFrame)
		self.depotFrame.pack(side=Tk.TOP,anchor="nw")
		

				
		
		self.depotLabel = Tk.Label(self.depotFrame,text="Depot node: ")
		#self.depotEntry = Tk.Entry(self.depotFrame,width=4)
		self.depotValue = Tk.StringVar()
		
		self.depotEntry = Tk.Spinbox(self.depotFrame, from_=0, to=150, width=4, textvariable=self.depotValue)
		
		self.depotValue.set(0)
		
		self.depotLabel.pack(side=Tk.LEFT,anchor="w")
		self.depotEntry.pack(side=Tk.LEFT,anchor="w")
		self.depotEntry.bind("<FocusOut>",self.checkNode)
		self.depotEntry.bind("<KeyRelease>",self.checkNode)
		
		self.mealsLabel = Tk.Label(self.parametersFrame,text="Meals:")
		self.mealsFrame = Tk.Frame(self.parametersFrame)
		self.mealsLabel.pack(side=Tk.TOP,anchor="nw")
		self.mealsFrame.pack(side=Tk.TOP,anchor="nw",fill=Tk.X)
		
		self.carsLabel = Tk.Label(self.parametersFrame,text="Cars:")
		self.carsFrame = Tk.Frame(self.parametersFrame)
		self.carsLabel.pack(side=Tk.TOP,anchor="nw")
		self.carsFrame.pack(side=Tk.TOP,anchor="nw",fill=Tk.X)
		
		
		
		
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
		
		

		self.parserFrame = Tk.Frame(self.parametersFrame)
		self.parserFrame.pack(side=Tk.BOTTOM,fill=Tk.X)
		
		self.exportButton = Tk.Button(self.parserFrame, text="Export as", command = self.export_data#command = 
		)
		self.exportButton.pack(side=Tk.LEFT)
		
		self.exportEntry = Tk.Entry(self.parserFrame)
		
		self.exportEntry.delete(0, Tk.END)
		self.exportEntry.insert(0, "FilenameTest")
		
		self.exportEntry.pack(side=Tk.LEFT,anchor="e",fill=Tk.X)
		
		self.loadButton = Tk.Button(self.parserFrame, text="Load",command = self.import_data)
		self.loadButton.pack(side=Tk.RIGHT)
		
		#self.cooksLabel.pack(side=Tk.TOP)
		#self.cooksEntry.pack(side=Tk.TOP)
		#self.clientsLabel.pack(side=Tk.TOP)
		#self.clientsEntry.pack(side=Tk.TOP)
		
		self.createMeals()
		self.createCars()
		
		
		self.canvas = Tk.Canvas(self.displayFrame, width=480, height=480)
		self.canvas.pack()
	
	
	
		self.button = Tk.Button(
		self.parametersFrame, text="Start DARP", fg="red", command=self.start_darp
		)
		self.button.pack(side=Tk.BOTTOM,anchor="w")
		
		
		#self.displayGraph()

		#self.hi_there = Tk.Button(self.parametersFrame, text="Hello", command=self.say_hi)
		#self.parametersFrame.quit est la commande pour quitter
		

	def start_darp(self):
		if(self.graph==None):
			Tk.messagebox.showwarning("DARP resolution","Veuillez générer un graphe")
			return
		
		try:
			#cooks=int(self.cooksEntry.get())
			#clients=int(self.clientsEntry.get())
			#print("Lancement de l'algo avec",cooks,"cuisiniers et",clients,"clients")
			canStart=True
			errorMessage=""
			
			#print(len(self.graph.getSortedNodes()),"noeuds,",len(self.carFrames),"voitures",len(self.mealsFrames),"livraisons")
			
			allCars = []
			allMeals = []
			
			for i,mealFrame in enumerate(self.mealsFrames):
				try:
					currentDelivery=self.timestring_to_minutes(mealFrame.DELIVERY.get())
					currentDeviation=int(mealFrame.DEVIATION.get())
					currentCook=int(mealFrame.COOK.get())
					currentClient=int(mealFrame.CLIENT.get())
					
					
					
					
					cookNode=self.graph.getSortedNodes()[currentCook]
					clientNode=self.graph.getSortedNodes()[currentClient]
					
					distanceNodes=self.graph.dist(cookNode,clientNode)
					
					newMeal=Meal.Meal(cookNode,clientNode,distanceNodes,currentDelivery,currentDeviation)
					allMeals.append(newMeal)
				except:
					errorMessage+="\nVeuillez entrer un nombre valide pour le repas"+str(i)
					canStart=False
					
			allMeals.sort(key=lambda obj: obj.ddt)
			
			for i in range(len(self.carFrames)):
				currentFrame = self.carFrames[i]
				try:
					currentCapacity = int(currentFrame.CAPACITY.get())
					currentStarttime = self.timestring_to_minutes(currentFrame.STARTTIME.get())
					currentDuration = int(currentFrame.DURATION.get())
					currentDepot = self.graph.getSortedNodes()[int(self.depotValue.get())]
					print("La voiture ",i,"a un capacité de ",currentCapacity,
					", a une starttime de ",currentStarttime," et a une durée de shift de ",
					currentDuration)
					
					newCar = Car.Car(currentCapacity,currentStarttime,currentDuration,currentDepot,self.graph)
					allCars.append(newCar)
					
					
				except ValueError:
					errorMessage+="\nVeuillez entrer un nombre valide pour la voiture"+str(i)
					canStart=False
					
			if(canStart):
				darp = DarpAlgo.DarpAlgo(allMeals,allCars)
			
				print("Starting DARP...")
				darp.createSchedules()
				for i,car in enumerate(allCars):
					print("Car numéro",i)
					for block in car.currentSchedule:
						print(block)
					print("\n")
					
				print("The program has not crashed")
			
		except ValueError:
			print("Veuillez entrer un nombre valide")

		
		if not canStart:
			Tk.messagebox.showwarning("DARP resolution",errorMessage)
			
		
	def export_data(self):
		
		if self.verifyEntries():			
			filename = self.exportEntry.get()
			
			cars=[] #maxcap, starttime, duration
			for carFrame in self.carFrames:
				cars.append((carFrame.CAPACITY.get(),carFrame.STARTTIME.get(),carFrame.DURATION.get()))
			
			meals=[] #dtt, deviation, chef,client
			for mealFrame in self.mealsFrames:
				meals.append((mealFrame.DELIVERY.get(),mealFrame.DEVIATION.get(),mealFrame.COOK.get(),mealFrame.CLIENT.get()))
				
			nodes=[] #id, i,j , neighbours
			for node in self.graph.getSortedNodes():
				neighbours = ""
				for neighbour in node.neighbours:
					neighbours+="|"+str(neighbour.index)
				nodes.append( (str(node.index), str(node.i), str(node.j), neighbours[1:])  )
			
			
			depot=self.depotValue.get()
			depots = [(depot)]
			
			Tk.messagebox.showwarning("Exporting as "+filename,"Exported:\n"+"\n".join(
				("Cars:"+str(cars),"Meals:"+str(meals),"Nodes:"+str(nodes),"Depots:"+str(depots))))
			
			
			DFW = DataFileWriter.DataFileWriter(filename, cars, meals, nodes, depots)
			DFW.writeXML_File()
			
			#DFP = DataFileParser(DFW.filename)
			#DFP.parseXML_File()
		else:
			print("error")
	def import_data(self):
		#filename = self.exportEntry.get()
		filename = askopenfilename(initialdir="../DataFiles")
		DFP = DataFileParser.DataFileParser(filename)
		DFP.parseXML_File()
		# TODO : give Data to Algo ?
		self.updateFromLoad(DFP)

	def updateFromLoad(self,dataFileParser):
		
		self.graph = dataFileParser.getGraph()
		self.displayGraph(self.graph)
		
		for mealFrame in self.mealsFrames:
			mealFrame.destroy()
		self.mealsFrames=[]
		
		for carFrame in self.carFrames:
			carFrame.destroy()
		self.carFrames=[]
		
		for car in dataFileParser.getCars():
			carFrame=self.addCar()
			carFrame.CAPACITY.set(str(car.maxCharge))
			carFrame.STARTTIME.set(self.minutes_to_timestring(int(car.start)))
			carFrame.DURATION.set(str(int(car.end)-int(car.start)))
			
			callFocusOut(carFrame)
			
		for meal in dataFileParser.getMeals():
			mealFrame=self.addMeal()
			
			mealFrame.COOK.set(str(meal.chef.index))
			mealFrame.CLIENT.set(str(meal.destination.index))
			mealFrame.DEVIATION.set(str(meal.deviation))
			mealFrame.DELIVERY.set(self.minutes_to_timestring(int(meal.ddt)))
			
			callFocusOut(mealFrame)
			
			
		self.depotValue.set(str(dataFileParser.getDepots()[0].index)) #multiple dépôts? ...
		self.nodesAmount.set(str(len(self.graph.getSortedNodes())))
		#TODO nodesamount
			
		
		
	def createMeals(self):
		self.mealsFrames = []
		mealHeaderFrame = Tk.Frame(self.mealsFrame)
		mealHeaderFrame.pack(side=Tk.TOP,anchor="w",fill=Tk.X)
		
		
	
		
		label_COOK = Tk.Label(mealHeaderFrame,text="Cook",width=6)
		label_COOK.pack(side=Tk.LEFT)
		label_CLIENT = Tk.Label(mealHeaderFrame,text="Client",width=6)
		label_CLIENT.pack(side=Tk.LEFT)
		
		label_DEVIATION = Tk.Label(mealHeaderFrame,text="Deviation",width=9)
		label_DEVIATION.pack(side=Tk.LEFT)
		label_DELIVERY = Tk.Label(mealHeaderFrame,text="Delivery",width=9)
		label_DELIVERY.pack(side=Tk.LEFT)
		
		empty_label = Tk.Label(mealHeaderFrame,width=4)
		empty_label.pack(side=Tk.LEFT)
		
		mealButton_PLUS = Tk.Button(mealHeaderFrame,text="+",fg="red",command=self.addMeal)
		mealButton_PLUS.pack(side=Tk.RIGHT)
		
	def addMeal(self):
		if(self.graph==None):
			Tk.messagebox.showwarning("Add meal","Please generate a graph first")
			return
		tempMealFrame=Tk.Frame(self.mealsFrame)
		self.mealsFrames.append(tempMealFrame)
		tempMealFrame.pack(side=Tk.TOP,fill=Tk.X)
		
		tempMealFrame.DEVIATION = Tk.StringVar()
		tempMealFrame.DELIVERY = Tk.StringVar()
		
		tempMealFrame.COOK = Tk.StringVar()
		tempMealFrame.CLIENT = Tk.StringVar()
		
		

		
		#entry_COOK = Tk.Spinbox(tempMealFrame, from_=0, to=len(self.graph.getSortedNodes())-1, textvariable=tempMealFrame.COOK, width=6)
		entry_COOK = Tk.Spinbox(tempMealFrame, from_=0, to=150, textvariable=tempMealFrame.COOK, width=5)
		tempMealFrame.COOK.set(len(self.graph.getSortedNodes())-1)
		entry_COOK.pack(side=Tk.LEFT)
		entry_COOK.bind("<FocusOut>",self.checkNode)
		entry_COOK.bind("<KeyRelease>",self.checkNode)
		#entry_CLIENT = Tk.Entry(tempMealFrame,textvariable=tempMealFrame.CLIENT,width=6)
		entry_CLIENT = Tk.Spinbox(tempMealFrame, from_=0, to=150, textvariable=tempMealFrame.CLIENT, width=5)
		tempMealFrame.CLIENT.set(int(len(self.graph.getSortedNodes())/2))
		entry_CLIENT.pack(side=Tk.LEFT)
		entry_CLIENT.bind("<FocusOut>",self.checkNode)
		entry_CLIENT.bind("<KeyRelease>",self.checkNode)
		
		#entry_DEVIATION = Tk.Entry(tempMealFrame,textvariable=tempMealFrame.DEVIATION,width=9)
		entry_DEVIATION = Tk.Spinbox(tempMealFrame, from_=0, to=100, textvariable=tempMealFrame.DEVIATION, width=8)
		entry_DEVIATION.pack(side=Tk.LEFT) # TODO: realTime
		entry_DEVIATION.bind("<FocusOut>",self.checkValue)
		entry_DEVIATION.bind("<KeyRelease>",self.checkValue)
		
		entry_DELIVERY = Tk.Spinbox(tempMealFrame, values=self.hoursInDay, textvariable=tempMealFrame.DELIVERY, width=8)
		entry_DELIVERY.pack(side=Tk.LEFT) # TODO: realTime
		entry_DELIVERY.bind("<FocusOut>",self.checkHour)
		entry_DELIVERY.bind("<KeyRelease>",self.checkHour)
		
		
		def removeMeal(): 
			"""
			Must be inside this function because otherwise we don't have
			access to tempCarFrames since it's not an attribute and it 
			can't be an attribute because it must be a local variable.
			"""
			self.mealsFrames.remove(tempMealFrame)
			tempMealFrame.destroy()
		
		deleteCarButton = Tk.Button(tempMealFrame,text="X",fg="red",command=removeMeal)
		deleteCarButton.pack(side=Tk.RIGHT)
		
		def duplicateMeal():
			mymeal = self.addMeal()
			
			mymeal.COOK.set( tempMealFrame.COOK.get() )
			mymeal.CLIENT.set( tempMealFrame.CLIENT.get() )
			mymeal.DEVIATION.set( tempMealFrame.DEVIATION.get() )
			mymeal.DELIVERY.set( tempMealFrame.DELIVERY.get() )
			
			
			callFocusOut(mymeal)
		
		duplicateButton = Tk.Button(tempMealFrame,image=self.dupeImage,command=duplicateMeal)
		duplicateButton.pack(side=Tk.RIGHT)
		
		
		
		return tempMealFrame
			
	def createCars(self):
		self.carFrames = []
		carHeaderFrame = Tk.Frame(self.carsFrame)
		carHeaderFrame.pack(side=Tk.TOP,anchor="w",fill=Tk.X)
		
		label_MAXCAPACITY = Tk.Label(carHeaderFrame,text="Capacity",width=10)
		label_MAXCAPACITY.pack(side=Tk.LEFT)
		label_STARTTIME = Tk.Label(carHeaderFrame,text="Start",width=10)
		label_STARTTIME.pack(side=Tk.LEFT)
		label_DURATION = Tk.Label(carHeaderFrame,text="Duration",width=10)
		label_DURATION.pack(side=Tk.LEFT)
		"""label_DUPE=Tk.Label(carHeaderFrame,width=3,text="")
		label_DUPE.pack(side=Tk.LEFT)
		label_DEL=Tk.Label(carHeaderFrame,width=3,text="")
		label_DEL.pack(side=Tk.LEFT)"""
		
		carButton_PLUS = Tk.Button(carHeaderFrame,text="+",fg="red",command=self.addCar)
		carButton_PLUS.pack(side=Tk.RIGHT)
				
	def addCar(self):
		"""Adds a car frame to the list and return the frame"""
		
		tempCarFrame=Tk.Frame(self.carsFrame)
		self.carFrames.append(tempCarFrame)
		tempCarFrame.pack(side=Tk.TOP,fill=Tk.X)
		
		tempCarFrame.CAPACITY=Tk.StringVar()
		tempCarFrame.STARTTIME=Tk.StringVar()
		tempCarFrame.DURATION=Tk.StringVar()
		
		
		
		#carIcon = Tk.Button(tempCarFrame,text="",width=3)
		#carIcon.pack(side=Tk.LEFT)
		#entry_MAXCAPACITY = Tk.Entry(tempCarFrame,textvariable=tempCarFrame.CAPACITY,width=10)
		entry_MAXCAPACITY = Tk.Spinbox(tempCarFrame, from_=1, to=250, textvariable=tempCarFrame.CAPACITY,width=9)
		entry_MAXCAPACITY.pack(side=Tk.LEFT)
		entry_MAXCAPACITY.bind("<FocusOut>",self.checkValue)
		entry_MAXCAPACITY.bind("<KeyRelease>",self.checkValue)
		#entry_STARTTIME = Tk.Entry(tempCarFrame,textvariable=tempCarFrame.STARTTIME,width=10)
		entry_STARTTIME = Tk.Spinbox(tempCarFrame, values=self.hoursInDay , textvariable=tempCarFrame.STARTTIME,width=9)
		entry_STARTTIME.pack(side=Tk.LEFT) # TODO : real time
		entry_STARTTIME.bind("<FocusOut>",self.checkHour)
		entry_STARTTIME.bind("<KeyRelease>",self.checkHour)
		#entry_STARTTIME.bind("<KeyRelease>",checkValue)
		#entry_DURATION = Tk.Entry(tempCarFrame,textvariable=tempCarFrame.DURATION,width=10)
		entry_DURATION = Tk.Spinbox(tempCarFrame, from_=0, to=100, textvariable=tempCarFrame.DURATION,width=9)
		entry_DURATION.pack(side=Tk.LEFT)
		entry_DURATION.bind("<FocusOut>",self.checkValue)
		entry_DURATION.bind("<KeyRelease>",self.checkValue)


		tempCarFrame.STARTTIME.set("8:00")
		tempCarFrame.CAPACITY.set("5")
		tempCarFrame.DURATION.set(8*60)
		

		def removeCar(): 
			"""
			Must be inside this function because otherwise we don't have
			access to tempCarFrames since it's not an attribute and it 
			can't be an attribute because it must be a local variable.
			"""
			self.carFrames.remove(tempCarFrame)
			tempCarFrame.destroy()
		
		deleteCarButton = Tk.Button(tempCarFrame,text="X",fg="red",command=removeCar)
		deleteCarButton.pack(side=Tk.RIGHT)

		def duplicateCar():
			mycar = self.addCar()
			mycar.CAPACITY.set( tempCarFrame.CAPACITY.get() )
			mycar.STARTTIME.set( tempCarFrame.STARTTIME.get() )
			mycar.DURATION.set( tempCarFrame.DURATION.get() )
			
			callFocusOut(mycar)
		
		duplicateButton = Tk.Button(tempCarFrame,image=self.dupeImage,command=duplicateCar)
		duplicateButton.pack(side=Tk.RIGHT)
		
		
		
		return tempCarFrame
		
	def generateGraph(self):
		try:
			nodesAmount=int(self.nodesAmount.get())
			self.graph=Graph.Graph(nodesAmount)
			#TODO : personalisation (endroit, type de repas etc.)
			self.depot = self.graph.getSortedNodes()[0] #TODO : multidepot
			
			self.displayGraph(self.graph)
		except ValueError:
			print("Veuillez entrer une valeur")

	def displayGraph(self,graph):
		if(self.guiGraph!=None):
			self.guiGraph.__init__(self.canvas)
		self.guiGraph = GUIGraph(self.canvas)
		self.guiGraph.generateGraph(graph)
		self.guiGraph.drawGraph()
	
	def verifyEntries(self):
		#gérer les float ? 0.5 capacity?
		for index,carFrame in enumerate(self.carFrames):	
			#if int(carFrame.CAPACITY.get()) < 0 or int(carFrame.STARTTIME.get()) < 0 or int(carFrame.DURATION.get()) < 0:
			if not(self.is_amountstring_ok(carFrame.CAPACITY.get())
			and self.is_timestring_ok(carFrame.STARTTIME.get())
			and self.is_amountstring_ok(carFrame.DURATION.get())):
				Tk.messagebox.showwarning("DARP export","Cannot export: Bad CAR values for car "+str(index))
				return False
		for index,mealFrame in enumerate(self.mealsFrames):
			#if (int(mealFrame.DELIVERY.get()) < 0 or int(mealFrame.DEVIATION.get()) < 0 or not(0 <= int(mealFrame.COOK.get()) < len(self.graph.getSortedNodes())) or not(0 <= int(mealFrame.CLIENT.get()) < len(self.graph.getSortedNodes()))):
			if not(self.is_timestring_ok(mealFrame.DELIVERY.get())
			and self.is_amountstring_ok(mealFrame.DEVIATION.get())
			and self.is_nodestring_ok(mealFrame.COOK.get())
			and self.is_nodestring_ok(mealFrame.CLIENT.get())):
				Tk.messagebox.showwarning("DARP export","Cannot export: Bad MEAL values for meal "+str(index))
				return False
		#if not(0 <= int(self.depotValue.get()) < len(self.graph.getSortedNodes())):
		if not(self.is_nodestring_ok(self.depotValue.get())):
			Tk.messagebox.showwarning("DARP export","Cannot export: bad DEPOT NODE value")
			return False
		return True
			
def callFocusOut(parent):
	#set the focus on the childrens of a frame
	#the focus is lost, calling FocusOut (recoloring our widgets)
	for widget in parent.winfo_children():
		widget.focus_set()
		
class GUIGraph:
	def __init__(self,canvas):
		#self.nodesAmount = 20
		self.canvas = canvas
		self.realNodes = []
		self.positionsInGraph = []
		self.canvasNodes = []
		self.margin = 25
		
		self.mouseDelta = (None,None)
		self.currentNode=None
		
		self.canvas.bind("<ButtonPress-1>", self.clickObject)
		self.canvas.bind("<B1-Motion>", self.moveObject)
		self.canvas.bind("<ButtonRelease-1>", self.releaseObject)
		
	
	def generateGraph(self,graph):
		self.canvas.delete(Tk.ALL)
		self.graph=graph
		self.nodesAmount=len(graph.getSortedNodes())
		
		self.nodes=graph.getSortedNodes()
		
		#for i in range(self.nodesAmount):
		#	self.nodes.append((randint(-100,100),randint(50,100)))
		
		self.minX = float("inf")
		self.minY = float("inf")
		self.maxX = -float("inf")
		self.maxY = -float("inf")
		
		for node in self.nodes:
			#prendre les valeurs min et max pour l'échelle
			x,y = node.i,node.j
			self.minX=min(self.minX,x)
			self.minY=min(self.minY,y)
			
			self.maxX=max(self.maxX,x)
			self.maxY=max(self.maxY,y)
			
		self.deltaX= self.maxX-self.minX
		self.deltaY= self.maxY-self.minY

		self.screensize=int(self.canvas.cget("width"))-2*self.margin
		
		for node in self.nodes:
			#convertir les positions des nodes en nouvelles positions
			x,y = node.i,node.j
			self.positionsInGraph.append(((x-self.minX)/self.deltaX*self.screensize+self.margin,(y-self.minY)/self.deltaY*self.screensize+self.margin))
			
	def drawGraph(self):	
			
		#adjacenceMatrix= [[None]*self.nodesAmount for i in range(self.nodesAmount)]
		#for i in range(self.nodesAmount):
		#	for j in range(self.nodesAmount):
		#		adjacenceMatrix[i][j]=choice([0,0,0,0,0,1])
		
		adjacenceMatrix=self.graph.getAdjMatrix()
		
		
		
		for j,(x,y) in enumerate(self.positionsInGraph):
			self.canvasNodes.append(GraphDrawer.NodeDrawing(x,y,str(j),self.canvas,self.nodes[j],self.margin))
			
			
		#self.linesDrawer = NodeLines(self.canvas,self.canvasNodes,adjacenceMatrix)
		GraphDrawer.generateLines(self.canvas,self.canvasNodes,adjacenceMatrix)
		
		for drawNode in self.canvasNodes:
			drawNode.generateDrawing()
	
	def clickObject(self,event):
		#self.coords = event.x,event.y
		self.currentObject = event.widget.find_withtag("current")
		
		if(len(self.currentObject)!=0):
			drawnClickedObject = self.currentObject[0]
			
			for node in self.canvasNodes:
				if node.isMine(drawnClickedObject):
					self.mouseDelta = node.x-event.x, node.y-event.y
					break
					
	def moveObject(self,event):
		if(len(self.currentObject)!=0):
			drawnClickedObject = self.currentObject[0]
			
			for node in self.canvasNodes:
				if node.isMine(drawnClickedObject):
					node.move(event.x+self.mouseDelta[0],event.y+self.mouseDelta[1])
					break
			#clickedNode = drawnClickedObject.parent
		#self.linesDrawer.drawLines() #lines are self-updating now
			
	def releaseObject(self,event):
		pass	
		
		
	
root = Tk.Tk()

app = App(root)

root.mainloop()
try:
	root.destroy() #if it wasn't already
except:
	exit() #quit anyway

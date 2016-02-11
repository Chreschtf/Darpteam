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


try:
	import Tkinter as Tk
except ImportError:
	import tkinter as Tk

class App:

	def __init__(self, master):
		self.graph = None
		self.guiGraph = None
		
		#MAINFRAME
		mainFrame = Tk.Frame(master)
		mainFrame.pack(fill=Tk.BOTH,expand=True)
		
		#PARAMETERS FRAME on the right    self.parametersFrame
		self.parametersFrame = Tk.Frame(mainFrame,bg="pink")
		self.parametersFrame.pack(side=Tk.RIGHT,anchor="n",expand=True,fill=Tk.BOTH)
		
		
		
		self.nodesFrame = Tk.Frame(self.parametersFrame)
		self.nodesFrame.pack(side=Tk.TOP,anchor="nw")
		
		
		self.nodesLabel = Tk.Label(self.nodesFrame,text="Amount of Nodes")
		self.nodesEntry = Tk.Entry(self.nodesFrame)
		self.nodesButton = Tk.Button(self.nodesFrame, text="Generate",command = self.generateGraph)
		
		self.nodesLabel.pack(side=Tk.LEFT,anchor="nw")
		self.nodesEntry.pack(side=Tk.LEFT,anchor="nw")
		self.nodesButton.pack(side=Tk.LEFT,anchor="nw")
		
		self.mealsLabel = Tk.Label(self.parametersFrame,text="Meals:")
		self.mealsFrame = Tk.Frame(self.parametersFrame)
		self.mealsLabel.pack(side=Tk.TOP,anchor="nw")
		self.mealsFrame.pack(side=Tk.TOP,anchor="nw")
		self.carsLabel = Tk.Label(self.parametersFrame,text="Cars:")
		self.carsFrame = Tk.Frame(self.parametersFrame)
		self.carsLabel.pack(side=Tk.TOP,anchor="nw")
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
		self.button.pack(side=Tk.LEFT,anchor="s")
		
		self.exportButton = Tk.Button(self.parametersFrame, text="Export as", command = self.export_data#command = 
		)
		self.exportButton.pack(side=Tk.LEFT,anchor="s")
		
		self.exportEntry = Tk.Entry(self.parametersFrame)
		
		self.exportEntry.delete(0, Tk.END)
		self.exportEntry.insert(0, "FilenameTest")
		
		self.exportEntry.pack(side=Tk.LEFT,anchor="s")
		
		self.loadButton = Tk.Button(self.parametersFrame, text="Load",command = self.import_data)
		self.loadButton.pack(side=Tk.LEFT,anchor="s")
		
		#self.cooksLabel.pack(side=Tk.TOP)
		#self.cooksEntry.pack(side=Tk.TOP)
		#self.clientsLabel.pack(side=Tk.TOP)
		#self.clientsEntry.pack(side=Tk.TOP)
		
		self.createMeals()
		self.createCars()
		
		
		self.canvas = Tk.Canvas(self.displayFrame, width=480, height=480)
		self.canvas.pack()
	
		
		#self.displayGraph()

		#self.hi_there = Tk.Button(self.parametersFrame, text="Hello", command=self.say_hi)
		#self.parametersFrame.quit est la commande pour quitter
		

	def start_darp(self):
		try:
			#cooks=int(self.cooksEntry.get())
			#clients=int(self.clientsEntry.get())
			#print("Lancement de l'algo avec",cooks,"cuisiniers et",clients,"clients")
			
			
			print(nodesAmount,"noeuds,",len(self.carFrames),"voitures")
			
			allCars = []
			allMeals = []
			
			
			for i in range(len(self.carFrames)):
				currentFrame = self.carFrames[i]
				try:
					currentCapacity = int(currentFrame.CAPACITY.get())
					currentStarttime = int(currentFrame.STARTTIME.get())
					currentDuration = int(currentFrame.DURATION.get())
					print("La voiture ",i,"a un capacité de ",currentCapacity,
					", a une starttime de ",currentStarttime," et a une durée de shift de ",
					currentDuration)
					
					newCar = Car.Car(currentCapacity,currentStarttime,currentDuration,self.depot,self.graph)
					allCars.append(newCar)
					
					
				except ValueError:
					print("Veuillez entrer un nombre valide pour la voiture",i)
					
			if(len(allCars) == len(self.carFrames)):
				darp = DarpAlgo.DarpAlgo(allMeals,allCars)
			
				print("Starting DARP...")
				darp.createSchedules()
			
				print("The program has not crashed")
			
		except ValueError:
			print("Veuillez entrer un nombre valide")
			
			
			
		
	def export_data(self):
		filename = self.exportEntry.get()
		print("Code here to export to",filename)
		
		
		
		cars=[]
		for carFrame in self.carFrames:
			cars.append((carFrame.CAPACITY.get(),carFrame.STARTTIME.get(),carFrame.DURATION.get()))
		
		"""
		self.mealsFrames.append(tempMealFrame)
		
		tempMealFrame.DEPARTURE = Tk.StringVar()
		tempMealFrame.DEVIATION = Tk.StringVar()"""
		
		"""
		meals = [("2","3","0","1"), ("8", "7", "0", "2")]
		nodes = [("0", "1", "2", "1|2"), ("1", "4", "2", "0"), ("2", "0", "3", "0")]
		depots = [("1")]
		
		DFW = DataFileWriter(filename, cars, meals, nodes, depots)
		DFW.writeXML_File()
		
		DFP = DataFileParser(DFW.filename)
		DFP.parseXML_File()"""
		
	def import_data(self):
		filename = self.exportEntry.get()
		print("Code here to load",filename)
		
		
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
		
	def generateGraph(self):
		try:
			nodesAmount=int(self.nodesEntry.get())
			self.graph=Graph.Graph(nodesAmount)
			#TODO : personalisation (endroit, type de repas etc.)
			self.depot = [self.graph.nodes[0]] #TODO : multidepot
			
			self.displayGraph(self.graph)
		except ValueError:
			print("Veuillez entrer une valeur")

	def displayGraph(self,graph):
		if(self.guiGraph!=None):
			self.guiGraph.__init__(self.canvas)
		self.guiGraph = GUIGraph(self.canvas)
		self.guiGraph.generateGraph(graph)
		self.guiGraph.drawGraph()
		
		
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
		self.nodesAmount=len(graph.nodes)
		
		self.nodes=graph.nodes
		
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

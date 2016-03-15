# /usr/bin/env python 3
# -*- coding: utf-8 -*-
import DarpAlgo
import Car
import Graph
import Meal
import Node
import os
import GUIGraph
import GUIDrawings

from random import randint
from random import choice
import DataFileWriter
import DataFileParser

#TODO Ajouter les cars et les meals et les mettre à jour quand on load un file.
#Mettre à jour la valeur maximale des spinbox (depot, meals.cook, meals.client) quand le graphe change de taille (après un load/après un generate)

SCREENWIDTH=1000-350
SCREENHEIGHT=800-100
AUTOPLAY_SPEED=int(1000/24)
#SCREENWIDTH=1500 
#SCREENHEIGHT=950

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
		ans=""
		if(minutes<0):
			ans="-"
			minutes=-minutes
		minutes=round(minutes)
		return (ans+str(int(minutes/60))).zfill(2)+":"+str(int(minutes%60)).zfill(2)

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
			
	def colorCheck(self,widget,testValue):
		if(not testValue):
			widget.configure(bg = "#ff6666")
		elif(widget.cget('bg')!="#ff6666"):
			widget.configure(bg = "#F0F0ED")
			
			
	def getCarFrameDuration(self,carFrame):
		return self.timestring_to_minutes(carFrame.ENDTIME.get())-self.timestring_to_minutes(carFrame.STARTTIME.get())
			
	def __init__(self, master):
		self.foodDisplay = True
	
		self.graph = None
		self.availableCars= []
		self.availableMeals= []
		self.remainingMeals= []
		
		self.guiGraph = None
		self.showingParameters = True
		
		self.hoursInDay = [str(h).zfill(2)+":"+str(m).zfill(2) for h in range(24) for m in range(60)]
		self.dupeImage = Tk.PhotoImage(file=os.path.join("GUIELEM","duplicate.gif"))
		
		
		#MAINFRAME
		mainFrame = Tk.Frame(master)
		mainFrame.pack(fill=Tk.BOTH,expand=True)
		
		#PARAMETERS FRAME on the right    self.parametersFrame
		self.parametersFrame = Tk.Frame(mainFrame)#,bg="pink")
		self.fill_parametersFrame(self.parametersFrame)
		
		
		#SCHEDULES FRAME on the right    self.schedulesFrame
		self.schedulesFrame = Tk.Frame(mainFrame)#,bg="pink")
		self.fill_schedulesFrame(self.schedulesFrame)

		#DISPLAY FRAME on the left    self.displayFrame
		self.displayFrame = Tk.Frame(mainFrame)
		self.canvas = Tk.Canvas(self.displayFrame, width=SCREENWIDTH, height=SCREENHEIGHT )
		self.canvas.pack()
		 
		def displaySwitcher():
			self.switch_display(permanent=self.showingParameters)
		
		self.displaySwitch = Tk.Button(self.displayFrame,text="Switch display",
		command=displaySwitcher)
		self.displaySwitch.pack(side=Tk.TOP,anchor="w")
	
	
		self.schedulesFrame.grid(row=0, column=1, sticky="nsew",)
		self.parametersFrame.grid(row=0, column=1, sticky="nsew")
		self.displayFrame.grid(row=0, column=0, sticky="nsew")
		
		
		self.button = Tk.Button(
		self.parametersFrame, text="Start DARP", fg="red", command=self.start_darp)
		self.button.pack(side=Tk.BOTTOM,anchor="w")
		
		
		
		self.currentLoop = self.parametersFrame.after(1000,self.colorLoop)
		self.carsLoop = None
		self.carsEarliestSchedule = 0;
		self.carsLatestSchedule = -1;
		
		self.generateGraph()
		self.createMeals()
		self.createCars()
		self.bring_forth_parameters()
		#self.bring_forth_schedules()
		
		
	
	def switch_display(self,event=None,setTo=None,permanent=True):
		if(setTo==None):
			self.foodDisplay=not self.foodDisplay
			setTo=self.foodDisplay
		if(setTo==True):
			self.colorMeals()
			if(permanent):
				self.start_meals_recoloring()
		else:
			self.stop_meals_recoloring()
			self.uncolorMeals()

	def fill_parametersFrame(self,parametersFrame):
		
		#Generate nodes
		self.nodesFrame = Tk.Frame(parametersFrame)
		self.nodesLabel = Tk.Label(self.nodesFrame,text="Amount of Nodes: ")
		self.nodesAmount = Tk.StringVar()
		
		self.nodesEntry = Tk.Spinbox(self.nodesFrame, from_=3, to=150, width=4,textvariable=self.nodesAmount)
		self.nodesButton = Tk.Button(self.nodesFrame, text="Generate",command = self.generateGraph)
		self.nodesAmount.set(15)
		
		self.nodesFrame.pack(side=Tk.TOP,anchor="nw")#,fill=Tk.BOTH, expand=Tk.YES)
		self.nodesLabel.pack(side=Tk.LEFT,anchor="w")#,fill=Tk.BOTH, expand=Tk.YES)
		self.nodesEntry.pack(side=Tk.LEFT,anchor="w")#,fill=Tk.BOTH, expand=Tk.YES)
		self.nodesButton.pack(side=Tk.LEFT,anchor="w")#,fill=Tk.BOTH, expand=Tk.YES)
		
		#Select depot
		self.depotFrame = Tk.Frame(parametersFrame)
		self.depotFrame.pack(side=Tk.TOP,anchor="nw")
		
		self.depotLabel = Tk.Label(self.depotFrame,text="Depot node: ")
		self.depotValue = Tk.StringVar()
		self.depotEntry = Tk.Spinbox(self.depotFrame, from_=0, to=150, width=4, textvariable=self.depotValue)
		self.depotValue.set(0)
		
		self.depotLabel.pack(side=Tk.LEFT,anchor="w")
		self.depotEntry.pack(side=Tk.LEFT,anchor="w")
		self.depotEntry.bind("<FocusOut>",self.checkNode)
		self.depotEntry.bind("<KeyRelease>",self.checkNode)
		
		
		miniFrame = Tk.Frame(parametersFrame)
		miniFrame.pack(anchor="nw",side=Tk.TOP)
		
		scrollbar = Tk.Scrollbar(miniFrame)
		scrollbar.pack(side=Tk.RIGHT, fill=Tk.Y)
		
		scrollingCanvas = Tk.Canvas(miniFrame,yscrollcommand=scrollbar.set,height=SCREENHEIGHT-100)
		scrollbar.config(command=scrollingCanvas.yview)
		
		scrollingCanvas.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=Tk.TRUE)
		scrollingFrame = Tk.Frame(scrollingCanvas)
		interior_id = scrollingCanvas.create_window(0, 0, window=scrollingFrame,anchor=Tk.NW)
		def _configure_interior(event):
			# update the scrollbars to match the size of the inner frame
			size = (scrollingFrame.winfo_reqwidth(), scrollingFrame.winfo_reqheight())
			scrollingCanvas.config(scrollregion="0 0 %s %s" % size)
			if scrollingFrame.winfo_reqwidth() != scrollingCanvas.winfo_width():
				# update the canvas's width to fit the inner frame
				scrollingCanvas.config(width=scrollingFrame.winfo_reqwidth())
		scrollingFrame.bind('<Configure>', _configure_interior)     

		def _configure_canvas(event):
			if scrollingFrame.winfo_reqwidth() != scrollingCanvas.winfo_width():
				# update the inner frame's width to fill the canvas
				scrollingCanvas.itemconfigure(interior_id, width=scrollingCanvas.winfo_width())  
		scrollingCanvas.bind('<Configure>', _configure_canvas)           

		#Add meals
		self.mealsLabel = Tk.Label(scrollingFrame,text="Meals:")
		self.mealsFrame = Tk.Frame(scrollingFrame)
		self.mealsLabel.pack(side=Tk.TOP,anchor="nw")
		self.mealsFrame.pack(side=Tk.TOP,anchor="nw",fill=Tk.X)
		
		#Add cars
		self.carsLabel = Tk.Label(scrollingFrame,text="Cars:")
		self.carsFrame = Tk.Frame(scrollingFrame)
		self.carsLabel.pack(side=Tk.TOP,anchor="nw")
		self.carsFrame.pack(side=Tk.TOP,anchor="nw",fill=Tk.X)
		
		#Parser: save and Load
		self.parserFrame = Tk.Frame(parametersFrame)
		self.parserFrame.pack(side=Tk.BOTTOM,fill=Tk.X)
		
		self.exportButton = Tk.Button(self.parserFrame, text="Export as", command = self.export_data)
		self.exportButton.pack(side=Tk.LEFT)
		
		self.exportEntry = Tk.Entry(self.parserFrame)
		self.exportEntry.delete(0, Tk.END)
		self.exportEntry.insert(0, "FilenameTest")
		self.exportEntry.pack(side=Tk.LEFT,anchor="e",fill=Tk.X)
		
		self.loadButton = Tk.Button(self.parserFrame, text="Load",command = self.import_data)
		self.loadButton.pack(side=Tk.RIGHT)
		
		
	def redrawCars(self,obj=None,blanc="",mode="w"):
		data=self.timeAmount.get()
		if(self.is_timestring_ok(data)):
			self.guiGraph.redrawCars(self.timestring_to_minutes(data))
	
	def toggleCars(self,event=None):
		self.guiGraph.toggleCars();
		self.redrawCars()
		
	def fill_schedulesFrame(self,schedulesFrame):
		
		carsCommandsFrame = Tk.Frame(schedulesFrame)
		carsCommandsFrame.pack(side=Tk.BOTTOM,anchor="w")
		
		showCar = Tk.Button(schedulesFrame,text="Toggle cars",command=self.toggleCars)
		showCar.pack(side=Tk.BOTTOM,anchor="w")
		
		self.timeAmount = Tk.StringVar()
		
		timebar = Tk.Spinbox(carsCommandsFrame,values=self.hoursInDay , textvariable=self.timeAmount,width=9)
		timebar.pack(side=Tk.LEFT,anchor="w")
		timebar.bind("<FocusOut>",self.checkHour)
		timebar.bind("<KeyRelease>",self.checkHour)
		timebar.bind("<ButtonRelease-1>",self.checkHour)
		
		self.timeAmount.trace('w',self.redrawCars)
		
		autoplay = Tk.Button(carsCommandsFrame, text="Autoplay",command=self.switch_cars_autoplay)
		autoplay.pack(side=Tk.LEFT, anchor="e")
		
		"""
		timebar.bind("<FocusOut>",self.redrawCars,add="+")
		timebar.bind("<KeyRelease>",self.redrawCars,add="+")
		timebar.bind("<ButtonRelease-1>",self.redrawCars,add="+")
		"""
		
		
		miniFrame = Tk.Frame(schedulesFrame)
		miniFrame.pack(anchor="nw",side=Tk.TOP)
		
		
		scrollbar = Tk.Scrollbar(miniFrame)
		scrollbar.pack(side=Tk.RIGHT, fill=Tk.Y)
		
		scrollingCanvas = Tk.Canvas(miniFrame,yscrollcommand=scrollbar.set,height=SCREENHEIGHT-50)
		scrollbar.config(command=scrollingCanvas.yview)
		
		scrollingCanvas.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=Tk.TRUE)
		scrollingFrame = Tk.Frame(scrollingCanvas)
		interior_id = scrollingCanvas.create_window(0, 0, window=scrollingFrame,anchor=Tk.NW)
		def _configure_interior(event):
			# update the scrollbars to match the size of the inner frame
			size = (scrollingFrame.winfo_reqwidth(), scrollingFrame.winfo_reqheight())
			scrollingCanvas.config(scrollregion="0 0 %s %s" % size)
			if scrollingFrame.winfo_reqwidth() != scrollingCanvas.winfo_width():
				# update the canvas's width to fit the inner frame
				scrollingCanvas.config(width=scrollingFrame.winfo_reqwidth())
		scrollingFrame.bind('<Configure>', _configure_interior)     

		def _configure_canvas(event):
			if scrollingFrame.winfo_reqwidth() != scrollingCanvas.winfo_width():
				# update the inner frame's width to fill the canvas
				scrollingCanvas.itemconfigure(interior_id, width=scrollingCanvas.winfo_width())  
		scrollingCanvas.bind('<Configure>', _configure_canvas)           

		
		self.scheduleContainer = Tk.Frame(scrollingFrame)
		self.scheduleScrollingFrame = scrollingFrame
		self.scheduleContainer.pack(side=Tk.TOP,anchor="nw")
		self.updateSchedules()
		
		
		self.backToParamButton = Tk.Button(schedulesFrame,text="Retour aux paramètres",command=self.bring_forth_parameters)
		self.backToParamButton.pack(side=Tk.BOTTOM,anchor="s")
		
		
		
		
		
	def updateSchedules(self):
		self.scheduleContainer.destroy()
		self.scheduleContainer = Tk.Frame(self.scheduleScrollingFrame)
		self.scheduleContainer.pack(side=Tk.TOP,anchor="nw")
		
		testSched = Tk.Label(self.scheduleContainer, text="Affichage des schedules du car:")
		testSched.pack(side=Tk.TOP,anchor="nw")
		
		varSched = Tk.StringVar()
		varSched.set("Cliquez sur une voiture")
		scheduleText=Tk.Label(self.scheduleContainer, textvariable=varSched,justify=Tk.LEFT,font="monospace")
		
		carsOptionsFrame = Tk.Frame(self.scheduleContainer)
		carsOptionsFrame.pack(side=Tk.TOP,anchor="n")
		
		if(len(self.availableCars)==0):
			varSched.set("Pas de voiture disponible!")
			
		
		for i,car in enumerate(self.availableCars):
			def switchSchedule(car=car):
				scheduleText=self.generate_schedule_list(car)				
				varSched.set(str(scheduleText))
			if(len(self.availableCars)<10):
				oneCar = Tk.Button(carsOptionsFrame, text="Car "+str(i), command = switchSchedule)
			else:
				oneCar = Tk.Button(carsOptionsFrame, text=str(i), command = switchSchedule)
			oneCar.pack(side=Tk.LEFT,anchor="n")
			
			#switchSchedule()
			
		scheduleText.pack(side=Tk.TOP,anchor="s")
		
		
		if(len(self.remainingMeals)>0):
			remainingMealsText = Tk.Label(self.scheduleContainer, 
			text="Les repas suivants n'ont pas pu être livrés:\n"+self.remainingMealsString(),
			justify=Tk.LEFT,font="monospace 10")
			remainingMealsText.pack(side=Tk.TOP,anchor="s")
		else:
			remainingMealsText = Tk.Label(self.scheduleContainer,
			text="Tous les repas on été distribués!",justify=Tk.LEFT,font="monospace 10")
			remainingMealsText.pack(side=Tk.TOP,anchor="s")
		
		
	def remainingMealsString(self):
		
		answer  = ""
		for meal in self.remainingMeals:
			smeal = "\n-Livraison de "
			smeal+=self.minutes_to_timestring(meal.ddt)
			smeal+=" ("
			smeal+=self.minutes_to_timestring(meal.edt)
			smeal+=" au plus tôt"
			smeal+= ")\n           du noeud "+str(meal.chef.index)
			smeal+= " au noeud "+str(meal.destination.index)
			smeal+= " ("+str(round(self.graph.dist(meal.chef,meal.destination),2))+"km)"
			answer+=smeal+"\n"
			
		return answer
		
	def generate_schedule_list(self,car):
		
		if(len(car.currentSchedule)==0):
			return "Cette voiture n'a pas de schedule"
		scheduleTitles="Heure ","Noeud ","Pick/Del "," Heure permise "
		scheduleLenghts=tuple(len(elem) for elem in scheduleTitles)
		scheduleElements=[]
		allSchedules=""
		
		schedule = "|".join(scheduleTitles)
		
		scheduleElements.append(schedule)
		allSchedules+=schedule+"\n"
		
		schedule = ""
		schedule+=self.minutes_to_timestring(car.start).ljust(scheduleLenghts[0])
		schedule+="|"
		schedule+=str(car.depot.index).ljust(scheduleLenghts[1])
		schedule+="|"
		schedule+="Dépôt".ljust(scheduleLenghts[2])
		schedule+="|"
		
		scheduleElements.append(schedule)
		allSchedules+=schedule+"\n"
		
		temps=car.start
		
		prevnode = car.depot
		for block in car.currentSchedule:
			
			#prevslack
			schedule ="(Temps mort de " + str(round(block.getPrevSlack(),2)) +"'"+\
			(block.getPrevSlack()>=60 and " (+"+self.minutes_to_timestring(round(block.getPrevSlack()))+")" or "") +" )"
			scheduleElements.append(schedule)
			allSchedules+=schedule+"\n"
			#temps au dépôt + slack
			#schedule = ""+self.minutes_to_timestring(temps+block.getPrevSlack()).ljust(scheduleLenghts[0])
			#allSchedules+=schedule+"\n"
			
			for stop in block.stops:
				dist = self.graph.dist(prevnode,stop.node)
				prevnode=stop.node
				if(dist>0):
					schedule= "(Déplacement de "+str(round(dist,2))+"km )"
					allSchedules+=schedule+"\n"
			
				schedule = ""
				schedule+=self.minutes_to_timestring(stop.st).ljust(scheduleLenghts[0])
				schedule+="|"
				schedule+=str(stop.node.index).ljust(scheduleLenghts[1])
				schedule+="|"
				schedule+=((stop.isPickup() and "Pickup") or ("Delivery")).ljust(scheduleLenghts[2])
				schedule+="| "
				if(stop.isPickup()):
					#afficher l'heure à aquelle il doit Pickup AU PLUS TARD
					#afficher de combien de minutes il pourrait être en avance (earliest - latest)
					schedule+=self.minutes_to_timestring(stop.meal.getEPT())+" ~ "+self.minutes_to_timestring(stop.meal.getLPT())
				else:
					#afficher l'heure à aquelle il doit Dropoff AU PLUS TARD
					#afficher de combien de minutes il pourrait être en avance (deviation)
					schedule+=self.minutes_to_timestring(stop.meal.getEDT())+" ~ "+self.minutes_to_timestring(stop.meal.getLDT())
					
				
				scheduleElements.append(schedule)
				allSchedules+=schedule+"\n"
				
				temps=stop.st
				
		difference = car.getEnd()-temps
		schedule ="(Temps mort de " + str(round(difference,2)) +"'"+\
		(difference>=60 and " (+"+self.minutes_to_timestring(round(difference))+")" or "") + " )"
		allSchedules+=schedule+"\n"
				
		schedule = self.minutes_to_timestring(car.getEnd()).ljust(scheduleLenghts[0])+\
		"|"+str(car.depot.index).ljust(scheduleLenghts[1])+\
		"|"+"Dépôt"
		allSchedules+=schedule+"\n"
			
		return allSchedules
			
		
	def calculateEarlySchedule(self):
		self.carsEarliestSchedule=float('inf')
		self.carsLatestSchedule=float('-inf')
		for car in self.availableCars:
			if len(car.currentSchedule)>0:
				stop = car.currentSchedule[0].stops[0]
				self.carsEarliestSchedule=min(self.carsEarliestSchedule,stop.st)
				
				stop = car.currentSchedule[-1].stops[-1]
				self.carsLatestSchedule=max(self.carsLatestSchedule,stop.st)
		print("Early,late:",self.carsEarliestSchedule,self.carsLatestSchedule)
			
			

	def bring_forth_schedules(self):
		self.showingParameters=False
		self.stop_meals_recoloring()
		self.schedulesFrame.tkraise()
		
		self.guiGraph.resetCars(self.availableCars,self.graph)
		
	def bring_forth_parameters(self):
		self.showingParameters=True
		self.start_meals_recoloring()
		self.parametersFrame.tkraise()
		
		self.guiGraph.removeCars()
		self.stop_cars_autoplay()
	
	def start_meals_recoloring(self):
		if(self.currentLoop==None):
			self.currentLoop = self.parametersFrame.after(1000,self.colorLoop)
		
	def stop_meals_recoloring(self):
		if(self.currentLoop!=None):
			self.parametersFrame.after_cancel(self.currentLoop)
			self.currentLoop = None
			
	def start_cars_autoplay(self):
		if(self.carsLoop==None):
			self.calculateEarlySchedule()
			self.carsLoop = self.parametersFrame.after(AUTOPLAY_SPEED,self.carsAutoLoop)
	
	def stop_cars_autoplay(self):
		if(self.carsLoop!=None):
			self.parametersFrame.after_cancel(self.carsLoop)
			self.carsLoop = None
			
	def switch_cars_autoplay(self):
		if(self.carsLoop==None):
			self.start_cars_autoplay()
		else:
			self.stop_cars_autoplay()
		
		
	def carsAutoLoop(self,even=None):
		if(self.is_timestring_ok(self.timeAmount.get())):
			time = (self.timestring_to_minutes(self.timeAmount.get()) +1) % (24*60)
			if(self.carsEarliestSchedule<self.carsLatestSchedule):
				time=max(self.carsEarliestSchedule,
				time<self.carsLatestSchedule and time or self.carsEarliestSchedule)
			self.timeAmount.set(self.minutes_to_timestring(time))
		self.carsLoop = self.parametersFrame.after(AUTOPLAY_SPEED,self.carsAutoLoop)
		
		
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
					currentDuration = self.getCarFrameDuration(currentFrame)
					if(currentDuration<=0):
						raise ValueError("Car's currentDuration<=0")
					
					currentEndtime = self.timestring_to_minutes(currentFrame.ENDTIME.get())
					currentDepot = self.graph.getSortedNodes()[int(self.depotValue.get())]
					#print("La voiture ",i,"a un capacité de ",currentCapacity,
					#", a une starttime de ",currentStarttime," et a une durée de shift de ",
					#currentDuration)
					
					newCar = Car.Car(currentCapacity,currentStarttime,currentDuration,currentDepot,self.graph)
					allCars.append(newCar)
					
					
				except ValueError:
					errorMessage+="\nVeuillez entrer un nombre valide pour la voiture"+str(i)
					canStart=False
					
			if(canStart):
				darp = DarpAlgo.DarpAlgo(allMeals,allCars)
			
				print("Starting DARP...")
				self.stop_meals_recoloring()
				darp.createSchedules()
				self.remainingMeals=darp.getNotInsertedMeals()
				self.availableCars=allCars[:]
				
				self.bring_forth_schedules()
				self.updateSchedules()
	
			
		except ValueError:
			print("Veuillez entrer un nombre valide")

		
		if not canStart:
			Tk.messagebox.showwarning("DARP resolution",errorMessage)
			
		
	def export_data(self):
		
		if self.verifyEntries():			
			filename = self.exportEntry.get()
			
			cars=[] #maxcap, starttime, duration
			for carFrame in self.carFrames:
				cars.append(
					(
					carFrame.CAPACITY.get(),
					str(self.timestring_to_minutes( carFrame.STARTTIME.get() )),
					str(self.getCarFrameDuration(carFrame))
					)
				)
			
			meals=[] #dtt, deviation, chef,client
			for mealFrame in self.mealsFrames:
				meals.append((str(self.timestring_to_minutes(mealFrame.DELIVERY.get())),mealFrame.DEVIATION.get(),mealFrame.COOK.get(),mealFrame.CLIENT.get()))
				
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
			carFrame.ENDTIME.set(self.minutes_to_timestring(int(car.end)))
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
		entry_COOK.pack(side=Tk.LEFT)
		entry_COOK.bind("<FocusOut>",self.checkNode)
		entry_COOK.bind("<KeyRelease>",self.checkNode)
		entry_COOK.bind("<Motion>",self.checkNode)
		
		#entry_COOK.bind("<FocusOut>",self.colorLoop,add="+")
		#entry_COOK.bind("<KeyRelease>",self.colorLoop,add="+")
		#entry_COOK.bind("<Motion>",self.colorLoop,add="+")
		
		#entry_CLIENT = Tk.Entry(tempMealFrame,textvariable=tempMealFrame.CLIENT,width=6)
		entry_CLIENT = Tk.Spinbox(tempMealFrame, from_=0, to=150, textvariable=tempMealFrame.CLIENT, width=5)
		entry_CLIENT.pack(side=Tk.LEFT)
		entry_CLIENT.bind("<FocusOut>",self.checkNode)
		entry_CLIENT.bind("<KeyRelease>",self.checkNode)
		entry_CLIENT.bind("<Motion>",self.checkNode)
		
		#entry_CLIENT.bind("<FocusOut>",self.colorLoop,add="+")
		#entry_CLIENT.bind("<KeyRelease>",self.colorLoop,add="+")
		#entry_CLIENT.bind("<Motion>",self.colorLoop,add="+")
		
		
		#entry_DEVIATION = Tk.Entry(tempMealFrame,textvariable=tempMealFrame.DEVIATION,width=9)
		entry_DEVIATION = Tk.Spinbox(tempMealFrame, from_=0, to=100, textvariable=tempMealFrame.DEVIATION, width=8)
		entry_DEVIATION.pack(side=Tk.LEFT) # TODO: realTime
		entry_DEVIATION.bind("<FocusOut>",self.checkValue)
		entry_DEVIATION.bind("<KeyRelease>",self.checkValue)
		
		entry_DELIVERY = Tk.Spinbox(tempMealFrame, values=self.hoursInDay, textvariable=tempMealFrame.DELIVERY, width=8)
		entry_DELIVERY.pack(side=Tk.LEFT) # TODO: realTime
		entry_DELIVERY.bind("<FocusOut>",self.checkHour)
		entry_DELIVERY.bind("<KeyRelease>",self.checkHour)
		
		tempMealFrame.DELIVERY.set("10:00")
		tempMealFrame.DEVIATION.set("10")
		tempMealFrame.COOK.set(len(self.graph.getSortedNodes())-1)
		tempMealFrame.CLIENT.set(int(len(self.graph.getSortedNodes())/2))
		
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
		label_ENDTIME = Tk.Label(carHeaderFrame,text="End",width=10)
		label_ENDTIME.pack(side=Tk.LEFT)
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
		tempCarFrame.ENDTIME=Tk.StringVar()
		
		
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
		entry_ENDTIME = Tk.Spinbox(tempCarFrame, values=self.hoursInDay , textvariable=tempCarFrame.ENDTIME,width=9)
		entry_ENDTIME.pack(side=Tk.LEFT)
		entry_ENDTIME.bind("<FocusOut>",self.checkHour)
		entry_ENDTIME.bind("<KeyRelease>",self.checkHour)
		
		
		def check_hourdiff(event):
			self.colorCheck(entry_ENDTIME,self.getCarFrameDuration(tempCarFrame)>0)
			
		entry_ENDTIME.bind("<FocusOut>", check_hourdiff, add="+")
		entry_ENDTIME.bind("<KeyRelease>", check_hourdiff, add="+")
		entry_STARTTIME.bind("<FocusOut>", check_hourdiff, add="+")
		entry_STARTTIME.bind("<KeyRelease>", check_hourdiff, add="+")



		tempCarFrame.STARTTIME.set("00:00")
		tempCarFrame.ENDTIME.set("23:00")
		tempCarFrame.CAPACITY.set("5")
		

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
			mycar.ENDTIME.set( tempCarFrame.ENDTIME.get() )
			
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
		self.guiGraph = GUIGraph.GUIGraph(self.canvas)
		self.guiGraph.generateGraph(graph)
		self.guiGraph.drawGraph()
	
	def verifyEntries(self):
		#gérer les float ? 0.5 capacity?
		for index,carFrame in enumerate(self.carFrames):	
			print(index)
			#if int(carFrame.CAPACITY.get()) < 0 or int(carFrame.STARTTIME.get()) < 0 or int(carFrame.DURATION.get()) < 0:
			if not(self.is_amountstring_ok(carFrame.CAPACITY.get())
			and self.is_timestring_ok(carFrame.STARTTIME.get())
			and self.is_timestring_ok(carFrame.ENDTIME.get())
			and self.getCarFrameDuration(carFrame)>0):
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
			
	def colorLoop(self,event=None):
		self.colorMeals()
		self.currentLoop = self.parametersFrame.after(500,self.colorLoop)
		
	
	def colorMeals(self):
		if(self.guiGraph != None):
			mealPairs = []
			for mealFrame in self.mealsFrames:
				cook = mealFrame.COOK.get()
				client = mealFrame.CLIENT.get()
				if(self.is_nodestring_ok(cook) and self.is_nodestring_ok(client)):
					mealPairs.append((int(cook), int(client)))
			self.guiGraph.redrawMeals(mealPairs)
		
	def uncolorMeals(self):
		if(self.guiGraph != None):
			self.guiGraph.redrawMeals(tuple())
		

def callFocusOut(parent):
	#set the focus on the childrens of a frame
	#the focus is lost, calling FocusOut (recoloring our widgets)
	for widget in parent.winfo_children():
		widget.focus_set()
	
		
	
root = Tk.Tk()

app = App(root)

root.mainloop()
try:
	root.destroy() #if it wasn't already
except:
	exit() #quit anyway

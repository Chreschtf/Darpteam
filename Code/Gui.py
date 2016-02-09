# /usr/bin/env python 3
# -*- coding: utf-8 -*-
 
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
		self.createCars(self.parametersFrame)

		#self.hi_there = Tk.Button(self.parametersFrame, text="Hello", command=self.say_hi)
		#self.parametersFrame.quit est la commande pour quitter

	def start_darp(self):
		try:
			cooks=int(self.cooksEntry.get())
			clients=int(self.clientsEntry.get())
			print("Lancement de l'algo avec",cooks,"cuisiniers et",clients,"clients")
			for i in range(len(self.carFrames)):
				currentFrame = self.carFrames[i]
				try:
					currentCapacity = int(currentFrame.CAPACITY.get())
					currentStarttime = int(currentFrame.STARTTIME.get())
					currentDuration = int(currentFrame.DURATION.get())
					print("La voiture ",i,"a un capacité de ",currentCapacity,", a une starttime de ",currentStarttime," et a une durée de shift de ",currentDuration)
				except ValueError:
					print("Veuillez entrer un nombre valide pour la voiture")
		except ValueError:
			print("Veuillez entrer un nombre valide")
		
			
			
	def createCars(self,frame):
		self.carFrames = []
		carHeaderFrame = Tk.Frame(frame)
		carHeaderFrame.pack(side=Tk.TOP)
		self.button_PLUS = Tk.Button(carHeaderFrame,text="+",fg="red",command=self.addCar)
		self.button_PLUS.pack(side=Tk.LEFT)
		self.label_MAXCAPACITY = Tk.Label(carHeaderFrame,text="Capacity")
		self.label_MAXCAPACITY.pack(side=Tk.LEFT)
		self.label_STARTTIME = Tk.Label(carHeaderFrame,text="Start")
		self.label_STARTTIME.pack(side=Tk.LEFT)
		self.label_DURATION = Tk.Label(carHeaderFrame,text="Duration")
		self.label_DURATION.pack(side=Tk.LEFT)
		
		
	def addCar(self):
		
		tempCarFrame=Tk.Frame(self.parametersFrame)
		self.carFrames.append(tempCarFrame)
		tempCarFrame.pack(side=Tk.TOP)
		
		tempCarFrame.CAPACITY=Tk.StringVar()
		tempCarFrame.STARTTIME=Tk.StringVar()
		tempCarFrame.DURATION=Tk.StringVar()
		
		entry_MAXCAPACITY = Tk.Entry(tempCarFrame,textvariable=tempCarFrame.CAPACITY)
		entry_MAXCAPACITY.pack(side=Tk.LEFT)
		entry_STARTTIME = Tk.Entry(tempCarFrame,textvariable=tempCarFrame.STARTTIME)
		entry_STARTTIME.pack(side=Tk.LEFT)
		entry_DURATION = Tk.Entry(tempCarFrame,textvariable=tempCarFrame.DURATION)
		entry_DURATION.pack(side=Tk.LEFT)

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
		
		duplicateButton = Tk.Button(tempCarFrame,text="D",command=duplicateCar)
		duplicateButton.pack(side=Tk.RIGHT)
		
		return tempCarFrame
		
		
root = Tk.Tk()

app = App(root)

root.mainloop()
root.destroy() # optional; see description below

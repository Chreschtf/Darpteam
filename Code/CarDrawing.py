try:
	import Tkinter as Tk
except ImportError:
	import tkinter as Tk

import os
import Car
import Block
import Stop
from math import atan2

if __name__=="__main__":
	root = Tk.Tk()
	
class CarDrawing:
	colorNum = 16
	rotNum = 32
	index = 0;
	carImage=None
		
	def __init__(self,car,graph,GUIgraph,canvas):
		self.canvas=canvas
		self.carNum = CarDrawing.index
		self.car=car
		self.graph=graph
		self.GUIgraph = GUIgraph
		self.schedule=car.currentSchedule
		CarDrawing.index+=1;
		self.has_schedule=False
		self.transform_schedule()
		
		if(CarDrawing.carImage==None):
			CarDrawing.carImage=[[] for i in range(CarDrawing.colorNum)]
			for num in range(CarDrawing.colorNum*CarDrawing.rotNum):
				CarDrawing.carImage[int(num/CarDrawing.rotNum)].append(Tk.PhotoImage(file=os.path.join("GUIELEM","CARDATA","CARIMAGE"+str(num).zfill(4)+".gif")))
				
		self.carDrawing=None
		self.reset_drawing()
		
	def transform_schedule(self):
		self.times=[0]
		self.nodes=[self.car.depot]
		lastTime=0
		lastNode=self.car.depot
		if(len(self.schedule)==0):
			self.has_schedule=False
			return
			
		self.has_schedule=True
			
		for block in self.schedule:
			lastTime+=block.prevSlack
			self.times.append(lastTime)
			self.nodes.append(lastNode)
			#if(lastNode!=block.getStart()):
			#	print("Error, different nodes:",lastNode.index,block.getStart().index)
			for stop in block.stops:
				dist = self.graph.dist(lastNode,stop.node)
				lastNode=stop.node
				lastTime+=dist
				
				if(dist>0):
					self.times.append(lastTime)
					self.nodes.append(lastNode)
		
		
		dist = self.graph.dist(lastNode,self.car.depot)
		lastNode=self.car.depot
		lastTime+=dist
		if(dist>0):
			self.times.append(lastTime)
			self.nodes.append(lastNode)
			
		#print(self.times)
		#print(self.nodes)
	def get_schedule_lastnode(self,time):
		#retourne le dernier noeud de pickup/delivery fait et la distance actuelle
		for index,timeframe in enumerate(self.times):
			if(timeframe>time):
				nextNode = self.nodes[index]
				
				previndex = index-1
				if(previndex<0):
					time=timeframe
					index=0
					#dépôt, pas encore sorti
				
				lastNode=self.nodes[index]
				lastTime=self.times[index] #is the one before timeframe
				
				deltaPos=(time-lastTime) #combien d'unités on a avancé
				#/(timeframe-lastTime or 1) #no division by zero #edit:not needed
				print("Pickup/del:",lastNode,nextNode,deltaPos)
				return lastNode,nextNode,deltaPos
		
		print("Pickup/del:",self.car.depot, self.car.depot, 0)
		return self.car.depot, self.car.depot, 0
		
	def get_schedule_node(self,time):
		#retourne le dernier noeud visité et le noeud suivant, et l'échelle entre les deux
		node1, node2, deltaPos = self.get_schedule_lastnode(time)
		#route = self.graph.getRoute(node1,node2)
		route=[node1,node2]
		
		currentDistance = 0
		prevNode = node1
		
		for index,node in enumerate(route):
			dist=self.graph.dist(prevNode,node)
			if(currentDistance+dist>deltaPos):
				startingNode = prevNode
				posScale = (currentDistance-deltaPos)/(self.graph.dist(prevNode,node) or 1)
				endingNode = node
				print("Node",startingNode, endingNode,posScale)
				return startingNode, endingNode,posScale
			
			currentDistance+=dist
		print("Node",node1,node1,0)
		return node1,node1,0
	def get_schedule_position(self,time):
		#retourne la position x et y du centre de la voiture, ainsi que l'angle
		node1, node2, posScale = self.get_schedule_node(time)
		
		drawNode1=self.GUIgraph.findNode(node1)
		drawNode2=self.GUIgraph.findNode(node2)
		
		if(drawNode1==None or drawNode2==None):
			print("Cannot find in:")
			print(self.GUIgraph.canvasNodes)
			print(node1,node1.index,drawNode1)
			print(node2,node2.index,drawNode2)
			return 0,0,0 #what the hell is happening
		
		x0=drawNode1.x
		y0=drawNode1.y
		y0-=CarDrawing.index*5/2+self.carNum*5 #pour les décaler si elles se superposent
		
		dx=drawNode2.x-drawNode1.x
		dy=drawNode2.y-drawNode1.y
		
		dx*=posScale
		dy*=posScale
		
		angle = atan2(dy,dx) #atan2 prends en compte tout
		
		return x0+dx,y0+dy,angle
		
	def move_drawing(self,time):
		if(self.has_schedule):
			self.remove_drawing()
			x,y,angle = self.get_schedule_position(time)
			self.carDrawing=self.canvas.create_image(
		(x,y),image=self.getImage(angle))
		#self.canvas.image(self.carDrawing,self.getImage(angle))
		#self.canvas.coords(self.carDrawing,(x,y))
		
	def reset_drawing(self):
		"""if(self.carDrawing==None):
			self.carDrawing=self.canvas.create_image(
			(0,0),image=self.getImage(0))
		"""
	def remove_drawing(self):
		if(self.carDrawing!=None):
			self.canvas.delete(self.carDrawing)
			self.carDrawing=None
		
	def getImage(self,angle):
		return CarDrawing.carImage[self.carNum][(int(angle/360*CarDrawing.rotNum)%CarDrawing.rotNum)];
		
		
		
	#TODO: draw dans le canvas
		
	@staticmethod
	def reset_index():
		CarDrawing.index=0;
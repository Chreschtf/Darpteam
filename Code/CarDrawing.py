try:
	import Tkinter as Tk
except ImportError:
	import tkinter as Tk

import os
import Car
import Block
import Stop

if __name__=="__main__":
	root = Tk.Tk()
	
class CarDrawing:
	colorNum = 16
	rotNum = 32
	carImage=[[] for i in range(colorNum)]
	for num in range(colorNum*rotNum):
		carImage[int(num/rotNum)].append(Tk.PhotoImage(file=os.path.join("GUIELEM","CARDATA","CARIMAGE"+str(num).zfill(4)+".gif")))
	index = 0;
		
	def __init__(self,car,graph,GUIgraph,canvas):
		self.carNum = index
		self.car=car
		self.graph=graph
		self.GUIgraph = GUIgraph
		self.schedule=car.currentSchedule
		index+=1;
		self.has_schedule=False
		self.transform_schedule()

	def transform_schedule(self):
		self.times=[0]
		self.nodes=[self.car.depot]
		lastTime=0
		lastNode=car.depot
		if(len(self.schedule)==0):
			self.has_schedule=False
			return
			
		self.has_schedule=True
			
		for block in self.schedule:
			lastTime+=block.prevSlack
			self.times.append(lastTime)
			self.nodes.append(lastNode)
			if(lastNode!=block.getStart()):
				print("Error, different nodes:",lastNode.index,block.getStart().index)
			for stop in block.stops:
				dist = self.graph.dist(prevnode,stop.node)
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
				
				return lastNode,nextNode,deltaPos
		return self.car.depot, self.car.depot, 0
		
	def get_schedule_node(self,time):
		#retourne le dernier noeud visité et le noeud suivant, et l'échelle entre les deux
		node1, node2, deltaPos = get_schedule_lastnode(time)
		route = self.graph.getRoute(node1,node2)
		currentDistance = 0
		prevNode = node1
		
		for index,node in enumerate(route):
			dist=self.graph.dist(prevNode,node)
			currentDistance=
			if(currentDistance+dist>deltaPos):
				startingNode = prevNode
				posScale = (currentDistance-deltaPos)/(self.graph.dist(prevNode,node) or 1)
				endingNode = node
				
				return startingNode, endingNode,posScale
				
	def get_schedule_position(self,time):
		#retourne la position x et y du centre de la voiture
		node1, node2, posScale = self.get_schedule_node(time)
		
		drawNode1=self.GUIgraph.findNode(node1)
		drawNode2=self.GUIgraph.findNode(node2)
		x0=drawNode1.x
		y0=drawNode1.y
		y0-=CarDrawing.index*5/2+self.carNum*5 #pour les décaler si elles se superposent
		
		dx=drawNode2.x-drawNode1.x
		dy=drawNode2.y-drawNode1.y
		
		dx*=posScale
		dy*=posScale
		
		return x0+dx,y0+dy
		
	def getImage(self):
		return carImage[self.carNum*rotNum];
		
	#TODO: draw dans le canvas
		
	@staticmethod
	def reset_index():
		CarDrawing.index=0;
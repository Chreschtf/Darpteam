try:
	import Tkinter as Tk
except ImportError:
	import tkinter as Tk



class NodeDrawing:
	def __init__(self,x,y,content,canvas,realNode,margin):
		self.canvas=canvas
		self.x=x 
		self.y=y 
		self.content=content
		self.realNode=realNode
		
		self.lowerbound = margin
		self.upperbound = int(self.canvas.cget("width"))-margin
		
	def move(self,x,y):
		self.x=min(self.upperbound,max(self.lowerbound,x)) 
		self.y=min(self.upperbound,max(self.lowerbound,y))
		self.canvas.coords(self.oval,self.ovalCoords())
		self.canvas.coords(self.text,(self.x,self.y))
		
	def isMine(self,shape):
		return self.oval==shape or self.text==shape
		
	def generateDrawing(self):
		self.oval=self.canvas.create_oval(self.ovalCoords(),fill="pink",activefill="red")
		self.text=self.canvas.create_text((self.x,self.y),text=self.content)
		
	def ovalCoords(self):
		return (self.x-20,self.y-20,self.x+20,self.y+20)
	
	
	
		
		
		
class NodeLines:
	def __init__(self,canvas,nodeslist=[],adjacence=[[]]):
		self.nodes=nodeslist
		#self.linespos=[]
		self.lines=[]
		self.canvas=canvas
		self.adjacence=adjacence
		self.generateLines()
		
	def addNode(self,node):
		self.nodes.append(node)
		
	def removeNode(self,node):
		self.nodes.remove(node)
		
	def generateLines(self):
		linespos = []
		
		for i in range(len(self.nodes)):
			for j in range(i+1,len(self.nodes)):
				p1 = self.nodes[i]
				p2 = self.nodes[j]
				if(self.adjacence[i][j]):
					linespos.append((p1.x,p1.y,p2.x,p2.y))
				
		for linepos in linespos:
			self.lines.append(self.canvas.create_line(linepos))#,width=8,fill="pink"))
	
	def drawLines(self):
		
		counter=0
		
		for i in range(len(self.nodes)):
			for j in range(i+1,len(self.nodes)):
				p1 = self.nodes[i]
				p2 = self.nodes[j]
				if(self.adjacence[i][j]):
					self.canvas.coords(self.lines[counter],(p1.x,p1.y,p2.x,p2.y))
					counter+=1
		
		
		#for line in self.lines:
		#	self.canvas.delete(line)
		
		

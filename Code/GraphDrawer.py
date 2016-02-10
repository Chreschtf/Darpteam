try:
	import Tkinter as Tk
except ImportError:
	import tkinter as Tk



class NodeDrawing:
	def __init__(self,x,y,content,canvas):
		self.canvas=canvas
		self.x=x 
		self.y=y 
		self.content=content
		self.oval=self.canvas.create_oval(self.ovalCoords())
		self.text=self.canvas.create_text((x,y),text=content)
		
	def move(self,x,y):
		self.x=x 
		self.y=y 
		self.canvas.coords(self.oval,self.ovalCoords())
		
	def ovalCoords(self):
		return (self.x-20,self.y-20,self.x+20,self.y+20)
		
		
class NodeLines:
	def __init__(self,canvas,nodeslist=[],adjacence=[[]]):
		self.nodes=nodeslist
		#self.linespos=[]
		self.lines=[]
		self.canvas=canvas
		self.adjacence=adjacence
		self.drawLines()
		
	def addNode(self,node):
		self.nodes.append(node)
		
	def removeNode(self,node):
		self.nodes.remove(node)
		
	def drawLines(self):
		for line in self.lines:
			self.canvas.delete(line)
		
		linespos = []
		
		for i in range(len(self.nodes)):
			for j in range(i+1,len(self.nodes)):
				p1 = self.nodes[i]
				p2 = self.nodes[j]
				if(self.adjacence[i][j]):
					linespos.append((p1+p2))
				
		for linepos in linespos:
			self.lines.append(self.canvas.create_line(linepos))
		

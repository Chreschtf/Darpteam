try:
	import Tkinter as Tk
except ImportError:
	import tkinter as Tk
	
import Graph
import GUIDrawings

class GUIGraph:
	coloredIcons = None
	
	def __init__(self,canvas):
		#self.nodesAmount = 20
		self.canvas = canvas
		if(GUIGraph.coloredIcons==None):
			GUIGraph.coloredIcons= GUIDrawings.AvailableColors()
		
		self.realNodes = []
		self.positionsInGraph = []
		self.canvasNodes = []
		self.margin = 25
		
		self.mouseDelta = (None,None)
		self.currentNode=None
		
		self.canvas.bind("<ButtonPress-1>", self.clickObject)
		self.canvas.bind("<B1-Motion>", self.moveObject)
		self.canvas.bind("<ButtonRelease-1>", self.releaseObject)
		
		print("New GUIGraph")
	
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
			
			
			
		width=int(self.canvas.cget("width"))
		
		self.canvas.create_line(4, width-4, 4, width-4-(1/self.deltaY*self.screensize))
		self.canvas.create_line(4, width-4, 4+(1/self.deltaX*self.screensize), width-4)
		
	def drawGraph(self):	
			
		#adjacenceMatrix= [[None]*self.nodesAmount for i in range(self.nodesAmount)]
		#for i in range(self.nodesAmount):
		#	for j in range(self.nodesAmount):
		#		adjacenceMatrix[i][j]=choice([0,0,0,0,0,1])
		
		adjacenceMatrix=self.graph.getAdjMatrix()
		
		
		
		for j,(x,y) in enumerate(self.positionsInGraph):
			self.canvasNodes.append(GUIDrawings.NodeDrawing(x,y,str(j),self.canvas,self.nodes[j],self.margin))
			
			
		#self.linesDrawer = NodeLines(self.canvas,self.canvasNodes,adjacenceMatrix)
		GUIDrawings.generateLines(self.canvas,self.canvasNodes,adjacenceMatrix)
		
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

		
	def redrawMeals(self,mealpairs):
		for node in self.canvasNodes:
			node.removeIcons()
		GUIGraph.coloredIcons.reset_set()
		
		for cooknode,clientnode in mealpairs:
			cookimage, clientimage = GUIGraph.coloredIcons.get_image_set()
			self.canvasNodes[cooknode].addIcon(cookimage)
			self.canvasNodes[clientnode].addIcon(clientimage)
		
			
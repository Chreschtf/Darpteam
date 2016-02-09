class NodeDrawing:
	def __init__(self,x,y,content,canvas):
		self.canvas=canvas
		self.x=x 
		self.y=y 
		self.content=content
		self.oval=self.canvas.create_oval(self.ovalCoords())
		
	def move(self,x,y)
		self.x=x 
		self.y=y 
		self.canvas.coords(self.oval,self.ovalCoords())
		
	def ovalCoords(self):
		return (self.x-20,self.y-20,self.x+20,self.y+20)
		
		
class NodeLines:
	def __init__(self,canvas,nodeslist=[]):
		self.nodes=nodeslist
		self.lines=[]
		self.canvas=canvas
		
	def addNode(self,node):
		self.nodes.append(node)
		
	def removeNode(self,node):
		self.nodes.remove(node)
		
	def redrawNodes(self):
		for line in self.lines:
			self.canvas.delete(line)
		
		linespos = set()
		
		for node in self.nodes:
			pass
			#code to get the node's neighbor
			p1 = (15,16)
			p2 = (180,180)
			
			if(p1>p2):
				linespos.add((p1,p2))
			else:
				linespos.add((p2,p1))
			#no repeats
			
		for linepos in linespos:
			lines.append(self.canvas.create_line(linepos))
		
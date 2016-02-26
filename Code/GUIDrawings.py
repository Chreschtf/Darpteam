try:
	import Tkinter as Tk
except ImportError:
	import tkinter as Tk

import os
from random import shuffle

class AvailableColors:
	def __init__(self):
		self.colors="blue","red","green","orange", "yellow"
		self.colorsvals=(64,64,224), (64,224,64),(224,64,64),(224,128,64), (224,224,64)
		black_offsets=2,3,4,5,6
		white_offsets=9,10,11,12,13 #utilisé uniquement lors du load initial
		self.pack_size=24			
		self.black_icons=[ ]		
		self.white_icons=[ ]
		for i in range(self.pack_size):
			for j in black_offsets:
				self.black_icons.append(Tk.PhotoImage(file=os.path.join("GUIELEM","FOODICONS","FOODICON"+str(i+j*self.pack_size).zfill(4)+".gif")))
			for j in white_offsets:
				self.white_icons.append(Tk.PhotoImage(file=os.path.join("GUIELEM","FOODICONS","FOODICON"+str(i+j*self.pack_size).zfill(4)+".gif")))
		self.knownMeals = []
		
		
		self.baseIndexes=[i for i in range(len(self.colors)*self.pack_size)]
		shuffle(self.baseIndexes)
		self.reset_set() #self.indexes
		
	def get_image_set(self):
		index=self.indexes.pop()
		color_index=int(round(index//self.pack_size%len(self.colors)))
		print(index,"/",len(self.black_icons),"-",color_index,"/",len(self.colors))
		return (self.black_icons[index],self.white_icons[index])#,self.colorsvals[color_index],index)
		
	def return_image_set(self,index):
		index.insert(index,0)
		
	def reset_set(self):
		self.indexes=self.baseIndexes[:]
		
		
		
class NodeDrawing:
	def __init__(self,x,y,content,canvas,realNode,margin):
		self.canvas=canvas
		self.x=x 
		self.y=y 
		self.content=content
		self.realNode=realNode
		self.icons = []
		self.images= []
		
		self.lowerbound = margin
		self.upperbound = int(self.canvas.cget("width"))-margin
		
		self.listeners=[]
		
	def move(self,x,y):
		self.x=min(self.upperbound,max(self.lowerbound,x)) 
		self.y=min(self.upperbound,max(self.lowerbound,y))
		self.canvas.coords(self.oval,self.ovalCoords())
		self.canvas.coords(self.text,(self.x,self.y))
		self.updateIcons()
		
		self.notifyListeners("moved")
		
	def updateIcons(self):
		num = len(self.icons)
		w=24
		w2=w/2
		l=self.x-20+w2
		h=self.x+20-w2
		d=h-l
		
		y=self.y-w2-5
		if(num==1):
			self.canvas.coords(self.icons[0],((l+h)/2,y))
		else:
			for i,image in enumerate(self.icons):
				self.canvas.coords(image,(l+i*d/(num-1),y))
		
	def isMine(self,shape):
		return self.oval==shape or self.text==shape or shape in self.icons
		
	def isMyNode(self,realNode):
		return self.realNode == realNode
		
	def generateDrawing(self):
		self.oval=self.canvas.create_oval(self.ovalCoords(),fill="pink",activefill="red")
		self.text=self.canvas.create_text((self.x,self.y),text=self.content)
		
	def ovalCoords(self):
		return (self.x-20,self.y-20,self.x+20,self.y+20)
	
	def addListener(self,listener):
		self.listeners.append(listener)
	
	def removeListener(self,listener):
		self.listeners.remove(listener)
		
	def notifyListeners(self,message):
		for listener in self.listeners:
			listener.notify(message)
	
	def destroyNode(self):
		self.notifyListeners("destroy")
		self.canvas.delete(self.oval)
		self.canvas.delete(self.text)
		for image in self.icons:
			self.canvas.delete(image)
		
	def addIcon(self,icon):
		self.images.append(icon)
		self.icons.append(self.canvas.create_image((0,0),image=icon))
		self.updateIcons()
		
	def removeIcon(self,icon):
		index=self.images.index(icon)
		self.canvas.delete(self.icons[index])
		self.images.pop(index)
		self.icons.pop(index)
		self.updateIcons()
		
				
	def removeIcons(self):
		for icon in self.icons:
			self.canvas.delete(icon)
		self.images=[]
		self.icons=[]
		
def generateLines(canvas,nodeslist,adjacence):
	for i in range(len(nodeslist)):
			for j in range(i+1,len(nodeslist)):
				n1 = nodeslist[i]
				n2 = nodeslist[j]
				if(adjacence[i][j]):
					LineDrawing(n1,n2,canvas)


class LineDrawing:
	def __init__(self,node1,node2,canvas,distance=-1):
		self.nodes=[node1,node2]
		
		
		self.canvas=canvas
		node1.addListener(self)
		node2.addListener(self)
		
		self.fatlLine=None
		self.thinLine=None
		#self.dots=[]
		
		self.generate()
		if(distance==-1):
			self.distance=self.lineDist()
		else:
			self.distance=distance
		
	def redraw(self):
		self.canvas.coords(self.fatlLine,self.lineCoords())
		self.canvas.coords(self.thinLine,self.lineCoords())
		
		if(abs(self.lineDist()-self.distance)>4):
			self.canvas.itemconfig(self.thinLine,dash=min(255,max(1,int(6*self.lineDist()/max(1,self.distance)))))
		else:
			self.canvas.itemconfig(self.thinLine,dash=[])
		#draw dots
		
	def generate(self):
		if(not self.thinLine):
			self.fatlLine=self.canvas.create_line(self.lineCoords(),width=8,fill="grey")
			self.thinLine=self.canvas.create_line(self.lineCoords(),width=6,fill="pink")#,dash=6)
		else:
			pass
			
	def lineCoords(self):
		return (self.nodes[0].x,self.nodes[0].y,self.nodes[1].x,self.nodes[1].y)
		
	def lineDist(self):
		x1,y1,x2,y2=self.lineCoords()
		
		return ((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))**0.5
		
	def notify(self,message):
		if(message=="destroy"):
			pass
			self.node[1].removeListener(self)
			self.node[2].removeListener(self)
			self.canvas.delete(self.fatLine)
			self.canvas.delete(self.thinLine)
			self.fatLine=None
			self.thinLine=None
		elif(message=="regenerate"):
			pass
		else:
			self.redraw()
		

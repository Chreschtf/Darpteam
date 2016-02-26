try:
	import Tkinter as Tk
except ImportError:
	import tkinter as Tk

import os
from random import shuffle
class AvailableColors:
	client_icons = []
	cook_icons = []
	pack_size=25
	#colorsvals=(64,192,64),(224,64,64),(96,96,224),(224,128,64), (64,192,192), (192,96,192),(224,192,32),(128,128,128)
	colorsvals="#40C040","#E04040","#6060E0","#E08040","#40C0C0","#C060C0","#E0C020","#808080"
	colors="green","red","blue","orange", "cyan","purple","yellow","grey"
	def __init__(self):
		self.colors=AvailableColors.colors
		self.pack_size=AvailableColors.pack_size	
		if(len(AvailableColors.client_icons)==0):
			for j in range(len(self.colors)):
				for i in range(self.pack_size):
					AvailableColors.client_icons.append(Tk.PhotoImage(file=os.path.join("GUIELEM","BLACKFORE","FOOD_BLACKFORE"+str(i+j*self.pack_size).zfill(4)+".gif")))
					AvailableColors.cook_icons.append(Tk.PhotoImage(file=os.path.join("GUIELEM","WHITEBACK","FOOD_WHITEBACK"+str(i+j*self.pack_size).zfill(4)+".gif")))
		self.knownMeals = []
		
		self.image_index=0
		self.image_delta=self.pack_size+1
		
	def get_image_set(self):
		index = self.image_index
		if(index%self.pack_size==self.pack_size-1):
			self.image_index-=self.pack_size
		#print(index,self.image_index,len(AvailableColors.client_icons))
		self.image_index=(self.image_index+self.image_delta)%len(AvailableColors.client_icons)
		return (AvailableColors.cook_icons[index],AvailableColors.client_icons[index], index)
		
	def reset_set(self):
		self.image_index=0
		
		
def get_color(index):
	return AvailableColors.colorsvals[int(index/AvailableColors.pack_size)%len(AvailableColors.colors)]
			
class NodeDrawing:
	def __init__(self,x,y,content,canvas,realNode,margin):
		self.canvas=canvas
		self.x=x 
		self.y=y 
		self.content=content
		self.realNode=realNode
		self.icons = []
		self.images= []
		self.iconcircles = []
		
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
		
		
	def drawWidth(self):
		return 10+(10*(len(self.icons)>0))
	
	def updateIcons(self):
		num = len(self.icons)
		
		w=20
		w2=w/2
		l=self.x-25+w2
		h=self.x+25-w2
		d=h-l
		
		r=15#(10*10+10*10)**0.5+0.5
		
		y=self.y-w
		if(num==1):
			self.canvas.coords(self.icons[0],(self.x,y))
			self.canvas.coords(self.iconcircles[0],(self.x-r,y-r,self.x+r-1,y+r-1))
			#elif(num==2):
			#	self.canvas.coords(self.icons[0],(self.x-w2,y))
			#	self.canvas.coords(self.icons[1],(self.x+w2,y))
			#	
			#	self.canvas.coords(self.iconcircles[0],(self.x-w2-r,y-r,self.x-w2+r,y+r)
			#	self.canvas.coords(self.iconcircles[1],(self.x+w2-r,y-r,self.x+w2+r,y+r)
		else:
			for i,image in enumerate(self.icons):
				x=l+i*d/(num-1)
				self.canvas.coords(image,(x,y))
				
				self.canvas.coords(self.iconcircles[i],(x-r,y-r,x+r-1,y+r-1))
				
		self.canvas.coords(self.oval,self.ovalCoords())
		
	def isMine(self,shape):
		return self.oval==shape or self.text==shape or shape in self.iconcircles
		
	def isMyNode(self,realNode):
		return self.realNode == realNode
		
	def generateDrawing(self):
		self.oval=self.canvas.create_oval(self.ovalCoords(),fill="pink",activefill="red")
		self.text=self.canvas.create_text((self.x,self.y),text=self.content)
		
	def ovalCoords(self):
		return (self.x-self.drawWidth(),self.y-self.drawWidth(),self.x+self.drawWidth(),self.y+self.drawWidth())
	
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
		
	def addIcon(self,icon,index,cook=True):
		if(cook):
			self.iconcircles.append(self.canvas.create_oval((0,0,0,0),fill="white"))
		else:
			self.iconcircles.append(self.canvas.create_oval((0,0,0,0),fill=get_color(index)))
			
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
		for circle in self.iconcircles:
			self.canvas.delete(circle)
		self.images=[]
		self.icons=[]
		self.iconcircles = []
		self.updateIcons()
		
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
		

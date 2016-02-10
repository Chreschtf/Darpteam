from xml.etree import ElementTree

from Node import *
from Graph import *
from Meal import *
from Car import *

class DataFileParser:
	def __init__(self, filename):
		self.filename = filename
		self.cars = []
		self.meals = []
		self.nodes = []
		self.depots = []
		
	
	def parseXML_File(self):
		data = ElementTree.parse( self.filename )
		
		
		neighbours = []
		for node in data.findall( "nodes/node" ):
			neighbours.append(  (int(node.attrib["nbr"]), [int(i) for i in node.attrib["neighbours"].split("|")])  )
			self.nodes.append( Node(int(node.attrib["i"]), int(node.attrib["j"]), int(node.attrib["nbr"])) )
		G = Graph( self.nodes, neighbours )
			
		
		for depot in data.findall( "depots/depot" ):
			self.depots.append( self.NodeWithIndex(int(depot.attrib["node"])) )
			
		
		for meal in data.findall( "meals/meal" ):
			self.meals.append( Meal(self.NodeWithIndex(int(meal.attrib["chef"])), self.NodeWithIndex(int(meal.attrib["client"])),\
									 drt, int(meal.attrib["ddt"]), int(meal.attrib["deviation"])) )
		
		
		for car in data.findall( "cars/car" ):
			self.cars.append( Car(car.attrib["maxCharge"], car.attrib["start"], car.attrib["duration"], self.depots[0], G) ) # utiliser plusieurs depots ?
			
			
			
			
	def NodeWithIndex(self, index):
		i = 0
		while i < len(self.nodes) and self.nodes[i].index != index:
			i += 1
		return self.nodes[i]
		
		
	def getNodes(self):
		return self.nodes
		
	def getMeals(self):
		return self.meals
		
	def getDepots(self):
		return self.depots
		
	def getCars(self):
		return self.cars
		
		

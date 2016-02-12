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
		self.graph = None
		
	
	def parseXML_File(self):
		tree = ElementTree.parse( self.filename )
		root = tree.getroot()
		
		neighbours = []
		for node in root.iter( "node" ):
			neighbours.append(  [int(node.attrib["nbr"]), [int(i) for i in node.attrib["neighbours"].split("|")]] )
			self.nodes.append( Node(int(node.attrib["i"]), int(node.attrib["j"]), int(node.attrib["nbr"])) )
		for elem in neighbours:
			newList = []
			for index in elem[1]:
				newList.append(self.NodeWithIndex(index))
			elem[0] = self.NodeWithIndex(elem[0])
			elem[1] = newList

		self.graph = Graph( len(self.nodes), "FromFile", self.nodes, neighbours )
			
		
		for depot in root.iter( "depot" ):
			self.depots.append( self.NodeWithIndex(int(depot.attrib["node"])) )
			
		
		for meal in root.iter( "meal" ):
			chef = self.NodeWithIndex(int(meal.attrib["chef"]))
			client = self.NodeWithIndex(int(meal.attrib["client"]))
			self.meals.append( Meal(chef, client, self.graph.dist(chef, client), int(meal.attrib["ddt"]), int(meal.attrib["deviation"])) )
		
		
		for car in root.iter( "car" ):
			self.cars.append( Car(car.attrib["maxCharge"], car.attrib["start"], car.attrib["duration"], self.depots[0], self.graph) ) # utiliser plusieurs depots ?
			
			
			
			
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

	def getGraph(self):
		return self.graph
		
		

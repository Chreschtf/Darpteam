import xml.etree.cElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment

#temporary:
from DataFileParser import *

class DataFileWriter:
	def __init__(self, filename, cars, meals, nodes, depots):
		self.cars = cars
		self.meals = meals
		self.nodes = nodes
		self.depots = depots
		self.filename = "../DataFiles/"+filename+'.xml'
		
	def writeXML_File(self):
		root = Element("root")
		root.append(Comment("Data for initialising a Darp scenario"))
		
		cars = SubElement(root, "Cars")
		for car in self.cars:
			carElem = SubElement(cars, "car", attrib={"maxCharge":car[0], "start":car[1], "duration":car[2]}) # add a name ?
			
			
		meals = SubElement(root, "Meals")
		for meal in self.meals:
			mealElem = SubElement(meals, "meal", attrib={"ddt":meal[0], "deviation":meal[1], "chef":meal[2], "client":meal[3]}) # add a name ?
			
		
		nodes = SubElement(root, "Nodes")
		for node in self.nodes:
			nodeElem = SubElement(nodes, "node", attrib={"nbr":node[0], "i":node[1], "j":node[2], "neighbours":node[3]})
		
		
		depots = SubElement(root, "Depots")
		for depot in self.depots:
			depotElem = SubElement(depots, "depot", attrib={"node":depot[0]})
			
			
		tree = ET.ElementTree(root)
		tree.write(self.filename)
		
		
"""
if __name__ == "__main__":
	filename = "testFile"
	cars = [("4","5","20"),("1","2","8")]
	meals = [("2","3","0","1"), ("8", "7", "0", "2")]
	nodes = [("0", "1", "2", "1|2"), ("1", "4", "2", "0"), ("2", "0", "3", "0")]
	depots = [("1")]
	
	DFW = DataFileWriter(filename, cars, meals, nodes, depots)
	DFW.writeXML_File()
	
	DFP = DataFileParser(DFW.filename)
	DFP.parseXML_File()
	print()
	print()

"""
	

from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.rdf.Resource import Resource
from SeasObjects.rdf.Property import Property
from SeasObjects.model.Obj import Obj
from SeasObjects.model.Waypoint import Waypoint
from rdflib.namespace import RDF

import traceback

class Waypoints(Obj):
	
	def __init__(self, uri = None):
		Obj.__init__(self, uri)
		self.setType(RESOURCE.WAYPOINTS)
		self.wps = []
	
	def hasWaypoints(self):
		return len(self.wps) > 0
	
	def getWaypoints(self):
		return self.wps
	
	def setWaypoints(self, wps):
		self.wps = wps
	
	def addWaypoint(self, wp):
		self.wps.append(wp)
	
	def serialize(self, model):
		waypoints = super(Waypoints, self).serialize(model)
		
		if self.hasWaypoints():
			rdfList = model.createOrderedList()
			rdfList.add_items(self.wps)
			
			listContainer = model.createResource()
			listContainer.addProperty(Property(RDF.first), rdfList)

			waypoints.addProperty(model.createProperty( PROPERTY.LIST ), listContainer)

		return waypoints
	
	def parse(self, resource):
		if isinstance(resource, Resource):
			if not resource.isAnon():
				waypoints = Waypoints(resource.toString())
			else:
				waypoints = Waypoints()
			waypoints.clearTypes()

			for statement in resource.findProperties():
				# parse statement
				waypoints.parse(statement)
	
			return waypoints
		
		else:
			statement = resource
			# get predicate
			predicate = str(statement.getPredicate())

			# waypoints
			if predicate == PROPERTY.LIST:
				try:
					self.setWaypoints(statement.getResource().toList(Waypoint))
				except:
					print "Unable to interpret seas:list value as a resource for Waypoints."
					traceback.print_exc() 
				return
			# pass on to Object
			super(Waypoints, self).parse(statement)


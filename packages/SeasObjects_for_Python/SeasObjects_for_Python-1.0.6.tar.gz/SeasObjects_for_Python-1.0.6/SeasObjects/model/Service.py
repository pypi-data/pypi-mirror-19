from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.model.AbstractEntity import AbstractEntity
from SeasObjects.rdf.Resource import Resource
from SeasObjects.model.Obj import Obj

import traceback


class Service(AbstractEntity):

	def __init__(self, uri = None):
		AbstractEntity.__init__(self, uri)
		self.managedBy = None
		self.setType(RESOURCE.SERVICE);

	def hasManagedBy(self):
		return self.managedBy is not None

	def setManagedBy(self, o):
		if isinstance(o, Obj):
			self.managedBy = o
		else:
			self.managedBy = Obj(o)
		
	def getManagedBy(self):
		return self.managedBy
	
	def serialize(self, model):
		service = super(Service, self).serialize(model)
		
		# set system uri
		if self.hasManagedBy():
			service.addProperty(model.createProperty( PROPERTY.ISMANAGEDBY ), self.managedBy.serialize(model))

		return service
	
	
	def parse(self, resource):
		from SeasObjects.model.Obj import Obj
		from SeasObjects.model.InterfaceAddress import InterfaceAddress
		
		if isinstance(resource, Resource):
			if not resource.isAnon():
				service = Service(resource.toString())
			else:
				service = Service()
			service.clearTypes()
	
			for statement in resource.findProperties():
				service.parse(statement)
			
			return service
		
		else:
			statement = resource
			# get predicate
			predicate = str(statement.getPredicate())

			# managedby
			if predicate == PROPERTY.ISMANAGEDBY:
				try:
					self.managedBy = Obj().parse(statement.getResource())
				except:
					print "Unable to interpret seas:isManagedBy value as resource."
					traceback.print_exc() 

			# pass on to Object
			super(Service, self).parse(statement)


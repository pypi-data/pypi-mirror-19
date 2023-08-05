from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.model.Obj import Obj
from SeasObjects.rdf.Variant import Variant

from rdflib import URIRef
import traceback


class ValueObject(Obj):

	def __init__(self, uri = None, quantity = None, unit = None, value = None, maximum = None, minimum = None):
		Obj.__init__(self, uri)
		if quantity is not None and not isinstance(quantity, URIRef): quantity = URIRef(quantity)
		if unit is not None and not isinstance(unit, URIRef): unit = URIRef(unit)
		if value is not None and not isinstance(unit, Variant): value = Variant(value)
		self.quantity = quantity
		self.unit = unit
		self.value = value
		self.maximum = maximum
		self.minimum = minimum
		self.setType(RESOURCE.VALUEOBJECT)

	def serialize(self, model):
		valueObject = super(ValueObject, self).serialize(model)

		# quantity
		if self.hasQuantity():
			quantity = model.createResource(self.quantity)
			valueObject.addProperty(model.createProperty( PROPERTY.QUANTITYKIND ), self.quantity)
		
		# unit
		if self.hasUnit():
			unit = model.createResource(self.unit)
			valueObject.addProperty(model.createProperty( PROPERTY.UNIT ), self.unit)

		# value
		if self.hasValue():
			valueObject.addProperty(model.createProperty( PROPERTY.RDF_VALUE ), self.value.serialize(model))

		return valueObject
	
	
	def parse(self, resource):
		from SeasObjects.rdf.Resource import Resource
		
		if isinstance(resource, Resource):
			if not resource.isAnon():
				valueObject = ValueObject(resource.toString())
			else:
				valueObject = ValueObject()
			valueObject.clearTypes()
		
			for statement in resource.findProperties():
				valueObject.parse(statement)
			
			return valueObject
		
		else:
			statement = resource
		
			# get predicate
			predicate = str(statement.getPredicate())
			
			# quantity
			if predicate == PROPERTY.QUANTITYKIND:
				try:
					self.setQuantity(statement.getResource().toString());
				except:
					print "Unable to interpret seas:quantity value as resource."
					traceback.print_exc() 

			# unit
			if predicate == PROPERTY.UNIT:
				try:
					self.setUnit(statement.getResource().toString())
				except:
					print "Unable to interpret seas:unit value as resource."
					traceback.print_exc() 
			
			# value
			if predicate == PROPERTY.RDF_VALUE:
				self.setValue(Variant().parse(statement))

			# pass on to Obj
			super(ValueObject, self).parse(statement)
		

	def hasQuantity(self):
		return self.quantity is not None

	def getQuantity(self):
		return self.quantity
	
	def setQuantity(self, quantity):
		self.quantity = URIRef(quantity)

	def hasUnit(self):
		return self.unit is not None

	def getUnit(self):
		return self.unit
	
	def setUnit(self, unit):
		self.unit = URIRef(unit)

	def hasValue(self):
		return self.value is not None
	
	def getValue(self):
		return self.value

	def setValue(self, value):
		self.value = value

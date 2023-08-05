from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.model.ValueObject import ValueObject
from SeasObjects.rdf.Variant import Variant

from rdflib import URIRef
import traceback


class Capacity(ValueObject):

	def __init__(self, uri = None, quantity = None, unit = None, value = None, maximum = None, system_of_interest = None):
		ValueObject.__init__(self, uri = uri, quantity = quantity, unit = unit, value = value, maximum = maximum)
		self.automatic_percentage_calculation = True
		self.system_of_interest = system_of_interest
		self.percentage = None
		self.setType(RESOURCE.CAPACITY)
	
	def serialize(self, model):
		capacity = super(Capacity, self).serialize(model)
		
		# percentage
		if self.automatic_percentage_calculation:
			self.calculatePercentage()
		if self.hasPercentage():
			capacity.addProperty(model.createProperty( PROPERTY.PERCENTAGE ), self.percentage.serialize(model))

		# systemOfInterest
		if self.hasSystemOfInterest():
			capacity.addProperty(model.createProperty( PROPERTY.SYSTEMOFINTEREST ), self.system_of_interest.serialize(model))
		
		return capacity
	
	
	def parse(self, resource):
		from SeasObjects.model.SystemOfInterest import SystemOfInterest
		from SeasObjects.rdf.Variant import Variant
		from SeasObjects.rdf.Resource import Resource
		
		if isinstance(resource, Resource):
			if not resource.isAnon():
				capacity = Capacity(resource.toString())
			else:
				capacity = Capacity()
			capacity.clearTypes()
	
			for statement in resource.findProperties():
				capacity.parse(statement)
			
			return capacity
		
		else:
			statement = resource
			
			# get predicate
			predicate = str(statement.getPredicate())
			
			# quantity
			if predicate == PROPERTY.PERCENTAGE:
				try:
					self.setPercentage(Variant().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:percentage value as resource."
					traceback.print_exc() 

			# unit
			if predicate == PROPERTY.SYSTEMOFINTEREST:
				try:
					self.setSystemOfInterest(SystemOfInterest().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:systemOfInterest value as resource."
					traceback.print_exc() 
			
			# pass on to ValueObject
			super(Capacity, self).parse(statement)

	def hasPercentage(self):
		return self.percentage is not None

	def getPercentage(self):
		return self.percentage
	
	def getPercentageAsInteger(self):
		try:
			return self.percentage.getValue()
		except:
			return None
	
	def getPercentageAsDouble(self):
		try:
			return self.percentage.getValue()
		except:
			return None
		
	def setPercentage(self, p):
		self.percentage = p

	def hasSystemOfInterest(self):
		return self.system_of_interest is not None

	def getSystemOfInterest(self):
		return self.system_of_interest
	
	def setSystemOfInterest(self, s):
		self.system_of_interest = s

	def hasMaximum(self):
		return self.maximum is not None

	def getMaximum(self):
		return self.maximum
	
	def setMaximum(self, m):
		self.maximum = m
		
	def enableAutomaticPercentageCalculation(self):
		automatic_percentage_calculation = True
		
	def disableAutomaticPercentageCalculation(self):
		automatic_percentage_calculation = False
		
	def calculatePercentage(self):
		if self.hasValue and self.hasMaximum():
			v = self.value.getValue()
			m = self.maximum.getValue()
			if m != 0:
				self.setPercentage(Variant(v/m*100))
				return True;
		return False

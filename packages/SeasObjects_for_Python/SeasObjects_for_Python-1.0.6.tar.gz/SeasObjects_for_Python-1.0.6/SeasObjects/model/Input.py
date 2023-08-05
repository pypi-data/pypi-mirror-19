from SeasObjects.model.Evaluation import Evaluation
from SeasObjects.rdf.Resource import Resource
from SeasObjects.rdf.Statement import Statement
from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.common.PROPERTY import PROPERTY

import traceback

class Input(Evaluation):
	TYPE_DATA = 0
	TYPE_REFERENCE = 1
		
	def __init__(self, uri = None, inputType = 0):
		Evaluation.__init__(self, uri)
		self.inputType = inputType
		self.outputValues = []
		self.setType(RESOURCE.INPUT)
	
	def serialize(self, model):
		input = super(Input, self).serialize(model)
		
		# outputs
		for ov in self.outputValues:
			input.addProperty(model.createProperty( PROPERTY.OUTPUTVALUES ), ov.serialize(model))
			
		return input

	def parse(self, resource):
		from SeasObjects.model.ValueObject import ValueObject
		
		if isinstance(resource, Resource):
			if not resource.isAnon():
				input = Input(resource.toString())
			else:
				input = Input()
			input.clearTypes()
			
			for i in resource.findProperties():
				# pass on to Evaluation
				input.parse(i)
			
			return input
		else:
			statement = resource
			predicate = str(statement.getPredicate())
			
			# output vals
			if  predicate == PROPERTY.OUTPUTVALUES:
				try:
					self.addOutputValue(ValueObject().parse(statement.getResource()));
				except:
					print "Unable to interpret seas:outputValues value as resource."
					traceback.print_exc()
				return

			super(Input, self).parse(resource)

	def getInputType(self):
		return self.inputType
	
	def setInputType(self, inputType):
		self.inputType = inputType

	def hasOutputValue(self):
		return len(self.outputValues) > 0

	def getOutputValues(self):
		return self.outputValues
	
	def setOutputValue(self, ov):
		self.outputValues = [ov]

	def addOutputValue(self, ov):
		self.outputValues.append(ov)
	

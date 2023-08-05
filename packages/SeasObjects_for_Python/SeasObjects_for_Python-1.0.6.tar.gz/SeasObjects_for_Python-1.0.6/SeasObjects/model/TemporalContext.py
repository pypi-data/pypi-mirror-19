from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.model.Obj import Obj
from SeasObjects.rdf.Variant import Variant
from SeasObjects.common.Tools import Tools

from dateutil import parser
import datetime
from SeasObjects.rdf.types import *
from rdflib import XSD

import traceback

class TemporalContext(Obj):

	def __init__(self, uri = None):
		Obj.__init__(self, uri)
		self.start = None
		self.end = None
		self.duration = None
		self.during = None
		self.setType(RESOURCE.TEMPORALCONTEXT)

	def serialize(self, model):
		temporalContext = super(TemporalContext, self).serialize(model);
		
		# start
		if self.hasStart():
			temporalContext.addProperty(model.createProperty( PROPERTY.START ), model.createLiteral(self.getStart().getValue()))

		# end
		if self.hasEnd():
			temporalContext.addProperty(model.createProperty( PROPERTY.END ), model.createLiteral(self.getEnd().getValue()))

		# duration
		if self.hasDuration():
			temporalContext.addProperty(model.createProperty( PROPERTY.DURATION ), model.createTypedLiteral(self.getDuration(), XSD.duration))

		# during
		if self.hasDuring():
			temporalContext.addProperty(model.createProperty( PROPERTY.DURING ), model.createResource(self.getDuring()))

		return temporalContext


	def  parse(self, resource):
		if not resource.isAnon():
			temporalContext = TemporalContext(resource.toString())
		else:
			temporalContext = TemporalContext()
		temporalContext.clearTypes()

		for statement in resource.findProperties():
			# get predicate
			predicate = str(statement.getPredicate())

			# start
			if predicate == PROPERTY.START:
				s = statement.getObject().toPython()
				if not isinstance(s, datetime.datetime):
					s = parser.parse(s)
				temporalContext.setStart(s)
				
			# end
			if predicate == PROPERTY.END:
				e = statement.getObject().toPython()
				if not isinstance(e, datetime.datetime):
					e = parser.parse(e)
				temporalContext.setEnd(e)
				
			# duration
			if predicate == PROPERTY.DURATION:
				try:
					temporalContext.setDuration(statement.getString())
				except:
					print "Unable to interpret seas:duration value as literal."
					traceback.print_exc() 
				continue

			# during
			if predicate == PROPERTY.DURING:
				try:
					temporalContext.setDuring(statement.getResource().toString())
				except:
					print "Unable to interpret seas:during value as resource."
					traceback.print_exc()
				continue

			# pass on to Object
			super(TemporalContext, temporalContext).parse(statement)
		
		return temporalContext


	def hasStart(self):
		return self.start is not None
	
	def getStart(self):
		return self.start

	def setStart(self, start):
		self.start = Variant(start)

	def hasEnd(self):
		return self.end is not None
	
	def getEnd(self):
		return self.end

	def setEnd(self, end):
		self.end = Variant(end)

	def hasDuration(self):
		return self.duration is not None

	def getDuration(self):
		return self.duration

	def setDuration(self, duration):
		self.duration = duration

	def hasDuring(self):
		return self.during is not None

	def getDuring(self):
		return self.during

	def setDuring(self, during):
		self.during = during

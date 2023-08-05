from SeasObjects.factory.Factory import Factory
from SeasObjects.rdf.Property import Property
from SeasObjects.rdf.Resource import Resource
from SeasObjects.rdf.LinkedList import LinkedList
from SeasObjects.rdf.OrderedList import OrderedList
from SeasObjects.rdf.ItemizedList import ItemizedList
from SeasObjects.rdf.NudeList import NudeList
from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.CONTENTTYPES import CONTENTTYPE
from SeasObjects.common.ClassMapper import ClassMapper

from SeasObjects.seasexceptions.NotFoundException import NotFoundException
from rdflib import URIRef
from rdflib.namespace import RDF

import traceback
import datetime


class Tools(object):

	def __init__(self):
		self.mapper = ClassMapper()
		
	def toString(self, element, serialization):
		model = Factory().createModel()
		
		if isinstance(element, list) or isinstance(element, LinkedList) or isinstance(element, OrderedList) or isinstance(element, ItemizedList) or isinstance(element, NudeList):
			# Raw top level list. We need some blank node to hold the list
			top_element = Resource(model = model)
			top_element.addProperty(Property(RDF.first), element)
			self.addRecursivelyToModel(top_element, model)
		else:
			self.addRecursivelyToModel(element, model)
		
		# serialize
		messageBody = ""
		try:
			messageBody = model.serialize(format=serialization)
		except:
			print "Exception while converting model into string"
			traceback.print_exc()

		return messageBody

	def fromString(self, strng, serialization = None):
		model = Factory().createModel()
		try:
			model.parse(data = strng, format=serialization)
		except:
			print "Could not parse the input into a model"
			traceback.print_exc()
		return model
	
	def fromFile(self, filename, serialization):
		model = Factory.createModel()

		try:
			f = open(filename)
			model.parse(file = filename, format=serialization)
			f.close()
		except:
			print "Could not read the file into a model"
			traceback.print_exc()
			
		return model
	
	def fromStringAsObj(self, strng, serialization = None, isType = None):
		model = self.fromString(strng, serialization = serialization)
		if isType is None:
			node, isType = self.getTopNode(model)
		
		res = self.getResourceByType(isType, model)
		cm = ClassMapper()
		obj = cm.getClass([str(isType)])()
		sl = node.findProperties()
		for s in sl:
			obj.parse(s)
		return obj;
	
	def fromStringAsList(self, strng, serialization = None, isType = None):
		model = self.fromString(strng, serialization = serialization)
		sl = model.listStatements(subject = None, predicate = URIRef(RDF.first), object = None)
		list_container = []
		# Find the "orphan" rdf.first node, this is the starting point of all lists
		for s in sl:
			ss = model.listStatements(subject = None, predicate = None, object = s.getSubject())
			if len(ss) == 0:
				model.parse_list(list_container, parent_node = s.getSubject(), first = s.getObject())
				break
		
		return list_container
		
	def getSerializationForContentType(self, content_type):
		if CONTENTTYPE.mapping.has_key(content_type):
			return CONTENTTYPE.mapping[content_type]
		return "Unknown"

	def addRecursivelyToModel(self, resource, model):
		from SeasObjects.model.Obj import Obj
		
		# add this level statements
		if isinstance(resource, Obj):
			model.add(resource.serialize(model))
		elif isinstance(resource, list):
			for item in resource:
				self.addRecursivelyToModel(item, model)
		else:
			model.add(resource)

	
		
	"""
	 Convert Python datetime to xsd:dateTime string
	 @param dateTime timestamp to convert
	 @return xsd:dateTime stype string
	"""
	def dateToString(self, date_time):
		ret = None
		try:
			ret = date_time.strftime("%Y-%m-%dT%H:%M:%S")
		except:
			print "Error while converting zoned datetime to ISO offset datetime string"
		return ret
	

	def stringToDate(self, date_str):
		date = None
		try:
			date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
		except:
			print "Error while converting ISO offset datetime string to zoned datetime"
		return date
		

	def stripUri(self, uri):
		stripped = uri
		splits = uri.split("#", 1)
		if len(splits) > 1:
			stripped = splits[1]
		return stripped;
		
	def getResourceByType(self, type, model):
		return model.findSubject(URIRef(PROPERTY.RDF_TYPE), URIRef(type))

	"""
	def getResourceByType(self, type, model):
		typeResource = model.createResource(type)
		typeProperty = model.createProperty(PROPERTY.RDF_TYPE)

		s = model.listStatements(None, typeProperty, typeResource)
		if len(s) > 0:
			r = Resource(model, s.getSubject())
			return r
		else:
			raise NotFoundException("Could not find resource by type " + type + " from the provided model.")
	"""
	
	def getResourceType(self, resource):
		object = resource.getPropertyResourceValue(resource.getModel().createProperty(PROPERTY.RDF_TYPE))
		if ( object is not None ):
			return object.toString()
		return None

	def getResourceTypes(self, resource):
		types = []
		for statement in resource.findProperty(resource.getModel().createProperty(PROPERTY.RDF_TYPE)):
			types.append(statement.getResource().toString())
		return types

	def getResourceClass(self, resource, default = None):
		types = self.getResourceTypes(resource)
		return self.mapper.getClass(types, default = default)

	def getTopNode(self, model):
		# Find the top node of a received structure. To do this, find all triples where
		# the subject is not the object of anything.
		# These subjects are the resources of orphan nodes. Because we are eventually
		# looking for the RDF type of the objects, it is enough to iterate the nodes
		# that contain an RDF type attribute
		nodeType = None
		node = None
		sl = model.listStatements(subject = None, predicate = URIRef(PROPERTY.RDF_TYPE), object = None)
		for s in sl:
			nodeType = s.getObject()
			ss = model.listStatements(subject = None, predicate = None, object = s.getSubject())
			if len(ss) == 0:
				node = Resource(model = model, node = s.getSubject())
				break
		if node is not None:
			return node, nodeType
		raise NotFoundException("Could not find any orphan objects from the provided model.")
		

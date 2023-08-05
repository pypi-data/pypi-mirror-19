from SeasObjects.model.Ability import Ability
from SeasObjects.common.RESOURCE import RESOURCE

class Controllability(Ability):

	def __init__(self, uri = None):
		Ability.__init__(self, uri)
		self.setType(RESOURCE.CONTROLLABILITY)

	def parse(self, resource):
		if not resource.isAnon():
			controllability = Controllability(resource.toString())
		else:
			controllability = Controllability()
		controllability.clearTypes()

		for i in resource.findProperties():
			# parse statement
			controllability.parse(i)

		return controllability;


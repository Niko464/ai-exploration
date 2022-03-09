from common.geneticAlgo.GeneticAlgo import *
from . import MemberFlappy


class GeneticFlappy(GeneticAlgo):
	def __init__(self, popSize):
		super().__init__(populationSize=popSize,
						mutationProb=0.2,
						shouldCrossOver=True,
						amtRandomMembersPerGen=2)

	def _createRandomMember(self):
		return MemberFlappy()

	def _foundNewFitnessRecord(self):
		pass
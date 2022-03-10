from common.geneticAlgo.GeneticAlgo import *
from . import MemberFlappy


class GeneticFlappy(GeneticAlgo):
	def __init__(self, popSize):
		super().__init__(
			populationSize=popSize,
			mutationProb=0.2,
			shouldCrossOver=True,
			amtRandomMembersPerGen=2)
		self.env = FlappyEnvironment(popSize)

	def _createRandomMember(self):
		return MemberFlappy()

	def _foundNewFitnessRecord(self):
		pass

	def _interactWithEnvironment(self):
		observations = env.reset()
		done = False
		dataforAi = []
		datafromAi = [ai.predict(observations[index]) for index, ai in enumerate(self.population)]
		while not done:
			observations, rewards, done, _ = env.step()

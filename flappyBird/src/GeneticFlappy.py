from common.geneticAlgo.GeneticAlgo import *
from src.MemberFlappy import *
from src.FlappyEnvironment import *


class GeneticFlappy(GeneticAlgo):
	def __init__(self, popSize):
		super().__init__(
			populationSize=popSize,
			mutationProb=0.2,
			shouldCrossOver=True,
			amtRandomMembersPerGen=2,
			showEvery=5)
		self.env = FlappyEnvironment(popSize)

	def _createRandomMember(self):
		return MemberFlappy()

	def _foundNewFitnessRecord(self, recordMember):
		recordMember.neuralNetwork.saveBrainToFile(f"brains/GEN-{self.currGen} Fitness-{recordMember.fitness}")

	def _interactWithEnvironment(self):
		#Calculate the game
		observations = self.env.reset(self.currGen % self.showEvery == 0)
		done = False
		rewards = []
		dataforAi = []
		while not done:
			datafromAi = [ai.predict(observations[index]) for index, ai in enumerate(self.population)]
			observations, rewards, done, _ = self.env.step(datafromAi)

		#Calc fitness for each member since I didn't specify a FitnessFunc to the super() class
		for index, member in enumerate(self.population):
			member.fitness = rewards[index]

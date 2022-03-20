from common.geneticAlgo.GeneticAlgo import *
from src.MemberFlappy import *
from src.FlappyEnvironment import *


class GeneticFlappy(GeneticAlgo):
	def __init__(self, name: str, popSize: int, showEvery: int, statsEvery: int, trainFromFile = None):
		super().__init__(
			name=name,
			populationSize=popSize,
			mutationProb=0.2,
			shouldCrossOver=True,
			amtRandomMembersPerGen=2,
			goalFitness=5000,
			showEvery=showEvery,
			statsEvery=statsEvery,
			trainFromFile=trainFromFile)
		self.env = FlappyEnvironment(popSize)

	def _createMember(self, name: str, existingFileSave = None):
		toReturn = MemberFlappy(name, self.currGen)
		if (existingFileSave != None):
			toReturn.neuralNetwork.loadBrainFromFile(existingFileSave)
		return toReturn

	def _foundNewFitnessRecord(self, recordMember):
		recordMember.saveToFile()

	def _interactWithEnvironment(self):
		#Calculate the game
		observations = self.env.reset(self.currGen % self.showEvery == 0)
		done = False
		rewards = []
		dataforAi = []
		while not done:
			datafromAi = [ai.predict(observations[index]) for index, ai in enumerate(self.population)]
			observations, rewards, done, _ = self.env.step(datafromAi)

		#Stats
		self.rewardsListAllGens.append(np.mean(rewards))

		#Calc fitness for each member since I didn't specify a FitnessFunc to the super() class
		for index, member in enumerate(self.population):
			member.fitness = rewards[index]
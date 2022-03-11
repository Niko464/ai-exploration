import matplotlib.pyplot as plt

from common.geneticAlgo.GeneticAlgo import *
from src.MemberFlappy import *
from src.FlappyEnvironment import *


class GeneticFlappy(GeneticAlgo):
	def __init__(self, popSize: int, showEvery: int, statsEvery: int):
		super().__init__(
			populationSize=popSize,
			mutationProb=0.2,
			shouldCrossOver=True,
			amtRandomMembersPerGen=2,
			showEvery=showEvery,
			statsEvery=statsEvery)
		self.env = FlappyEnvironment(popSize)
		self.statistics = []
		self.otherStatistics = {"gen": [], "avg": [], "max": [], "min": []}

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

		#Stats
		self.statistics.append(np.mean(rewards))
		if (self.currGen % self.statsEvery == 0):
			avg = sum(self.statistics[-self.statsEvery:]) / self.statsEvery
			self.otherStatistics["gen"].append(self.currGen)
			self.otherStatistics["max"].append(max(self.statistics[-self.statsEvery:]))
			self.otherStatistics["min"].append(min(self.statistics[-self.statsEvery:]))
			self.otherStatistics["avg"].append(avg)

		#Calc fitness for each member since I didn't specify a FitnessFunc to the super() class
		for index, member in enumerate(self.population):
			member.fitness = rewards[index]

	def showStats(self):
		plt.plot(self.otherStatistics["gen"], self.otherStatistics["avg"], label="average rewards")
		plt.plot(self.otherStatistics["gen"], self.otherStatistics["min"], label="min rewards")
		plt.plot(self.otherStatistics["gen"], self.otherStatistics["max"], label="max rewards")
		plt.legend(loc=4)
		plt.show()
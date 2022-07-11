from common.geneticAlgo.GeneticAlgo import *
from src.MPRMember import *
from src.MPREnvironment import *


class MPRGenetic(GeneticAlgo):
	def __init__(self, name: str, popSize: int, showEvery: int, statsEvery: int, amtRandomMembersPerGen: int, trainFromFile = None):
		super().__init__(
			name=name,
			populationSize=popSize,
			mutationProb=0.4,
			shouldCrossOver=True,
			amtRandomMembersPerGen=amtRandomMembersPerGen,
			goalFitness=5000000,
			showEvery=showEvery,
			statsEvery=statsEvery,
			trainFromFile=trainFromFile)
		self.env = MPREnvironment(	amtPlayers=popSize,
									saveCpFile="",
									loadCpFile="maps/" + "map" + ".map")

	def _createMember(self, name: str, existingFileSave = None):
		toReturn = MPRMember(name, self.currGen)
		if (existingFileSave != None):
			toReturn.neuralNetwork.loadBrainFromFile(existingFileSave)
		return toReturn

	def _foundNewFitnessRecord(self, recordMember):
		recordMember.saveToFile()

	def _interactWithEnvironment(self):
		print("Another generation starts")
		#Calculate the game
		observations = self.env.reset(self.currGen % self.showEvery == 0)
		done = False
		rewards = []
		dataforAi = []
		while not done:
			datafromAi = [member.predict(observations[index]) for index, member in enumerate(self.population)]
			observations, rewards, done, _ = self.env.step(datafromAi)
		#Stats
		self.rewardsListAllGens["min"].append(min(rewards))
		self.rewardsListAllGens["max"].append(max(rewards))
		self.rewardsListAllGens["avg"].append(np.mean(rewards))

		#Calc fitness for each member since I didn't specify a FitnessFunc to the super() class
		for index, member in enumerate(self.population):
			member.fitness = rewards[index]
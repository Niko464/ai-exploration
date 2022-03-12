from copy import deepcopy

from common.geneticAlgo.Member import *
from common.neuralNetwork.NeuralNetwork import *
from common.neuralNetwork.ActivationFuncs import *

class MemberFlappy(Member):
	def __init__(self, name: str, gen: int):
		super().__init__(name, gen)
		self.neuralNetwork = NeuralNetwork()
		self.relu = ActivationRelu()
		self.neuralNetwork.addLayer(5, 6, self.relu)
		self.neuralNetwork.addLayer(6, 1, self.relu)
		self.randomize()

	def randomize(self):
		self.neuralNetwork.randomize()

	def crossover(self, other):
		self.neuralNetwork.crossover(other.neuralNetwork)

	def mutate(self):
		self.neuralNetwork.mutate()

	def predict(self, data):
		return self.neuralNetwork.forward(data)

	def saveToFile(self):
		self.neuralNetwork.saveBrainToFile(f"brains/{self.name}-Gen_{self.gen}-Fitness_{self.fitness}")
from copy import deepcopy

from common.geneticAlgo.Member import *
from common.neuralNetwork.NeuralNetwork import *
from common.neuralNetwork.ActivationFuncs import *
from common.geneticAlgo.Genes import *

class MemberFlappy(Member):
	def __init__(self):
		super().__init__()
		self.neuralNetwork = NeuralNetwork()
		self.relu = ActivationRelu()
		self.neuralNetwork.addLayer(4, 6, self.relu)
		self.neuralNetwork.addLayer(6, 1, self.relu)
		self.neuralNetwork.finishSetup()
		self.randomize()

	#TODO
	def randomize(self):
		pass

	def clone(self):
		newMember = deepcopy(self)
		return newMember

	def crossover(self, other):
		#TODO
		newGenes = self.genes.crossover(other.genes)

	def mutate(self):
		print("BEFORE")
		print("Genes:")
		print(self.neuralNetwork.genes)
		print("Network:")
		self.neuralNetwork.printNetwork()
		self.neuralNetwork.genes.mutate(low=-1.0, high=1.0)
		print("AFTER")
		print("Genes:")
		print(self.neuralNetwork.genes)
		print("Network:")
		self.neuralNetwork.printNetwork()

	def predict(self, data):
		return self.neuralNetwork.forward(data)
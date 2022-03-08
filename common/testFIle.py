
import numpy as np
from geneticAlgo.Genes import * 

"""
class MyFitness(FitnessFunc):
	def __init__(self):
		super().__init__()

	def fitness(self, member):
		return 15

class MyGeneticAlgo(GeneticAlgo):
	def __init__(self, popSize, fitnessFunc, mutationProb):
		super().__init__(popSize, fitnessFunc, mutationProb)

	def createRandomPopulation(self):
		self.population = ["a" for x in range(5)]
"""


def main():
	"""
	myFitness = MyFitness()
	test = MyGeneticAlgo(popSize=5, fitnessFunc=myFitness, mutationProb=0.1)
	print(test.population)
	"""

	"""
	relu = ActivationRelu()
	myNN = NeuralNetwork()
	myNN.addLayer(4, 5, relu)
	myNN.addLayer(5, 2, relu)
	output = myNN.forward(np.array([.1, .1, .1, .1]))
	print(output)
	"""
	geneA = Genes(np.random.uniform(low=0.0, high=10.0, size=(10)))
	geneB = Genes(np.random.uniform(low=0.0, high=10.0, size=(10)))
	child = geneA.crossover(geneB)
	print(geneA)
	print(geneB)
	print(child)

if __name__ == "__main__":
	main()
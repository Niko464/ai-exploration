import numpy as np
from . LayerDense import *
from . ActivationFuncs import *
from common.geneticAlgo.Genes import *

class NeuralNetwork:
	def __init__(self):
		self.layers = []
		self.activationFuncs = []
		self.finishedSetup = False

	def addLayer(self, amtInputs:int, amtNeurons: int, activationFunc: ActivationFunc):
		newLayer = LayerDense(amtInputs, amtNeurons)
		newLayer.randomize()
		self.layers.append(newLayer)
		self.activationFuncs.append(activationFunc)

	def finishSetup(self):
		startingData = np.array([])
		for layer in self.layers:
			#This is because we accept "batches"
			for weights in layer.getWeights():
				startingData = np.concatenate([startingData, weights])
			for biases in layer.getBiases():
				startingData = np.concatenate([startingData, biases])
		self.genes = Genes(startingData)
		print(f"finishedSetup: {startingData}")

	def loadGenes(self):
		currIndex = 0
		for layer in self.layers:
			totalWeightsList = np.array([])
			totalBiasesList = np.array([])
			for i in range(layer.amtInputs):
				weightsList = np.array([])
				for j in range(layer.amtNeurons):
					weightsList.append(self.genes.data[currIndex])
					currIndex += 1
				totalWeightsList.append(weightsList)

			for i in range(layer.amtNeurons):
				biasList = np.array([])
				for j in range(layer.amtNeurons):
					biasList.append(self.genes.data[currIndex])
					currIndex += 1
				totalBiasesList.append(biasList)

			layer.setWeights(totalWeightsList)
			layer.setBiases(totalBiasesList)
		print("totalWeightsList")
		print(totalWeightsList)
		print("totalBiasesList")
		print(totalBiasesList)

			


	def printNetwork(self):
		for index, layer in enumerate(self.layers):
			print(f"LAYER {index}")
			print("weights")
			print(layer.getWeights())
			print("biases")
			print(layer.getBiases())
			print("\n\n")


	# returns all weights and biases
	def getBrain(self):
		brain = []
		for layer in self.layers:
			layerData = [layer.getWeights(), layer.getBiases()]
			brain.append(layerData)
		return brain

	def loadBrain(self, weightsAndbiasesArray):
		for weightsAndbiases, layer in zip(weightsAndbiasesArray, self.layers):
			layer.setWeights(weightsAndbiases[0])
			layer.setBiases(weightsAndbiases[1])

	def saveBrainToFile(self, file):
		with open(file, 'wb') as handle:
			pickle.dump(self.getBrain(), handle)

	def forward(self, inputs):
		if (finishedSetup == False):
			print("You didn't call finishSetup()")
			return
		currInput = inputs
		for index, layer in enumerate(self.layers):
			layer.forward(currInput)
			self.activationFuncs[index].forward(layer.output)
			currInput = self.activationFuncs[index].output
		return self.layers[-1].output
import numpy as np
import random
import pickle

from . LayerDense import *
from . ActivationFuncs import *

class NeuralNetwork:
	def __init__(self):
		self.layers = []
		self.activationFuncs = []
		self.totalParams = 0

	def addLayer(self, amtInputs:int, amtNeurons: int, activationFunc: ActivationFunc):
		newLayer = LayerDense(amtInputs, amtNeurons)
		newLayer.randomize()
		self.layers.append(newLayer)
		self.activationFuncs.append(activationFunc)
		self.totalParams += newLayer.amtParams

	def randomize(self):
		for layer in self.layers:
			layer.randomize()

	#Modifies this object to take certain values of the otherNN
	def crossover(self, otherNN):
		otherBrain = otherNN.getBrain()
		for layerIndex, layerData in enumerate(otherBrain):
			for weightsIndex, weights in enumerate(layerData[0]):
				for weightIndex, weight in enumerate(weights):
					#50% chance
					if (np.random.random() > 0.5):
						self.layers[layerIndex].weights[weightsIndex][weightIndex] = weight
			for biasesIndex, biases in enumerate(layerData[1]):
				for biasIndex, bias in enumerate(biases):
					if (np.random.random() > 0.5):
						self.layers[layerIndex].biases[biasesIndex][biasIndex] = bias


	def mutate(self):
		rand = random.randint(0, self.totalParams - 1)
		currCounter = 0
		mutated = False
		currLayerIndex = 0
		while mutated == False:
			layer = self.layers[currLayerIndex]
			if currCounter + layer.amtParams < rand:
				currLayerIndex += 1
				currCounter += layer.amtParams
				continue
			weightsList = layer.getWeights()
			currWeightsIndex = 0
			while mutated == False and currWeightsIndex < len(weightsList):
				weights = weightsList[currWeightsIndex]
				if currCounter + layer.amtNeurons <= rand:
					currWeightsIndex += 1
					currCounter += layer.amtNeurons 
					continue
				else:
					"""
					print(f"should mutate in weights here {currLayerIndex} {currWeightsIndex}")
					print(f"index that we should mutate: {rand - currCounter}")
					print(f"val: {weights[rand - currCounter]}")
					"""
					weights[rand - currCounter] += np.random.uniform(low=-0.1, high=0.1)
					mutated = True
					break
			biasesList = layer.getBiases()
			currBiasesIndex = 0
			while (mutated == False and currBiasesIndex < len(biasesList)):
				biases = biasesList[currBiasesIndex]
				if (currCounter + layer.amtNeurons <= rand):
					currBiasesIndex += 1
					currCounter += layer.amtNeurons
					continue
				else:
					"""
					print(f"should mutate in biases here {currLayerIndex} {currBiasesIndex}")
					print(f"index that we should mutate: {rand - currCounter}")
					print(f"val: {biases[rand - currCounter]}")
					"""
					biases[rand - currCounter] += np.random.uniform(low=-0.1, high=0.1)
					mutated = True
					break


	def printNetwork(self):
		print(f"Amt params: {self.totalParams}")
		for index, layer in enumerate(self.layers):
			print(f"LAYER {index}")
			print("weights")
			print(layer.getWeights())
			print("biases")
			print(layer.getBiases())
			print("\n")
		print("\n")


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

	def loadBrainFromFile(self, file):
		brain = None
		with open(file, 'rb') as handle:
			brain = pickle.load(handle)
		self.loadBrain(brain)

	def forward(self, inputs):
		currInput = inputs
		for index, layer in enumerate(self.layers):
			layer.forward(currInput)
			self.activationFuncs[index].forward(layer.output)
			currInput = self.activationFuncs[index].output
		return self.layers[-1].output
import numpy as np
import random

class LayerDense:
	#amtInputs = the number of features, amt of parameters
	def __init__(self, amtInputs, amtNeurons):
		self.amtInputs = amtInputs
		self.amtNeurons = amtNeurons
		self.amtParams = amtInputs * amtNeurons + amtNeurons
		self.weights = []
		self.biases = []

	def forward(self, inputs):
		self.output = np.dot(inputs, self.weights) + self.biases

	def getWeights(self):
		return self.weights

	def getBiases(self):
		return self.biases

	def setWeights(self, newWeights):
		self.weights = newWeights

	def setBiases(self, newBiases):
		self.biases = newBiases

	def randomize(self):
		self.weights = 0.3 * np.random.randn(self.amtInputs, self.amtNeurons)
		self.biases = np.array([np.array([np.random.random() for _ in range(self.amtNeurons)])])#np.zeros((1, amtNeurons))
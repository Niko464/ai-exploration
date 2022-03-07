import numpy as np

class LayerDense:
	#amtInputs = the number of features, amt of parameters
	def __init__(self, amtInputs, amtNeurons):
		self.weights = 0.3 * np.random.randn(amtInputs, amtNeurons)
		self.biases = np.array([np.array([1 for _ in range(amtNeurons)])])#np.zeros((1, amtNeurons))
		print("Init LayerDense")
		print(f"\tweights: {self.weights}\n\tbiases: {self.biases}")

	def forward(self, inputs):
		self.output = np.dot(inputs, self.weights) * self.biases

	def getWeights(self):
		return self.weights

	def getBiases(self):
		return self.biases

	def setWeights(self, newWeights):
		self.weights = newWeights

	def setBiases(self, newBiases):
		self.biases = newBiases
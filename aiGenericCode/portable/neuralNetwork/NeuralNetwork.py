import numpy
from portable.neuralNetwork.LayerDense import *
from portable.neuralNetwork.ActivationFuncs import *

class NeuralNetwork:
	def __init__(self):
		self.layers = []
		self.activationFuncs = []

	def addLayer(self, amtInputs:int, amtNeurons: int, activationFunc: ActivationFunc):
		newLayer = LayerDense(amtInputs, amtNeurons)
		newLayer.randomize()
		self.layers.append(newLayer)
		self.activationFuncs.append(activationFunc)

	# returns all wieghts and biases
	def getBrain(self):
		pass

	def loadBrain(self, weights, biases):
		pass

	def saveBrainToFile(self, file):
		pass

	def forward(self, inputs):
		currInput = inputs
		for index, layer in enumerate(self.layers):
			layer.forward(currInput)
			self.activationFuncs[index].forward(layer.output)
			currInput = self.activationFuncs[index].output
		return self.layers[-1].output

import numpy as np
from abc import ABC, abstractmethod

class ActivationFunc(ABC):
	def __init__(self):
		pass

	@abstractmethod
	def forward(self, inputs):
		pass

class ActivationRelu(ActivationFunc):
	def __init__(self):
		super().__init__()

	def forward(self, inputs):
		self.output = np.maximum(0, inputs)

class ActivationSoftMax(ActivationFunc):
	def __init__(self):
		super().__init__()

	def forward(self, inputs):
		#this is to prevent an overflow from happenning
		exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
		probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)
		self.output = probabilities

class ActivationSigmoid(ActivationFunc):
	def __init__(self):
		super().__init__()

	def forward(self, inputs):
		# length = len(inputs)
		# self.output = np.empty(length)
		# for i in range(length):
		# 	print("f")
		# 	print(f"shit { 1 / (1 + np.exp(-inputs[i]))}")
		# 	print("g")
		# 	self.output[i] = 1 / (1 + np.exp(-inputs[i]))
		self.output = [1 / (1 + np.exp(-x)) for x in inputs]
		return self.output
import numpy as np

class ActivationFunc:
	def __init__(self):
		pass

class ActivationRelu(ActivationFunc):
	def __init__(self):
		super().__init__()

	def forward(self, inputs):
		self.output = np.maximum(0, inputs)
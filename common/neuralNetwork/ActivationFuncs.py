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
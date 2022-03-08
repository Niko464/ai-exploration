import random
import sys
from abc import ABC, abstractmethod
from copy import deepcopy
import numpy as np

class Genes(ABC):
	def __init__(self, startingData):
		self.data = startingData
		self.len = len(startingData)

	def __str__(self):
		return f"{self.data}"

	def clone(self):
		return Genes(deepcopy(self.data))

	def mutate(self, low: float, high: float):
		rand = random.randint(0, self.len - 1)
		self.data[rand] = np.random.uniform(low=low, high=high)

	def crossover(self, other):
		child = self.clone()
		for i in range(self.len):
			if (np.random.uniform(low=-0.5, high=0.5) > 0.0):
				child.data[i] = other.data[i]
		return child
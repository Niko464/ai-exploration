import random
import sys
from abc import ABC, abstractmethod
from copy import deepcopy
import numpy as np

"""
TODO: A problem with this is the following:
	I mutate a random index, but I don't know if that index is a weight or a bias,
	it could even be someting else
	so I should have "low and high" for different parts of the genes ? idk
"""
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
		print(f"MUTATING INDEX {rand}")
		self.data[rand] = np.random.uniform(low=low, high=high)

	def crossover(self, other):
		child = self.clone()
		for i in range(self.len):
			if (np.random.uniform(low=-0.5, high=0.5) > 0.0):
				child.data[i] = other.data[i]
		return child
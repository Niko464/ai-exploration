import sys
from . import Genes
import numpy as np
from abc import ABC, abstractmethod

class Member(ABC):
    def __init__(self):
        self.fitness = -sys.maxsize - 1
        self.pickingProb = 0.0
        self.genes = Genes.Genes(np.array([0.0]))

    """
    This should randomize the genes, in a way that makes sense for ex:
    if you want some values to have a different low and high value
    in a neural network weights can be -1.0 to 1.0
    """
    @abstractmethod
    def randomize(self):
        pass

    @abstractmethod
    def clone(self):
        pass

    @abstractmethod
    def crossover(self, other):
        pass

    @abstractmethod
    def mutate(self):
        pass
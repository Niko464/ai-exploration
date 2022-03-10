import sys
from copy import deepcopy
import numpy as np
from abc import ABC, abstractmethod

"""
NOTES:
Genes shouldn't be used, because the mutate function, the crossover function are problem dependant so it's a useless
object, the NeuralNetwork object mutates, clones and makes crossovers onitself
Then according to the problem, the Member object will call these functions if necessary, for the salesman problem for
example, no need for a neural network, just an array of data
"""
class Member(ABC):
    def __init__(self):
        self.fitness = -sys.maxsize - 1
        self.pickingProb = 0.0

    """
    This should randomize the member in a way that makes sense to the problem
    """
    @abstractmethod
    def randomize(self):
        pass

    """
    Performs crossover according to the problem
    """
    @abstractmethod
    def crossover(self, other):
        pass

    """
    Self Explanatory
    """
    @abstractmethod
    def mutate(self):
        pass

    """
    Clones this object, and returns a new copy
    """
    def clone(self):
        newMember = deepcopy(self)
        return newMember
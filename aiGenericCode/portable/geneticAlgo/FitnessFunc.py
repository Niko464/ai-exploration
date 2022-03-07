from portable.geneticAlgo.Member import *
from abc import ABC, abstractmethod

class FitnessFunc(ABC):

    @abstractmethod
    def fitness(self, member: Member):
        pass
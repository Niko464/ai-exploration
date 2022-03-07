import sys
from abc import ABC, abstractmethod

class Member(ABC):
    def __init__(self):
        self.fitness = -sys.maxsize - 1
        self.pickingProb = 0.0

    @abstractmethod
    def clone(self):
        pass
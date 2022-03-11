import sys
import random

from abc import ABC, abstractmethod
from . import FitnessFunc
from . import Member


class GeneticAlgo(ABC):
    def __init__(self,
        populationSize: int,
        mutationProb: float,
        shouldCrossOver: bool,
        amtRandomMembersPerGen: int,
        showEvery: int,
        statsEvery: int,
        fitnessFunc: FitnessFunc = None):
        self.population = [self._createRandomMember() for _ in range(populationSize)]
        self.fitnessObj = fitnessFunc
        self.popSize = populationSize
        self.mutationProb = mutationProb
        self.recordFitness = -sys.maxsize - 1
        #This is the amount of members that will have totally random genes
        self.amtRandomMembersPerGen = amtRandomMembersPerGen
        self.shouldCrossOver = shouldCrossOver
        self.currGen = 1
        self.showEvery = showEvery
        self.statsEvery = statsEvery

        if self.popSize <= self.amtRandomMembersPerGen:
            raise ValueError("amtRandomMembersPerGen can't be lower or the same as popSize")

    #This should be called in a loop to train the AI
    def trainOneGeneration(self):
        self._interactWithEnvironment()
        #Calc Fitness for the population
        if (self.fitnessObj != None):
            for member in self.population:
                member.fitness = self.fitnessObj.fitness(member)
        #Order them by fitness
        self.population.sort(key=lambda member: member.fitness, reverse=True)
        #Check if the best member is a new record
        if (self.population[0].fitness > self.recordFitness):
            self.recordFitness = self.population[0].fitness
            self._foundNewFitnessRecord(self.population[0])
        #Perform Crossover and mutation
        nextGeneration = [self._createRandomMember() for _ in range(self.amtRandomMembersPerGen)]
        nextGeneration.append(self.population[0])
        #TODO: the best parents can be lost with this system
        for _ in range(self.popSize - self.amtRandomMembersPerGen - 1):
            #Generate the member's picking probabilities
            self.__generatePickingProbabilities()
            parentAIndex = self.__pickAMemberIndex()
            #Next is done so that the two parent's can't be the same
            oldFitness = self.population[parentAIndex].fitness
            self.population[parentAIndex].fitness = 0.0
            self.__generatePickingProbabilities()
            self.population[parentAIndex].fitness = oldFitness
            parentBIndex = self.__pickAMemberIndex()
            child = self.population[parentAIndex].clone()
            if (self.shouldCrossOver):
                self.population[parentAIndex].crossover(self.population[parentBIndex])
            if (random.random() < self.mutationProb):
                child.mutate()
            nextGeneration.append(child)
        #Set the new population
        self.population = nextGeneration
        self.currGen += 1

    def __generatePickingProbabilities(self):
        total = 0
        for member in self.population:
            total += member.fitness
        for member in self.population:
            member.pickingProb = member.fitness / total

    #Picks a member according to the probabilities of each member to get picked
    #Returns an index in the population list
    def __pickAMemberIndex(self):
        index = 0
        prob = random.random()
        while (prob > 0.0):
            prob = prob - self.population[index].pickingProb
            index += 1
        index -= 1
        return index

    #This should be overriden by children classes in specific projects
    @abstractmethod
    def _createRandomMember(self):
        pass

    #Called when a member exceeded the current fitnessRecord
    @abstractmethod
    def _foundNewFitnessRecord(self, member):
        pass

    @abstractmethod
    def _interactWithEnvironment(self):
        pass
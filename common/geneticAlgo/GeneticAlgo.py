import sys
import random
import matplotlib.pyplot as plt

from abc import ABC, abstractmethod
from . import FitnessFunc
from . import Member


class GeneticAlgo(ABC):
    def __init__(self,
        name: str,
        populationSize: int,
        mutationProb: float,
        shouldCrossOver: bool,
        amtRandomMembersPerGen: int,
        showEvery: int,
        statsEvery: int,
        trainFromFile,
        goalFitness: float = None,
        fitnessFunc: FitnessFunc = None):
        self.name = name
        self.currGen = 1
        self.population = [self._createMember(name, trainFromFile) for _ in range(populationSize)]
        self.fitnessObj = fitnessFunc
        self.popSize = populationSize
        self.mutationProb = mutationProb
        self.recordFitness = -sys.maxsize - 1
        #This is the amount of members that will have totally random genes
        self.amtRandomMembersPerGen = amtRandomMembersPerGen
        self.shouldCrossOver = shouldCrossOver
        self.showEvery = showEvery
        self.statsEvery = statsEvery
        self.goalFitness = goalFitness
        self.rewardsListAllGens = {"gen": [], "avg": [], "max": [], "min": []}
        self.statisticsForGens = {"gen": [], "avg": [], "max": [], "min": []}

        if self.popSize <= self.amtRandomMembersPerGen:
            raise ValueError("amtRandomMembersPerGen can't be lower or the same as popSize")

    #This should be called in a loop to train the AI
    def trainOneGeneration(self):
        self._interactWithEnvironment()
        #Recording statistings accross generations
        if (self.currGen % self.statsEvery == 0):
            avg = sum(self.rewardsListAllGens["avg"][-self.statsEvery:]) / self.statsEvery
            self.statisticsForGens["gen"].append(self.currGen)
            self.statisticsForGens["max"].append(max(self.rewardsListAllGens["max"][-self.statsEvery:]))
            self.statisticsForGens["min"].append(min(self.rewardsListAllGens["min"][-self.statsEvery:]))
            self.statisticsForGens["avg"].append(avg)

            if (self.goalFitness != None and self.statisticsForGens["avg"][-1] >= self.goalFitness):
                print(f"Achieved goal fitness at generation {self.currGen}")
                return True
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
        nextGeneration = [self._createMember(self.name) for _ in range(self.amtRandomMembersPerGen)]
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
            child.gen += 1
            if (self.shouldCrossOver):
                self.population[parentAIndex].crossover(self.population[parentBIndex])
            if (random.random() < self.mutationProb):
                child.mutate()
            nextGeneration.append(child)
        #Set the new population
        self.population = nextGeneration
        self.currGen += 1
        return False

    def showStats(self):
        plt.plot(self.statisticsForGens["gen"], self.statisticsForGens["avg"], label="average rewards")
        plt.plot(self.statisticsForGens["gen"], self.statisticsForGens["min"], label="min rewards")
        plt.plot(self.statisticsForGens["gen"], self.statisticsForGens["max"], label="max rewards")
        plt.legend(loc=4)
        plt.show()

    def __generatePickingProbabilities(self):
        total = 0
        minVal = min([member.fitness for member in self.population])
        for member in self.population:
            total += (member.fitness - minVal)
        #this happens when we train the algo with a loaded file
        if (total == 0):
            for member in self.population:
                member.pickingProb = 1.0
            return
        for member in self.population:
            member.pickingProb = (member.fitness - minVal) / total

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
    def _createMember(self, existingFileSave = None):
        pass

    #Called when a member exceeded the current fitnessRecord
    @abstractmethod
    def _foundNewFitnessRecord(self, member):
        pass

    """
    Needs to be included:
    - interaction with environmnent
    - self.rewardsListAllGens.append(np.mean(rewards))

    Can be included:
    - calculation of fitness
    """
    @abstractmethod
    def _interactWithEnvironment(self):
        pass
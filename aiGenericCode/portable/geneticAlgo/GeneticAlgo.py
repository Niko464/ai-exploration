import sys
from abc import ABC, abstractmethod
from portable.geneticAlgo.FitnessFunc import *

class GeneticAlgo(ABC):
    def __init__(       self,
                        populationSize: int,
                        fitnessFunc: FitnessFunc,
                        mutationProb: float
                ):
        self.population = []
        self.createRandomPopulation()
        self.fitnessObj = fitnessFunc
        self.popSize = populationSize
        self.mutationProb = mutationProb
        self.recordFitness = -sys.maxsize - 1
    
    def __crossover(self, memberA: Member, memberB: Member):
        pass
    
    def __mutation(self, memberA: Member):
        pass

    #This should be called in a loop to train the AI
    def trainOneGeneration(self):
        #Calc Fitness for the population
        for member in self.population:
            member.fitness = self.fitnessObj.fitness(member)
        #Order them by fitness
        self.population.sort(key=lambda member: member.fitness, reverse=True)
        #Check if the best member is a new record
        if (self.population[0].fitness > self.recordFitness):
            self.recordFitness = self.population[0].fitness
            #TODO: do something with this info
            print(f"TODO | new fitnessRecord: {self.recordFitness}")
        #Generate the member's picking probabilities
        self.__generatePickingProbabilities()
        #Perform Crossover and mutation
        nextGeneration = []
        for _ in range(self.popSize):
            #TODO
            pass
        #Set the new population
        self.population = nextGeneration

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
    def createRandomPopulation():
        pass

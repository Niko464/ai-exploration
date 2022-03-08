from random import shuffle
import pickle
import math
from threading import Thread
import time
import random
from copy import *
import sys
import os

p = os.path.abspath("..")
sys.path.append(p)

from common.other.Point import *
from common.geneticAlgo.FitnessFunc import *
from common.geneticAlgo.Member import *
from common.graphical.GameEngine import *
from src.SalesDroneGraphical import *

def getDistance(a: Point, b: Point):
	return math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2)

def loadObject(file):
	toReturn = None
	with open(file, 'rb') as handle:
		toReturn = pickle.load(handle)
	return toReturn

class SaleDroneMember(Member):
	def __init__(self, listCities, cityInfos):
		super().__init__()
		self.data = listCities
		self.cityInfos = cityInfos

	def clone(self):
		pass

	def crossover(self):
		pass

	def mutate(self):
		pass

	def randomize(self):
		pass

        
class SaleDroneFitnessFunc(FitnessFunc):
	def __init__(self):
		pass
    
	def fitness(self, member: SaleDroneMember):
		score = 0.0
		for i in range(len(member.data) - 1):
			cityIndex = member.data[i]
			nextCityIndex = member.data[i + 1]
			score -= getDistance(member.cityInfos[cityIndex], member.cityInfos[nextCityIndex])
		score -= getDistance(member.cityInfos[member.data[0]], member.cityInfos[member.data[len(member.data) - 1]])
		return score

class SalesDroneAlgo:
	def __init__(self, dataToModify, cityInfos, fitnessFunc, popSize, mutationProbability):
		self.shouldStop = False
		self.dataToModify = dataToModify
		self.cityInfos = cityInfos
		self.fitnessObj = fitnessFunc
		self.popSize = popSize
		self.mutationProb = mutationProbability * 100

	def start(self):
		print("Starting to solve the problem")
		recordFitness = -sys.maxsize - 1
		#Generate random population
		population = []
		for _ in range(self.popSize):
			newMemData = [i for i in range(len(self.cityInfos))]
			random.shuffle(newMemData)
			newMem = SaleDroneMember(newMemData, self.cityInfos)
			population.append(newMem)
		while self.shouldStop == False:
			"""
			self.dataToModify[0] = random.randint(1, 3)
			time.sleep(1)
			"""
			#Calc Fitness of the population
			for member in population:
				member.fitness = self.fitnessObj.fitness(member)
			#Order them by fitness
			population.sort(key=lambda mem: mem.fitness, reverse=True)
			#Check if the best member is a new record
			if (population[0].fitness > recordFitness):
				recordFitness = population[0].fitness
				print(f"New record found: {population[0].fitness}")
				#self.dataToModify = population[0].data
				for index, newData in enumerate(population[0].data):
					self.dataToModify[index] = newData
			#Generate the member's picking probabilities
			self.generateProbabilities(population)
			newPopulation = []
			#Perform Crossover and mutation (can't do crossover in this environment)
			for _ in range(self.popSize - 2):
				#child = self.crossover(parentOne, parentTwo)
				childData = self.pickAMember(population)
				child = SaleDroneMember(childData, self.cityInfos)
				self.mutation(child)
				newPopulation.append(child)
			population = newPopulation


	def generateProbabilities(self, population):
		total = 0
		for member in population:
			total += member.fitness
		for member in population:
			member.pickingProb = member.fitness / total

	def pickAMember(self, population):
		index = 0
		prob = random.random()
		while (prob > 0.0):
			prob = prob - population[index].pickingProb
			index += 1
		index -= 1
		return copy(population[index].data)

	#TODO: problem, corssing over the two genes makes a invalid solution...
	#def crossover(self, parentA, parentB):
	#	splitPoint = random.randint(1, len(parentA.cityInfos) - 1)
	#	crossedGenes = parentA.data[:splitPoint] + parentB.data[splitPoint:]
	#	return SaleDroneMember(crossedGenes, self.cityInfos)

	def mutation(self, child):
		probability = random.randint(0, 100)
		if probability < self.mutationProb:
			dataIndexToMutate = random.randint(0, len(child.data) - 1)
			newData = random.randint(0, max(child.data))
			#print(f"Data: {child.data} dataIndexToMutate: {dataIndexToMutate} newData: {newData}")
			oldDataIndex = child.data.index(newData)
			#print(f"oldDataIndex: {oldDataIndex}")
			child.data[oldDataIndex] = child.data[dataIndexToMutate]
			child.data[dataIndexToMutate] = newData


	def stop(self):
		self.shouldStop = True

#TODO: optimization, calculate all distances once, then use a lookup table
#TODO: optimization, use "simulated annealing"
def main():
	saveFile = "saves/map20"
	cityInfos = loadObject(saveFile)
	graphicalDisplayLogic = SalesDroneGraphical(cityInfos)

	graphicalEngine = GameEngine(500, 500, "Travel Sales Drone", graphicalDisplayLogic)

	data = [i for i in range(len(cityInfos))]
	shuffle(data)
	graphicalDisplayLogic.init()

	fitnessFunc = SaleDroneFitnessFunc()
	algo = SalesDroneAlgo(data, cityInfos=cityInfos, fitnessFunc=fitnessFunc, popSize=5, mutationProbability=1.0)
	thread = Thread(target=algo.start)
	thread.start()
	while True:
		if (graphicalEngine.runGameLoop(data) == False):
			break
	algo.stop()
	thread.join()

if __name__ == "__main__":
	main()
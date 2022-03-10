import os
import sys

p = os.path.abspath("..")
sys.path.append(p)

from common.geneticAlgo.GeneticAlgo import *
from src.FlappyEnvironment import *
from src.GeneticFlappy import *

from src.MemberFlappy import *


def main():
	popSize = 1
	genAlgo = GeneticFlappy()
	#env = FlappyEnvironment(popSize)


	done = False
	#TODO: change
	aiOutputs = [[0] for _ in range(popSize)]
	for generation in range(5):
		#env.reset(shouldRender=True)
		#while not done:
		#	observations, rewards, done, _ = env.step(aiOutputs)
		genAlgo.trainOneGeneration()


def test():
	mem = MemberFlappy()
	mem.mutate()
	mem.neuralNetwork.loadGenes()

if __name__ == "__main__":
	test()
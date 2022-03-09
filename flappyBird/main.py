import os
import sys

p = os.path.abspath("..")
sys.path.append(p)

from common.geneticAlgo.GeneticAlgo import *
from src.FlappyEnvironment import *
from src.GeneticFlappy import *


def main():
	popSize = 1
	genAlgo = GeneticFlappy()
	env = FlappyEnvironment(popSize)

	env.reset(shouldRender=True)
	done = False
	#TODO: change
	aiOutputs = [[0] for _ in range(popSize)]
	while not done:
		observations, rewards, done, _ = env.step(aiOutputs)


if __name__ == "__main__":
	main()
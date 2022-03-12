import os
import sys

p = os.path.abspath("..")
sys.path.append(p)

from common.geneticAlgo.GeneticAlgo import *
from src.FlappyEnvironment import *
from src.GeneticFlappy import *
 
from src.MemberFlappy import *

import numpy as np
import time


def main():

	ai = MemberFlappy("shit", 1)
	ai.neuralNetwork.loadBrainFromFile("brains/best-Gen_12-Fitness_10002")

	env = FlappyEnvironment(1)
	observations = env.reset(True)
	done = False
	rewards = []
	dataforAi = []
	while not done:
		datafromAi = [ai.predict(observations[0])]
		observations, rewards, done, _ = env.step(datafromAi)



if __name__ == "__main__":
	main()
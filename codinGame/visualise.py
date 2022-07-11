import os
import sys

p = os.path.abspath("..")
sys.path.append(p)

from src.MPREnvironment import *
from src.MPRMember import *


def main():

	ai = MPRMember("shit", 1)
	ai.neuralNetwork.loadBrainFromFile("brains/firstTest-Gen_4-Fitness_-11667.brain")

	env = MPREnvironment(1)
	observations = env.reset(True)
	done = False
	rewards = []
	dataforAi = []
	while not done:
		datafromAi = [ai.predict(observations[0])]
		observations, rewards, done, _ = env.step(datafromAi)



if __name__ == "__main__":
	main()
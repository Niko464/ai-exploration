import os
import sys

p = os.path.abspath("..")
sys.path.append(p)

from src.MPRGenetic import *


"""

INPUTS:
VecPosNextCp X
VecPosNextCp Y

Velocity X
Velocity Y
DistanceNextCp
WorldAngle

Later:
VecNextCpNextNextCp X
VecNextCpNextNextCp Y

Outputs:
ANGLE (Calculate a vector from this angle and multiply it by 100, that will be the targetPos x and y)
THRUST


First Step is to make an AI learn to follow the checkpoints to discover AI
Second Step is to make enemies, and teams, make them learn to fight enemies, help allies


Picking probs debug
Try threading
"""
def main():
	popSize = 25
	genAlgo = MPRGenetic(	name="eigth",
							popSize=popSize,
							showEvery=20,
							statsEvery=5,
							trainFromFile="brains/eigth-Gen_443-Fitness_10975.brain",
							amtRandomMembersPerGen=5)
	amtGens = 500
	counter = 0
	done = False
	while counter < amtGens and not done:
		done = genAlgo.trainOneGeneration()
		counter += 1
	genAlgo.showStats()


if __name__ == "__main__":
	main()
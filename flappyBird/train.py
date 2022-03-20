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
 

"""
- add Curr gen on display ? (this isn't easy so I'm not doing it for now)
- create a Env object seperated from flappyenv
- Make calculations faster with threads ?
"""
def main():
	popSize = 100
	genAlgo = GeneticFlappy(name="apollo", popSize=popSize, showEvery=5, statsEvery=5)
	amtGens = 100
	counter = 0
	done = False
	while counter < amtGens and not done:
		done = genAlgo.trainOneGeneration()
		counter += 1
	genAlgo.showStats()

if __name__ == "__main__":
	main()
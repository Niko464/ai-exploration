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
- add Curr gen on display
- add score on display
- create a Env object seperated from flappyenv
- Make calculations faster with threads ?
- put statistic stuff in GeneticAlgo and not GeneticFlappy
"""
def main():
	popSize = 100
	genAlgo = GeneticFlappy(name="aaa", popSize=popSize, showEvery=1, statsEvery=5)

	for generation in range(3):
		genAlgo.trainOneGeneration()
	genAlgo.showStats()

if __name__ == "__main__":
	main()
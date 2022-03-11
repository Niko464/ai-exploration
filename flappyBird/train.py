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
- Add statistics graph
- Add x1.5 x2 x3 x4 buttons on display
- create a Env object seperated from flappyenv
- fix bugs with the AI not learning fast
- Make calculations faster with threads ?
- put statistic stuff in GeneticAlgo and not GeneticFlappy
"""
def main():
	popSize = 100
	genAlgo = GeneticFlappy(popSize=popSize, showEvery=30, statsEvery=5)

	for generation in range(30):
		genAlgo.trainOneGeneration()
	genAlgo.showStats()

if __name__ == "__main__":
	main()
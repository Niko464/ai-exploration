import os
import sys

p = os.path.abspath("..")
sys.path.append(p)

from common.geneticAlgo.GeneticAlgo import *
from src.FlappyEnvironment import *
from src.GeneticFlappy import *
 
from src.MemberFlappy import *
 

def main():
	popSize = 100
	genAlgo = GeneticFlappy(popSize=popSize)

	for generation in range(100):
		genAlgo.trainOneGeneration()

"""
def test():
	mem = MemberFlappy()
	other = mem.clone()
	other.randomize()
	print("Network Mem")
	mem.neuralNetwork.printNetwork()
	print("Network other")
	other.neuralNetwork.printNetwork()

	child = mem.clone()
	child.crossover(other)
	print("Child")
	child.neuralNetwork.printNetwork()
"""

if __name__ == "__main__":
	main()
import os
import sys

p = os.path.abspath("..")
sys.path.append(p)


import numpy as np
from common.neuralNetwork.ActivationFuncs import *

def fitness(amtCps, distNextCp, amtTicks):
	return ((amtCps * 30000) - distNextCp - (amtTicks * 100))

def printTestCase(amtCps, dist, ticks):
	print(f"{amtCps} CPs   {dist} m   {ticks} ticks\t\t{fitness(amtCps, dist, ticks)}")

def main():
	"""
	printTestCase(0, 6000, 100)
	printTestCase(0, 5000, 100)
	printTestCase(0, 1000, 100)
	printTestCase(1, 9000, 200)
	printTestCase(1, 7000, 200)
	printTestCase(1, 1000, 200)
	printTestCase(1, 1000, 180)
	printTestCase(2, 15000, 180)
	printTestCase(3, 15000, 280)
	"""



if __name__ == "__main__":
	#main()
	#sigmoid_v = np.vectorize(sigmoid)
	#print(sigmoid_v([0, ]))
	sig = ActivationSigmoid()
	sig.forward([1, 0, -2222, 5658, 232, 15, 0])
	print(sig.output)
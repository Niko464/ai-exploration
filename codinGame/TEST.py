
import numpy as np

def fitness(amtCps, distNextCp, amtTicks):
	return ((amtCps * 30000) - distNextCp - (amtTicks * 100))

def printTestCase(amtCps, dist, ticks):
	print(f"{amtCps} CPs   {dist} m   {ticks} ticks\t\t{fitness(amtCps, dist, ticks)}")

def main():
	printTestCase(0, 6000, 100)
	printTestCase(0, 5000, 100)
	printTestCase(0, 1000, 100)
	printTestCase(1, 9000, 200)
	printTestCase(1, 7000, 200)
	printTestCase(1, 1000, 200)
	printTestCase(1, 1000, 180)
	printTestCase(2, 15000, 180)
	printTestCase(3, 15000, 280)

def sigmoid(x):  
    return np.exp(-np.logaddexp(0, -x))

if __name__ == "__main__":
	#main()
	#sigmoid_v = np.vectorize(sigmoid)
	#print(sigmoid_v([0, ]))
	print(np.zeros((1, 5)))
	arr = np.array([np.array([0.1 for _ in range(5)])])
	print(arr)
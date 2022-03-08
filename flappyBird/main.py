
p = os.path.abspath("..")
sys.path.append(p)

from common.geneticAlgo.GeneticAlgo import *
from src.FlappyEnvironment import *

"""
THREE parts have to work together: Environment, the Genetic Algo, the display of a game
- make all ais interact with env in a loop
- when game is finished, 

#TODO: set seed for flappy map to train on
"""
def main():
	print("hi")
	genAlgo = GeneticAlgo()
	env = FlappyEnvironment(2)

if __name__ == "__main__":
	main()
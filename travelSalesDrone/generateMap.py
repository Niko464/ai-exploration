import random
import pickle
import sys
import os

p = os.path.abspath("..")
sys.path.append(p)

from common.other.Point import *


def main():
	saveFile = "saves/map20"
	amtCities = 20
	cities = [Point(random.randint(5, 495), random.randint(5, 495)) for i in range(amtCities)]
	with open(saveFile, 'wb') as handle:
		pickle.dump(cities, handle)

if __name__ == "__main__":
	main()
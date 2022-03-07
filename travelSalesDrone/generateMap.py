import random
from Point import *
import pickle

def main():
	saveFile = "saves/map9"
	amtCities = 9
	cities = [Point(random.randint(5, 495), random.randint(5, 495)) for i in range(amtCities)]
	with open(saveFile, 'wb') as handle:
		pickle.dump(cities, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
	main()
import GameEngine
import portable.graphical.GameEngine
from specific.graphical import *
from array import array
import random
from ai.LayerDense import *
from ai.ActivationFuncs import *

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

The GeneticAlgorithm needs to have a starting Population (generation 1)
with is a collection of
Members, a Member is composed by a Neural Network with (at first) random weights and biases
These weights and biases will be adjusted through the generations
At the end of a Member's game, we calculate it's fitness
The members with the highest fitnesses will have a higher chance
to be chosen for the next generation (next population)
The next population is composed of the best ones from the previous gen
and Mutations (modified weights or biases, only one thing is modified)
and Crossovers ?

I don't need to do "back propagation" at least not the "usual" one
because I use a Genetic Algorithm

"""
"""
Three possibilites
Create & Train AI
Load & Train AI
Load & Show AI

GeneticAlgoAI has a member array
each member has a neural network with weights and biases
the geneticalgo ai has the crossover, mutation functions
"""
class GeneticAlgoAI:
	def __init__(self):
		pass

	#TODO: Maybe delete this and use pickle to directly laod the class
	def initLoad(self, saveFile):
		pass

	def initCreate(self, saveFile, amtMembers):
		self.amtMembers = amtMembers
		self.members = [Member(i) for i in range(self.amtMembers)]

	# gets fitness for all the users, selects 2 parents replaces population with offsprings by crossing over
	def naturalSelection(self):
		pass

	#Returns a new member which is a mix of these two members
	#Calls mutation function
	def crossover(self, memberA, memberB):
		pass

	#Modifies a member so that only one value on the Neural network changes
	def mutation(self, member):
		pass


	def fitness(self, member):
		pass

	#TODO: do the population modification
	#TODO: save the ais every generations
	#TODO: if it doesn't work: what's the diff between populationSize and batchSize ?
	def startLearning(self):
		gameEngine = GameEngine.GameEngine(	amtPlayers=self.amtMembers,
											saveCpFile=None,
											loadCpFile="saves/checkpoints/map1")
		for gen in range(1):
			gameEngine.reset()
			
			#compute game for all the AIs
			while True:
				inputsForAi = gameEngine.getAIInputs()
				#aiOutputs = [member.computeOutputsForTick(aiInputsForMember) for member, aiInputsForMember in zip(self.members, inputsForAi)]
				outputsOfAi = []
				for member, aiInputsForMember in zip(self.members, inputsForAi):
					#print(f"{member.ID} {gameOutputForMember}")
					outputsOfAi.append(member.computeOutputsForTick(aiInputsForMember))

				print(f"AI Outputs: {outputsOfAi}")
				if gameEngine.computeTick(outputsOfAi) == False:
					break

			computedGame = gameEngine.getGameSummary()
			graphicalDisplayLogic = MadPodRaceGraphic.MadPodRaceGraphic(computedGame)
			#This is a class that can be reused
			graphicalEngine = portable.graphical.GameEngine.GameEngine(1600, 900, "Mad Pod Racing", graphicalDisplayLogic)

			#initialise surfaces etc for the game
			graphicalDisplayLogic.init()
			while graphicalEngine.runGameLoop(): pass
			print(f"[Generation {gen}] Starting reproduction for next generation")





class Member:
	def __init__(self, ID):
		self.ID = ID
		self.amtInputFeatures = 6
		self.amtOutputFeatures = 2
		self.layer1 = LayerDense(self.amtInputFeatures, 20)
		self.layer2 = LayerDense(20, 20)
		self.layer3 = LayerDense(20, self.amtOutputFeatures)
		self.relu = ActivationRelu()

	#Returns the output of this member's neural network for a game tick
	def computeOutputsForTick(self, arrayInputs):

		print(f"Member {self.ID} Debug")
		print(f"{arrayInputs}")
		self.layer1.forward(np.array(arrayInputs))
		self.relu.forward(self.layer1.output)
		print(f"Layer 1 Output after activation: {self.relu.output}")
		self.layer2.forward(self.relu.output)
		self.relu.forward(self.layer2.output)
		print(f"Layer 2 Output after activation: {self.relu.output}")
		self.layer3.forward(self.relu.output)
		self.relu.forward(self.layer3.output)
		print(f"Layer 3 Output after activation: {self.relu.output}")

		self.output = self.relu.output

		#return the first elem because it was built to allow a population and not just one member
		return self.output[0]







"""
Right now:
- Create GameEngine
- Compute an Entire Game
- Initialise the Graphic part of the project
- Start the display of the game


Much Later:
- Start Graphic part of the project
- Leave it up to the graphic part to get user input and ask user to choose between
	- Loading AI Model
	- Creating new model
- Once the user has chosen, init AI
- Init the GameEngine

- Start a loop: Ask input from AI until the game is done
- When the game is done, Display the Game (Problem, this means that between generations, we will need to wait until the display is done...)
- Make AI Smarter with genetic algorithm
- Restart the loop



First Step is to make an AI learn to follow the checkpoints to discover AI
Second Step is to make enemies, and teams, make them learn to fight enemies, help allies
"""
def main():
	populationSize = 1
	#ai = createNewAi("first", "saves/ai/", populationSize)
	ai = GeneticAlgoAI()
	ai.initCreate("saves/ai", populationSize)
	ai.startLearning()

	"""
	game = GameEngine.GameEngine(	amtPlayers=populationSize,
									saveCpFile=None,
									loadCpFile="saves/checkpoints/map1")
	game.reset()
	print("Starting to compute Game")
	while game.computeTick(ai.computeOutputsForTick(game.getAIInputs())): pass
	print("Finished")
	computedGame = game.getGameSummary()
	#This is a project specific class
	graphicalDisplayLogic = MadPodRaceGraphic.MadPodRaceGraphic(computedGame)
	#This is a class that can be reused
	graphicalEngine = portable.graphical.GameEngine.GameEngine(1600, 900, "Mad Pod Racing", graphicalDisplayLogic)

	#initialise surfaces etc for the game
	graphicalDisplayLogic.init()
	while graphicalEngine.runGameLoop(): pass
	"""

if __name__ == "__main__":
	main()
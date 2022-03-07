import random
from Point import *
from Player import *
from MyMath import *
from typing import List
from array import array
import copy
import pickle

class CheckpointGenerator:
	def __init__(self, checkpointRadius):
		self.checkpointRadius = checkpointRadius

	def generateCheckpoints(self, amt, minX, maxX, minY, maxY):
		checkpoints = []
		for _ in range(amt):
			newCp = Point(	random.randint(minX, maxX),
							random.randint(minY, maxY))
			while self.canCheckpointSpawnThere(newCp, checkpoints) == False:
				newCp = Point(	random.randint(minX, maxX),
								random.randint(minY, maxY))
			checkpoints.append(newCp)
		return checkpoints

	def canCheckpointSpawnThere(self, point: Point, checkpointsList: List[Point]) -> bool:
		for cp in checkpointsList:
			if getDistance(cp, point) < self.checkpointRadius * 2.5:
				return False
		return True


#TODO: Boost & Shield
class GameEngine:
	def __init__(self, amtPlayers, saveCpFile = None, loadCpFile=None):
		self.amtLaps = 3
		self.amtCheckpoints = 4#random.randint(3, 8)
		self.mapX = 16000
		self.mapY = 9000
		self.checkpointRadius = 600
		self.playerRadius = 400
		offsetBetweenCpsAndMapBorder = self.checkpointRadius + 400
		generator = CheckpointGenerator(self.checkpointRadius)
		if loadCpFile == None:
			self.checkpoints = generator.generateCheckpoints(self.amtCheckpoints,
														offsetBetweenCpsAndMapBorder,
														self.mapX - offsetBetweenCpsAndMapBorder * 2,
														offsetBetweenCpsAndMapBorder,
														self.mapY - offsetBetweenCpsAndMapBorder * 2)
			if saveCpFile != None:
				with open(saveCpFile, 'wb') as handle:
					pickle.dump(self.checkpoints, handle, protocol=pickle.HIGHEST_PROTOCOL)
		else:
			with open(loadCpFile, 'rb') as handle:
				self.checkpoints = pickle.load(handle)
		self.amtPlayers = amtPlayers


	def reset(self):
		self.tickIndex = 0
		self.players = []
		for _ in range(self.amtPlayers):
			self.players.append(Player(self.checkpoints, self.playerRadius))

		self.gameSummary = {
			"static": {
				"checkpoints": self.checkpoints
			},
			"dynamic": []
		}


	"""
	Should compute the current tick:
		- update the pod's values
		- append a game state to an array of game states
	"""
	def computeTick(self, aiOutputs: array):
		print(f"computeTick GameEngine {aiOutputs}")
		playersNotDone = self.amtPlayers
		for index, p in enumerate(self.players):
			isAlive = p.computeTick(aiOutputs[index], self.tickIndex)
			if isAlive == False:
				playersNotDone -= 1
			elif p.didFinish == True:
				playersNotDone -= 1
		self.gameSummary["dynamic"].append(self._getCurrentGameState())
		if playersNotDone == 0:
			return False
		self.tickIndex += 1
		return True

	"""
	
	"""
	def getAIInputs(self):
		return [p.getAIInputs() for p in self.players]


	def _getCurrentGameState(self):
		return {
			"players": [p.getState() for p in self.players]
		}

	"""
	Returns an array of GameStates
	for MadPodRacing, a game state would be:
		- the current positions of each player,
		- their direction angle,
		- maybe their velocity
	"""
	def getGameSummary(self):
		return self.gameSummary
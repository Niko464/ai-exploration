import pygame

from common.other.Point import *


class FlappyEnvironment:
	def __init__(self, amtAgents: int):
		self.amtAgents = amtAgents
		self.shouldRender = False
		self.ticks = 0
		self.gameSummary = {
			"static": {}
			"dynamic": []
		}
		self.gameStatePlay = True

	def reset(self, shouldRender: bool):
		self.shouldRender = shouldRender
		self.ticks = 0

	# gets executed every game tick
	def step(self, aiInputs):
		print("FlappyEnvironment | step")

		if (self.__isGameDone()):
			if self.shouldRender:
				self.__renderGame()

		self.ticks += 1
		return (observation, reward, self.__isGameDone(), None)

	def __isGameDone(self):
		return False



	#This is all the graphical part of the environment


	def __renderGame(self):
		graphicalEngine = GameEngine(1200, 450, "Flappy Bird AI", self.__renderUpdate, self.__processEvents)

		self.__graphicalReset()
		#Draw the whole game
		while graphicalEngine.runGameLoop(): pass

	def __graphicalReset(self):
		self.currentGameStateIndex = 0
		self.amtGameStatesPerSec = 5
		self.gameStateIndexCounterInterval = 1000 / self.amtGameStatesPerSec
		self.lastTimeIncreasedGameStateIndex = datetime.datetime.now()

	def __renderUpdate(self):
		print(f"FlappyEnvironment | __renderUpdate")
		self._updateGameStateIndex()



	def __processEvents(self, event):
		print(f"FlappyEnvironment | __processEvents | {event}")
		if event.key == pygame.K_LEFT:
			self.gameStatePlay = False
			self.currentGameStateIndex -= 1
			if (self.currentGameStateIndex < 0):
				self.currentGameStateIndex = 0
		elif event.key == pygame.K_RIGHT:
			self.gameStatePlay = False
			if (self.currentGameStateIndex < len(self.gameSummary["dynamic"]) - 1):
				self.currentGameStateIndex += 1
		elif event.key == pygame.K_SPACE:
			self.gameStatePlay = not self.gameStatePlay




	def _updateGameStateIndex(self):
		if self.gameStatePlay == False:
			return
		currTime = datetime.datetime.now()
		elapsed = currTime - self.lastTimeIncreasedGameStateIndex
		if (elapsed.total_seconds() * 1000 > self.gameStateIndexCounterInterval):
			self.lastTimeIncreasedGameStateIndex = currTime
			self.currentGameStateIndex += 1
			if (self.currentGameStateIndex >= len(self.gameSummary["dynamic"])):
				print("arrived at the end of the replay")
				self.currentGameStateIndex = 0
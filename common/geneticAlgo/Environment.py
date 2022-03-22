import pygame
from copy import deepcopy
import datetime

from common.graphical.GameEngine import *
from common.graphical.TextButton import *
from abc import ABC, abstractmethod

class Environment(ABC):
	def __init__(self, envName: str, amtAgents: int, baseAmtGameStatesPerSec: int, screenSizeX: int, screenSizeY: int):
		self.baseAmtGameStatesPerSec = baseAmtGameStatesPerSec
		self.envName = envName
		self.amtAgents = amtAgents
		self.shouldRender = False
		self.ticks = 0
		self.screenSizeX = screenSizeX
		self.screenSizeY = screenSizeY
		self.gameStatePlay = True
		self.gameSummary = {
			"static": {},
			"dynamic": []
		}

	"""
	Returns an array of observations
	"""
	@abstractmethod
	def reset(self, shouldRender: bool):
		pass

	"""
	Gets executed every game tick
	Returns what this func returns
	"""
	def step(self, aiInputs):
		observations = []
		rewards = []

		"""
		INSERT LOGIC
		"""

		if (self.shouldRender):
			self.gameSummary["dynamic"].append(self._getTickSummary())
		done = self._isGameDone()
		if (done):
			if self.shouldRender:
				self._renderGame()

		self.ticks += 1
		return (observations, rewards, done, None)

	"""
	Returns a boolean
	"""
	@abstractmethod
	def _isGameDone(self):
		pass

	"""
	Returns a summary of the current Tick as a json Object
	"""
	@abstractmethod
	def _getTickSummary(self):
		pass


	#This is all the graphical part of the environment


	"""
	This should be called in the step func, when it's time to render a finished game
	"""
	def _renderGame(self):
		graphicalEngine = GameEngineV2(self.screenSizeX, self.screenSizeY, self.envName, self._renderUpdate, self._processEvents)

		self._graphicalReset()
		#Draw the whole game
		while graphicalEngine.runGameLoop(): pass

	"""
	This is called before starting to draw the playback of the environment
	"""
	def _graphicalReset(self):
		self.currentGameStateIndex = 0
		self._changeReplaySpeed(1)
		self.lastTimeIncreasedGameStateIndex = datetime.datetime.now()

		self.lenGameState = len(self.gameSummary["dynamic"])
		self.fontSmall = pygame.font.Font(None, 20)
		self.fontMedium = pygame.font.Font(None, 30)
		self.fontBig = pygame.font.Font(None, 80)
		self.btnx1speed = TextButton(700, 420, "x1", self.fontMedium, drawBackground=True)
		self.btnx2speed = TextButton(730, 420, "x2", self.fontMedium, drawBackground=True)
		self.btnx3speed = TextButton(760, 420, "x3", self.fontMedium, drawBackground=True)
		self.btnx4speed = TextButton(790, 420, "x4", self.fontMedium, drawBackground=True)
		self.btnx8speed = TextButton(820, 420, "x8", self.fontMedium, drawBackground=True)

	"""
	Returns bool: if we should continue playing the playback or stop
	"""
	@abstractmethod
	def _renderUpdate(self, screen):
		pass
		"""
		screen.fill((255, 255, 255))
		self._renderGameTicks(screen)
		return self._updateGameStateIndex()
		"""


	"""
	Draws the current gametick on the screen
	"""
	def _renderGameTicks(self, screen, posX, posY):
		txtToRender = "GameTick: " + str(self.currentGameStateIndex) + " / " + str(self.lenGameState)
		txtWidth, txtHeight = self.fontMedium.size(txtToRender)
		txtSurface = self.fontMedium.render(txtToRender, False, "Black")
		screen.blit(txtSurface, (posX, posY - txtHeight))


	"""
	Draws the buttons for changing the playback speed on the screen
	"""
	def _renderReplaySpeedBtns(self, screen, x = 700, y = 420):
		if self.btnx1speed.update(screen, x, y):
			self._changeReplaySpeed(1)
		elif self.btnx2speed.update(screen, x + 30, y):
			self._changeReplaySpeed(2)
		elif self.btnx3speed.update(screen, x + 60, y):
			self._changeReplaySpeed(3)
		elif self.btnx4speed.update(screen, x + 90, y):
			self._changeReplaySpeed(4)
		elif self.btnx8speed.update(screen, x + 120, y):
			self._changeReplaySpeed(8)

	"""
	This should also be called even when overriding the class
	"""
	def _processEvents(self, event):
		if (event.type == pygame.KEYDOWN):
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



	"""
	This should be called at the end of _renderUpdate
	"""
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
				return False
		return True

	def _changeReplaySpeed(self, multiplier):
		self.amtGameStatesPerSec = self.baseAmtGameStatesPerSec * multiplier
		self.gameStateIndexCounterInterval = 1000 / self.amtGameStatesPerSec
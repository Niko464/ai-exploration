import random
from array import array
import copy
import pickle
import pygame

from src.Pod import Pod
from src.CheckpointGenerator import CheckpointGenerator
from common.geneticAlgo.Environment import Environment
from common.other.Point import Point

#TODO: Boost & Shield
class MPREnvironment(Environment):
	def __init__(self, amtPlayers, saveCpFile = None, loadCpFile=None):
		super().__init__("Mad Pod Racing", amtPlayers, 6, 1600, 900)
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


	def reset(self, shouldRender: bool):
		self.gameSummary = {
			"static": {
				"checkpoints": self.checkpoints
			},
			"dynamic": []
		}
		self.ticks = 0
		self.shouldRender = shouldRender

		self.players = []
		for _ in range(self.amtPlayers):
			self.players.append(Pod(self.checkpoints, self.playerRadius))
		return [player.getObservation() for player in self.players]


	"""
	Should compute the current tick:
		- update the pod's values
		- append a game state to an array of game states
	"""
	def step(self, aiOutputs: array):
		observations = []
		rewards = []

		"""
		INSERT LOGIC
		"""
		#print(f"computeTick GameEngine {aiOutputs}")
		for index, p in enumerate(self.players):
			p.computeTick(aiOutputs[index], self.ticks)
			observations.append(p.getObservation())
			rewards.append(0)

		if (self.shouldRender):
			self.gameSummary["dynamic"].append(self._getTickSummary())
		done = self._isGameDone()
		if (done):
			if self.shouldRender:
				self._renderGame()
			#This is custom to this game
			for index, p in enumerate(self.players):
				rewards[index] = p.getFitness(self.ticks)

		self.ticks += 1
		return (observations, rewards, done, None)


	def _getTickSummary(self):
		return {
			"players": [p.getState() for p in self.players]
		}

	def _isGameDone(self):
		return not any([pod.isAlive for pod in self.players])

	def _graphicalReset(self):
		super()._graphicalReset()
		self.cpColor = (50, 50, 50)
		self.playerColorAlive = (255, 143, 22)
		self.playeColorDead = (170, 50, 70)
		self.showCoordinates = [Point(), 0]

	def _processEvents(self, event):
		super()._processEvents(event)
		if (event.type == pygame.MOUSEMOTION):
			mouse_position = pygame.mouse.get_pos()
			self.showCoordinates = [Point(mouse_position[0], mouse_position[1]), 120]

	def _renderUpdate(self, screen):
		screen.fill("gray")
		self._drawCheckpoints(screen)
		self._drawPlayers(screen)
		self._drawCoords(screen)
		self._renderGameTicks(screen, 20, 880)
		return self._updateGameStateIndex()

	def _drawCheckpoints(self, screen):
		for index, cp in enumerate(self.gameSummary["static"]["checkpoints"]):
			pygame.draw.circle(screen, self.cpColor, (cp.x / 10, cp.y / 10), 600 / 10, 3)
			txtToRender = str(index)
			txtWidthOne, txtHeightOne = self.fontBig.size(txtToRender)
			txtSurface = self.fontBig.render(txtToRender, False, "Black")
			screen.blit(txtSurface, (cp.x / 10 - txtWidthOne / 2 + 1, cp.y / 10 - txtHeightOne / 2 + 1))
			txtToRender = str(cp.x) + "," + str(cp.y)
			txtWidth, txtHeight = self.fontSmall.size(txtToRender)
			txtSurface = self.fontSmall.render(txtToRender, False, "Black")
			screen.blit(txtSurface, (cp.x / 10 - txtWidth / 2 + 1, cp.y / 10 - txtHeight / 2 + 1 + txtHeightOne))

	def _drawPlayers(self, screen):
		for p in self.gameSummary["dynamic"][self.currentGameStateIndex]["players"]:
			pX = p["pos"].x / 10
			pY = p["pos"].y / 10
			color = self.playerColorAlive if p["isAlive"] else self.playeColorDead
			pygame.draw.circle(screen, color, (pX, pY), 400 / 10, 3)
			pygame.draw.line(screen, color, (pX, pY), (pX + p["lookingVector"][0] * 400 / 10, pY + p["lookingVector"][1] * 400 / 10), 3)
			pygame.draw.line(screen, color, (pX, pY), (p["targetPos"].x / 10, p["targetPos"].y / 10), 1)

	def _drawCoords(self, screen):
		if (self.showCoordinates[1] <= 0):
			return
		self.showCoordinates[1] -= 1
		txtToRender = "x: " + str(self.showCoordinates[0].x * 10) + ", y: " + str(self.showCoordinates[0].y * 10)
		txtWidth, txtHeight = self.fontMedium.size(txtToRender)
		coordsSurface = pygame.Surface((txtWidth + 40, txtHeight + 40))
		coordsSurface.set_alpha(128)
		coordsSurface.fill("gray20")
		txtSurface = self.fontMedium.render(txtToRender, False, "White")
		screen.blit(coordsSurface, (self.showCoordinates[0].x, self.showCoordinates[0].y))
		screen.blit(txtSurface, (self.showCoordinates[0].x + 20, self.showCoordinates[0].y + 20))
import random
from array import array
import copy
import pickle
import pygame

from src.BomberMap2D import BomberMap2D
from src.Character import Character
from common.geneticAlgo.Environment import Environment
from common.other.Point import Point

class BomberEnv(Environment):
	def __init__(self, amtPlayers):
		super().__init__("Bomberman 2D", amtPlayers, 6, 1600, 900)
		self.mapX = 16000
		self.mapY = 9000
		self.amtPlayers = amtPlayers
        self.map = BomberMap2D(8, 8)


	def reset(self, shouldRender: bool):
		self.gameSummary = {
			"static": {
			},
			"dynamic": []
		}
		self.ticks = 0
		self.shouldRender = shouldRender

		self.players = []
		for _ in range(self.amtPlayers):
			self.players.append(Character())
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


	def getColorAccordingToType(self, type):
		pass

	def _drawMap(self, screen):
		for row in (self.gameSummary["dynamic"]["map"]):
			for type in row:
				color = self.getColorAccordingToType(type)
				#TODO
				#pygame.draw.rect(screen, )
				pygame.draw.circle(screen, self.cpColor, (cp.x / 10, cp.y / 10), 600 / 10, 3)
				txtToRender = str(index)
				txtWidthOne, txtHeightOne = self.fontBig.size(txtToRender)
				txtSurface = self.fontBig.render(txtToRender, False, "Black")
				screen.blit(txtSurface, (cp.x / 10 - txtWidthOne / 2 + 1, cp.y / 10 - txtHeightOne / 2 + 1))
				txtToRender = str(cp.x) + "," + str(cp.y)
				txtWidth, txtHeight = self.fontSmall.size(txtToRender)
				txtSurface = self.fontSmall.render(txtToRender, False, "Black")
				screen.blit(txtSurface, (cp.x / 10 - txtWidth / 2 + 1, cp.y / 10 - txtHeight / 2 + 1 + txtHeightOne))

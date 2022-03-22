import pygame
from copy import deepcopy
import datetime

from common.other.Point import *
from common.geneticAlgo.Environment import *
from src.Bird import *
from src.Pipe import *

class FlappyEnvironment(Environment):
	def __init__(self, amtAgents: int):
		super().__init__("Flappy Bird AI", amtAgents, 20, 900, 450)
		self.minPipeSpacing = 145
		self.maxPipeSpacing = 175
		self.pipeSpeed = 8
		self.reset(False)

	def reset(self, shouldRender: bool):
		self.gameSummary = {
			"static": {},
			"dynamic": []
		}
		self.shouldRender = shouldRender
		self.ticks = 0
		self.birds = []
		self.currentPipeSpacing = self.maxPipeSpacing
		self.pipes = []
		amtPipes = 3
		pipeSpacingX = (self.screenSizeX + 60) / amtPipes
		for i in range(3):
			self.pipes.append(Pipe(self.screenSizeX + 50, self.screenSizeX + 50 + i * pipeSpacingX , self.pipeSpeed, self.screenSizeY, self.currentPipeSpacing))
		
		startX = 150
		startY = self.screenSizeY / 2
		self.birds = [Bird(index, startX, startY, self.screenSizeX, self.screenSizeY, self.pipeSpeed) for index in range(self.amtAgents)]
		return [bird.getObservation(self.pipes) for bird in self.birds]

	# gets executed every game tick
	def step(self, aiInputs):
		observations = []
		rewards = []

		if (self.ticks % 100 == 0):
			self.currentPipeSpacing = max(self.currentPipeSpacing - 5, self.minPipeSpacing)
		for pipe in self.pipes:
			pipe.update(self.ticks, self.currentPipeSpacing)

		for index, agent in enumerate(self.birds):
			obs, reward = agent.update(self.ticks, aiInputs[index], self.pipes)
			observations.append(obs)
			rewards.append(reward)

		if (self.shouldRender):
			self.gameSummary["dynamic"].append(self._getTickSummary())
		done = self._isGameDone()
		if (done):
			if self.shouldRender:
				self._renderGame()

		self.ticks += 1
		return (observations, rewards, done, None)

	def _isGameDone(self):
		amtDead = 0
		for agent in self.birds:
			if agent.isOnGround == True:
				amtDead += 1
		if (self.ticks > 10000):
			return True
		return amtDead == self.amtAgents


	def _getTickSummary(self):
		return {
			"birds": [deepcopy(agent) for agent in self.birds],
			"pipes": [deepcopy(pipe) for pipe in self.pipes]
		}


	#This is all the graphical part of the environment


	def _renderUpdate(self, screen):
		screen.fill((255, 255, 255))
		self._renderBirds(screen)
		self._renderPipes(screen)
		self._renderScore(screen)
		self._renderGameTicks(screen, 20, 430)
		self._renderReplaySpeedBtns(screen)
		return self._updateGameStateIndex()

	def _renderScore(self, screen):
		maxScore = max([bird.score for bird in self.gameSummary["dynamic"][self.currentGameStateIndex]["birds"]])
		txtToRender = str(maxScore)
		txtWidth, txtHeight = self.fontBig.size(txtToRender)
		txtSurface = self.fontBig.render(txtToRender, False, "Black")
		screen.blit(txtSurface, (self.screenSizeX / 2 - txtWidth, 25))

	def _renderBirds(self, screen):
		for bird in self.gameSummary["dynamic"][self.currentGameStateIndex]["birds"]:
			pygame.draw.circle(screen, bird.aliveColor if bird.isAlive else bird.deadColor, (bird.pos.x, bird.pos.y), bird.radius, 3)
			txtToRender = str(bird.ID)
			txtWidth, txtHeight = self.fontSmall.size(txtToRender)
			txtSurface = self.fontSmall.render(txtToRender, False, "Black")
			screen.blit(txtSurface, (bird.pos.x - txtWidth / 2, bird.pos.y - txtHeight / 2))

	def _renderPipes(self, screen):
		for pipe in self.gameSummary["dynamic"][self.currentGameStateIndex]["pipes"]:
			pygame.draw.rect(screen, pipe.color, pygame.Rect(pipe.x, 0, pipe.width, pipe.topY))
			pygame.draw.rect(screen, pipe.color, pygame.Rect(pipe.x, pipe.bottomY, pipe.width, self.screenSizeY - pipe.bottomY))
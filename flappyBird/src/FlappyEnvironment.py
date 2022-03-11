import pygame
from copy import deepcopy
import datetime

from common.other.Point import *
from common.graphical.GameEngine import *
from src.Bird import *
from src.Pipe import *

class FlappyEnvironment:
	def __init__(self, amtAgents: int):
		self.amtAgents = amtAgents
		self.shouldRender = False
		self.ticks = 0
		self.gameStatePlay = True

		self.reset(False)

	def reset(self, shouldRender: bool):
		self.gameSummary = {
			"static": {},
			"dynamic": []
		}
		self.screenSizeY = 450
		self.screenSizeX = 900
		self.pipeSpeed = 8
		self.birds = []
		self.minPipeSpacing = 115
		self.maxPipeSpacing = 175
		self.currentPipeSpacing = self.maxPipeSpacing
		self.pipes = []
		amtPipes = 3
		pipeSpacingX = (self.screenSizeX + 60) / amtPipes
		for i in range(3):
			self.pipes.append(Pipe(self.screenSizeX + 50, self.screenSizeX + 50 + i * pipeSpacingX , self.pipeSpeed, self.screenSizeY, self.currentPipeSpacing))
		self.shouldRender = shouldRender

		self.ticks = 0
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
		done = self.__isGameDone()
		if (done):
			if self.shouldRender:
				self.__renderGame()

		self.ticks += 1
		return (observations, rewards, done, None)

	def __isGameDone(self):
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


	def __renderGame(self):
		graphicalEngine = GameEngineV2(self.screenSizeX, self.screenSizeY, "Flappy Bird AI", self.__renderUpdate, self.__processEvents)

		self.__graphicalReset()
		#Draw the whole game
		while graphicalEngine.runGameLoop(): pass

	def __graphicalReset(self):
		self.currentGameStateIndex = 0
		self.amtGameStatesPerSec = 20
		self.gameStateIndexCounterInterval = 1000 / self.amtGameStatesPerSec
		self.lastTimeIncreasedGameStateIndex = datetime.datetime.now()

		self.fontSmall = pygame.font.Font(None, 20)
		self.fontMedium = pygame.font.Font(None, 30)

		self.lenGameState = len(self.gameSummary["dynamic"])

	def __renderUpdate(self, screen):
		screen.fill((255, 255, 255))
		self._renderBirds(screen)
		self._renderPipes(screen)
		self._renderHUD(screen)
		return self._updateGameStateIndex()


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

	def _renderHUD(self, screen):
		startHud = (20, 430)
		txtToRender = "GameTick: " + str(self.currentGameStateIndex) + " / " + str(self.lenGameState)
		txtWidth, txtHeight = self.fontMedium.size(txtToRender)
		txtSurface = self.fontMedium.render(txtToRender, False, "Black")
		screen.blit(txtSurface, (startHud[0], startHud[1] - txtHeight))

	def __processEvents(self, event):
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
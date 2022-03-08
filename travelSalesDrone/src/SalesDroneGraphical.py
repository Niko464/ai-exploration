import pygame
import datetime

from common.graphical.GameLogic import *
from common.other.Point import *


class SalesDroneGraphical(GameLogic):
	def __init__(self, cityInfos):
		self.cityInfos = cityInfos

	def init(self):
		self.cityColor = (50, 50, 50)
		self.backgroundSurface = pygame.Surface((500, 500))
		self.backgroundSurface.fill("gray")

		self.fontSmall = pygame.font.Font(None, 20)
		self.fontMedium = pygame.font.Font(None, 30)
		self.fontBig = pygame.font.Font(None, 40)

	def processEvent(self, event):
		if (event.type == pygame.KEYDOWN):
			self._processKey(event)

	def _processKey(self, event):
		pass

	def update(self, screen, currSolution):
		screen.blit(self.backgroundSurface, (0, 0))
		self._drawLines(screen, currSolution)
		self._drawCities(screen, currSolution)


	def _drawLines(self, screen, currSolution):
		color = (70, 70, 0)
		for i in range(len(currSolution) - 1):
			cityIndex = currSolution[i]
			nextCityIndex = currSolution[i + 1]
			cityPos = self.cityInfos[cityIndex]
			nextCityPos = self.cityInfos[nextCityIndex]
			pygame.draw.line(screen, color, (cityPos.x, cityPos.y), (nextCityPos.x, nextCityPos.y), 3)
		pygame.draw.line(screen, color, (self.cityInfos[currSolution[0]].x, self.cityInfos[currSolution[0]].y), (self.cityInfos[currSolution[len(currSolution) - 1]].x, self.cityInfos[currSolution[len(currSolution) - 1]].y), 3)

	def _drawCities(self, screen, currSolution):
		color = (240, 112, 5)
		for i in range(len(currSolution)):
			cityIndex = currSolution[i]
			cityPos = self.cityInfos[cityIndex]
			pygame.draw.circle(screen, color, (cityPos.x, cityPos.y), 10, 3)
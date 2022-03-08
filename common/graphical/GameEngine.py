import pygame
from typing import Callable
from abc import ABC, abstractmethod
from . import GameLogic

"""
This is the Engine for the Graphical part of the project
it is responsible for getting input from the user and drawing
stuff to the screen

It can also be reused in different projects
"""
class GameEngine:
	def __init__(self, screenSizeX: int, screenSizeY: int, screenTitle: str, gameLogicObj: GameLogic):
		pygame.init()
		self.screen = pygame.display.set_mode((screenSizeX, screenSizeY))
		pygame.display.set_caption(screenTitle)
		self.clock = pygame.time.Clock()
		self.gameLogicObj = gameLogicObj

	def runGameLoop(self, data = None) -> bool:
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				pygame.quit()
				return False
			self.gameLogicObj.processEvent(event)
		self.gameLogicObj.update(self.screen, data)
		pygame.display.update()
		self.clock.tick(60)
		return True

class GameEngineV2(ABC):
	def __init__(self, screenSizeX: int, screenSizeY: int, screenTitle: str, updateCallback: Callable, eventCallback: Callable):
		pygame.init()
		self.screen = pygame.display.set_mode((screenSizeX, screenSizeY))
		pygame.display.set_caption(screenTitle)
		self.clock = pygame.time.Clock()
		self.updateCallback = updateCallback
		self.eventCallback = eventCallback

	def runGameLoop(self) -> bool:
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				pygame.quit()
				return False
			self.eventCallback(event)
		if (self.updateCallback.update(self.screen) == False):
			pygame.quit()
			return False
		pygame.display.update()
		#TODO: maybe readd this ? idk
		#self.clock.tick(60)
		return True
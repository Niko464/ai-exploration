from portable.graphical.GameLogic import *
import pygame
from Point import *
import datetime



"""
Commands:
- Space = Play/Pause
- L key = Go back a Tick
- R key = Go forward a Tick
"""
class MadPodRaceGraphic(GameLogic):
	def __init__(self, gameSummary):
		self.gameSummary = gameSummary
		self.showCoordinates = [Point(), 0]
		#These variables need to get updated if at some point I integrate a x2 or x4 speed feature
		self.amtGameStatesPerSec = 6 * 3
		self.gameStateIndexCounterInterval = 1000 / self.amtGameStatesPerSec
		self.lastTimeIncreasedGameStateIndex = datetime.datetime.now()
		self.currentGameStateIndex = 0
		self.gameStatePlay = True

	def init(self):
		self.cpColor = (50, 50, 50)
		self.playerColorAlive = (255, 143, 22)
		self.playeColorDead = (170, 50, 70)
		self.backgroundSurface = pygame.Surface((1600, 900))
		self.backgroundSurface.fill("gray")

		self.fontSmall = pygame.font.Font(None, 20)
		self.fontMedium = pygame.font.Font(None, 30)
		self.fontBig = pygame.font.Font(None, 40)

	def processEvent(self, event):
		if (event.type == pygame.MOUSEMOTION):
			mouse_position = pygame.mouse.get_pos()
			self.showCoordinates = [Point(mouse_position[0], mouse_position[1]), 120]
		elif (event.type == pygame.KEYDOWN):
			self._processKey(event)

	def _processKey(self, event):
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

	def update(self, screen):
		self._updateGameStateIndex()
		screen.blit(self.backgroundSurface, (0, 0))
		self._drawCheckpoints(screen)
		self._drawPlayers(screen)
		self._drawCoords(screen)
		self._drawHUDLeft(screen)


	def _drawCoords(self, screen):
		if (self.showCoordinates[1] > 0):
			self.showCoordinates[1] -= 1
			txtToRender = "x: " + str(self.showCoordinates[0].x * 10) + ", y: " + str(self.showCoordinates[0].y * 10)
			txtWidth, txtHeight = self.fontMedium.size(txtToRender)
			coordsSurface = pygame.Surface((txtWidth + 40, txtHeight + 40))
			coordsSurface.set_alpha(128)
			coordsSurface.fill("gray20")
			txtSurface = self.fontMedium.render(txtToRender, False, "White")
			screen.blit(coordsSurface, (self.showCoordinates[0].x, self.showCoordinates[0].y))
			screen.blit(txtSurface, (self.showCoordinates[0].x + 20, self.showCoordinates[0].y + 20))

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

	def _drawHUDLeft(self, screen):
		#Coords of the start of the Left HUD, (coords of the bottom of the HUD)
		startHud = (20, 880)
		txtToRender = "GameTick: " + str(self.currentGameStateIndex)
		txtWidth, txtHeight = self.fontMedium.size(txtToRender)
		txtSurface = self.fontMedium.render(txtToRender, False, "White")
		screen.blit(txtSurface, (startHud[0], startHud[1] - txtHeight))

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
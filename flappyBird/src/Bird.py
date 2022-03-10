import sys

from common.other.Point import *
from common.other.collisions import *

def constrain(val, minVal, maxVal):
	return min(maxVal, max(minVal, val))

class Bird:
	def __init__(self, ID, startPosX, startPosY, screenSizeX, screenSizeY, velX):
		self.ID = ID
		self.gravity = 6
		self.screenSizeX = screenSizeX
		self.screenSizeY = screenSizeY
		self.pos = Point(startPosX, startPosY)
		self.velX = velX
		self.velY = 0.0
		self.targetPos = Point(0.0, 0.0)
		self.radius = 20
		self.aliveColor = (20, 200, 20)
		self.deadColor = (200, 20, 20)
		self.isAlive = True
		self.isOnGround = False
		self.ticksAlive = 0

	def update(self, tick, actions, pipes):
		self.velY += self.gravity
		self.velY = constrain(self.velY, -1000, 25 if self.isAlive else 40)

		if (actions[0] > 0.5):
			self.__jump()

		if (self.isOnGround == False):
			self.pos.y += self.velY
			self.pos.y = constrain(self.pos.y, 0 + self.radius, self.screenSizeY - self.radius)
		if (self.isAlive == False):
			self.pos.x -= self.velX

		self.__checkCollisions(pipes)
		if (self.isAlive):
			self.ticksAlive += 1

		
		return (self.getObservation(pipes), self.ticksAlive)

	def getObservation(self, pipes):
		pipe = self.__getClosestPipe(pipes)
		# 'Normalized' values for the AI to use
		distX = (pipe.x - self.pos.x) / (self.screenSizeX)
		distTopY = (self.pos.y - pipe.topY) / (self.screenSizeY)
		distBottomY = (self.pos.y - pipe.bottomY) / (self.screenSizeY)
		velYNorm = self.velY / 25
		return [distX, distTopY, distBottomY, velYNorm]

	# gets closest pipe in front of the bird
	def __getClosestPipe(self, pipes):
		record = sys.maxsize
		bestPipe = None
		for pipe in pipes:
			dist = pipe.x - self.pos.x
			if (dist > 0 and dist < record):
				record = dist
				bestPipe = pipe
		return bestPipe

	def __jump(self):
		if (self.isAlive and self.isOnGround == False):
			self.velY = -25.0

	def __checkCollisions(self, pipes):
		if (self.pos.y + self.radius >= self.screenSizeY):
			self.isAlive = False
			self.isOnGround = True
		elif(self.pos.y <= self.radius):
			self.isAlive = False

		for pipe in pipes:
			if circleRectCollision(self.pos.x, self.pos.y, self.radius, pipe.x, 0, pipe.width, pipe.topY):
				self.isAlive = False
			elif circleRectCollision(self.pos.x, self.pos.y, self.radius, pipe.x, pipe.bottomY, pipe.width, self.screenSizeY - pipe.bottomY):
				self. isAlive = False
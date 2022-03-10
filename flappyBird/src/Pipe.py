import random

class Pipe:
	def __init__(self, respawnPos, startX, velX, screenSizeY, spacing):
		#offset = the space between top of the screen and where the pipe can start spawning, same for bottom
		self.offset = 40
		self.velX = velX
		self.width = 50
		self.screenSizeY = screenSizeY
		self.respawnPos = respawnPos
		self._reSpawn(spacing)
		self.x = startX
		self.color = (0, 200, 0)

	def update(self, tick, currentSpacing):
		self.x -= self.velX
		if (self.x < 0 - self.width - 10):
			self._reSpawn(currentSpacing)

	def _reSpawn(self, currentSpacing):
		self.x = self.respawnPos
		self.topY = random.randint(self.offset, self.screenSizeY - currentSpacing - self.offset)
		self.bottomY = self.topY + currentSpacing
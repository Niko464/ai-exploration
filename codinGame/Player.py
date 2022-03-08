import copy
from Point import *
import math
import numpy as np
from MyMath import *
import random

class Player:
	dividerVelocity = 800 - -800
	dividerDiffTwoPositions = 16000 - -16000
	dividerAngle = 360 - 0
	def __init__(self, cpList, playerRadius):
		self.cpList = cpList
		self.playerRadius = playerRadius
		self.pos = copy.deepcopy(cpList[0])
		self.worldAngle = 0.0
		self.isAlive = True
		self.lookingVector = np.array([0.0, 0.0])
		self.velocityVector = np.array([0.0, 0.0])
		self.targetPos = Point(0.0, 0.0)
		#To update on CP collision
		self.nextCheckpointId = 1
		self.amtLapsPassed = 0
		self.totalCheckpointsPassed = 0
		self.ticksSinceLastCP = 0
		self.didFinish = False
		#end
		self._updateLookingVector()

	def getAIInputs(self):
		to_return = []
		
		nextCpPos = self.cpList[self.nextCheckpointId]
		nextnextCpPos = self.cpList[(self.nextCheckpointId + 1) % len(self.cpList)]
		vecPosNextCpX = nextCpPos.x - self.pos.x
		vecPosNextCpY = nextCpPos.y - self.pos.y

		vecNextCpNextNextCpX = nextnextCpPos.x - nextCpPos.x
		vecNextCpNextNextCpY = nextnextCpPos.y - nextCpPos.y

		to_return.append(self._normalizeDifferenceTwoPositionsVector(vecPosNextCpX))
		to_return.append(self._normalizeDifferenceTwoPositionsVector(vecPosNextCpY))
		to_return.append(self._normalizeVelocity(self.velocityVector[0]))
		to_return.append(self._normalizeVelocity(self.velocityVector[1]))
		to_return.append(self._normalizeDistance(getDistance(nextCpPos, self.pos)))
		to_return.append(self._normalizeAngle0To360(self.worldAngle))

		print(f"getAIInputs | START")
		print(f"getAIInputs | nextCp | {nextCpPos}")
		print(f"getAIInputs | nextnextCp | {nextnextCpPos}")
		print(f"getAIInputs | {vecPosNextCpX} {to_return[0]}")
		print(f"getAIInputs | {vecPosNextCpY} {to_return[1]}")
		print(f"getAIInputs | {self.velocityVector[0]} {to_return[2]}")
		print(f"getAIInputs | {self.velocityVector[1]} {to_return[3]}")
		print(f"getAIInputs | {getDistance(nextCpPos, self.pos)} {to_return[4]}")
		print(f"getAIInputs | {self.worldAngle} {to_return[5]}")
		print(f"getAIInputs | END")
		#to_return.append(vecNextCpNextNextCpX)
		#to_return.append(vecNextCpNextNextCpY)
		return to_return


	def computeTick(self, aiOutput, tickIndex):
		if self.isAlive == False or self.didFinish == True:
			return False
		
		aiAngle = self._unNormalizeAngle0To360(aiOutput[0])
		thrust = min(100, self._unNormalizeThrust(aiOutput[1]))
		print(f"player Input AKA aiOutput \tthrust: {thrust} aiAngle: {aiAngle}")
		self._updateTargetPos(aiAngle)
		#Update looking Vector to make calcs for the rotation part of the game
		self._updateLookingVector()
		self._updateRotation(tickIndex)
		
		"""
		thrust = 100
		self.targetPos.x = self.cpList[self.nextCheckpointId].x
		self.targetPos.y = self.cpList[self.nextCheckpointId].y
		self._updateLookingVector()
		self._updateRotation(tickIndex)
		"""
		#Update Looking vector for the graphic game representation
		self._updateLookingVector()
		self._updateVelocityVector(thrust)
		self._updatePosition()
		self._applyFriction()
		self._truncateValues()
		self._checkCPCollisions()
		self._checkDeath()
		return self.isAlive

	def _minMaxNormalization(self, value, minVal, divider):
		return (value - minVal) / divider

	def _minMaxUnNormalization(self, value, minVal, divider):
		return (value * divider) + minVal

	def _normalizeVelocity(self, value):
		return self._minMaxNormalization(value, -800, Player.dividerVelocity)

	def _normalizeDifferenceTwoPositionsVector(self, value):
		return self._minMaxNormalization(value, -16000, Player.dividerDiffTwoPositions)

	def _normalizeAngle0To360(self, value):
		return self._minMaxNormalization(value, 0, Player.dividerAngle)

	def _normalizeDistance(self, value):
		return self._minMaxNormalization(value, 0, 18000)

	def _unNormalizeAngle0To360(self, value):
		return self._minMaxUnNormalization(value, 0, Player.dividerAngle)

	def _unNormalizeThrust(self, value):
		return self._minMaxUnNormalization(value, 0, 100)



	def _updateLookingVector(self):
		radians = math.radians(self.worldAngle)
		self.lookingVector[0] = math.cos(radians)
		self.lookingVector[1] = math.sin(radians)

	def _updateTargetPos(self, aiAngle):
		radians = math.radians(aiAngle)
		self.targetPos.x = math.cos(radians) * 200
		self.targetPos.y = math.sin(radians) * 200

	def _updateRotation(self, tickIndex):
		vectorTargetPos = np.array([self.targetPos.x - self.pos.x, self.targetPos.y - self.pos.y])
		angleToTargetPos0To360 = getAngleTwoVectors0To360(self.lookingVector, vectorTargetPos)
		angleToTargetPos0To180 = getAngleTwoVectors0To180(self.lookingVector, vectorTargetPos)
		if (angleToTargetPos0To360 <= 180):
			if angleToTargetPos0To180 < 18.0 or tickIndex == 0:
				self.worldAngle -= angleToTargetPos0To180
			else:
				self.worldAngle -= 18.0
		else:
			if angleToTargetPos0To180 < 18.0 or tickIndex == 0:
				self.worldAngle += angleToTargetPos0To180
			else:
				self.worldAngle += 18.0

	def _updateVelocityVector(self, thrust):
		toAdd = self.lookingVector * thrust
		self.velocityVector += toAdd

	def _updatePosition(self):
		self.pos.x += self.velocityVector[0]
		self.pos.y += self.velocityVector[1]

	def _applyFriction(self):
		self.velocityVector *= 0.85

	def _truncateValues(self):
		self.velocityVector[0] = math.trunc(self.velocityVector[0])
		self.velocityVector[1] = math.trunc(self.velocityVector[1])
		self.pos.x = round(self.pos.x)
		self.pos.y = round(self.pos.y)

	def _checkCPCollisions(self):
		cpPos = self.cpList[self.nextCheckpointId]
		if isPointInCircle(self.pos, cpPos, 600):
			if (self.nextCheckpointId == 0):
				self.amtLapsPassed += 1
			self.nextCheckpointId = (self.nextCheckpointId + 1) % len(self.cpList)
			self.totalCheckpointsPassed += 1
			self.ticksSinceLastCP = 0
		if (self.amtLapsPassed >= 3):
			self.didFinish = True
		self.ticksSinceLastCP += 1

	def _checkDeath(self):
		if (self.ticksSinceLastCP > 100):
			self.isAlive = False


	"""
	This is called to represent the player in a gameState
	it should contain the pos, worldangle, maybe his velocity
	and stuff like that to display to the screen later on
	"""
	def getState(self):
		return {
			"isAlive": self.isAlive,
			"pos": Point(self.pos.x, self.pos.y),
			"worldAngle": self.worldAngle,
			"lookingVector": copy.deepcopy(self.lookingVector),
			"targetPos": Point(self.targetPos.x, self.targetPos.y)
		}
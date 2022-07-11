import copy
import math
import numpy as np
import random
import os

from common.other.Point import Point
from common.math.distances import getDistance
from common.math.circles import isPointInCircle
from common.math.angles import getAngleTwoVectors0To180, getAngleTwoVectors0To360

class Pod:
	dividerVelocity = 800 - -800
	dividerDiffTwoPositions = 16000 - -16000
	dividerAngle = 360 - 0
	debug = False
	def __init__(self, ID, cpList, playerRadius):
		self.cpList = cpList
		self.playerRadius = playerRadius
		self.pos = copy.deepcopy(cpList[0])
		self.worldAngle = 0.0
		self.ticksAlive = 0
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
		self.ID = ID
		if (Pod.debug and os.path.exists("debug" + str(ID))):
			os.remove("debug/" + str(ID))
		#end
		self._updateLookingVector()

	def getObservation(self):
		#This is an optimisation, if he's dead, we don't need to recalculate everything
		if (self.isAlive == False):
			return self.observation
		self.observation = []
		
		nextCpPos = self.cpList[self.nextCheckpointId]
		nextnextCpPos = self.cpList[(self.nextCheckpointId + 1) % len(self.cpList)]
		vecPosNextCpX = nextCpPos.x - self.pos.x
		vecPosNextCpY = nextCpPos.y - self.pos.y

		vecNextCpNextNextCpX = nextnextCpPos.x - nextCpPos.x
		vecNextCpNextNextCpY = nextnextCpPos.y - nextCpPos.y

		self.observation.append(self._normalizeDifferenceTwoPositionsVector(vecPosNextCpX))
		self.observation.append(self._normalizeDifferenceTwoPositionsVector(vecPosNextCpY))
		self.observation.append(self._normalizeVelocity(self.velocityVector[0]))
		self.observation.append(self._normalizeVelocity(self.velocityVector[1]))
		self.observation.append(self._normalizeDistance(getDistance(nextCpPos, self.pos)))
		self.observation.append(self._normalizeAngle0To360(self.worldAngle))

		if Pod.debug:
			with open("debug/" + str(self.ID) + ".debug", "a") as file:
				file.write(f"getAIInputs | START\n")
				file.write(f"getAIInputs | nextCp | {nextCpPos}\n")
				file.write(f"getAIInputs | nextnextCp | {nextnextCpPos}\n")
				file.write(f"getAIInputs | vecPosNextCpX {vecPosNextCpX} {self.observation[0]}\n")
				file.write(f"getAIInputs | vecPosNextCpY {vecPosNextCpY} {self.observation[1]}\n")
				file.write(f"getAIInputs | velocityVectorX {self.velocityVector[0]} {self.observation[2]}\n")
				file.write(f"getAIInputs | velocityVectorY {self.velocityVector[1]} {self.observation[3]}\n")
				file.write(f"getAIInputs | distNextCp {getDistance(nextCpPos, self.pos)} {self.observation[4]}\n")
				file.write(f"getAIInputs | worldAngle {self.worldAngle} {self.observation[5]}\n")
		#to_return.append(vecNextCpNextNextCpX)
		#to_return.append(vecNextCpNextNextCpY)
		return self.observation


	def computeTick(self, aiOutput, tickIndex):
		if self.isAlive == False or self.didFinish == True:
			return False
		aiOutput = aiOutput[0]
		aiAngle = self._unNormalizeAnglemin18max18(aiOutput[0])
		thrust = min(100, self._unNormalizeThrust(aiOutput[1]))
		
		if aiOutput[0] < 0.25:
			aiAngle = -18.0
		elif aiOutput[0] > 0.75:
			aiAngle = 18.0
		if aiOutput[1] < 0.25:
			thrust = 0
		elif aiOutput[1] > 0.75:
			thrust = 100

		if Pod.debug:
			with open("debug/" + str(self.ID) + ".debug", "a") as file:
				file.write(f"{tickIndex} player Input not parsed: {aiOutput}\n")
				file.write(f"{tickIndex} player Input AKA aiOutput \tthrust: {thrust} aiAngle: {aiAngle}\n")
		
		self._updateTargetPos(aiAngle)
		if (tickIndex == 0):
			self.targetPos.x = self.cpList[self.nextCheckpointId].x
			self.targetPos.y = self.cpList[self.nextCheckpointId].y
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
		if (self.isAlive):
			self.ticksAlive += 1
		return self.isAlive

	def _minMaxNormalization(self, value, minVal, divider):
		return (value - minVal) / divider

	def _minMaxUnNormalization(self, value, minVal, divider):
		return (value * divider) + minVal

	def _normalizeVelocity(self, value):
		return self._minMaxNormalization(value, -800, Pod.dividerVelocity)

	def _normalizeDifferenceTwoPositionsVector(self, value):
		return self._minMaxNormalization(value, -16000, Pod.dividerDiffTwoPositions)

	def _normalizeAngle0To360(self, value):
		return self._minMaxNormalization(value, 0, Pod.dividerAngle)

	def _normalizeDistance(self, value):
		return self._minMaxNormalization(value, 0, 18000)

	def _unNormalizeAnglemin18max18(self, value):
		return self._minMaxUnNormalization(value, -18.0, 18.0)

	def _unNormalizeThrust(self, value):
		return self._minMaxUnNormalization(value, 0, 100)



	def _updateLookingVector(self):
		radians = math.radians(self.worldAngle)
		self.lookingVector[0] = math.cos(radians)
		self.lookingVector[1] = math.sin(radians)

	def _updateTargetPos(self, aiAngle):
		radians = math.radians((self.worldAngle + aiAngle) % 360)
		self.targetPos.x = self.pos.x + math.cos(radians) * 200 * 10
		self.targetPos.y = self.pos.y +  math.sin(radians) * 200 * 10

	def _updateRotation(self, tickIndex):
		vectorTargetPos = np.array([self.targetPos.x - self.pos.x, self.targetPos.y - self.pos.y])
		"""
		print(f"TargetPos: ")
		print(f"VectorTargetPos: ")
		print(f"LookingVector: ")
		"""
		angleToTargetPos0To360 = getAngleTwoVectors0To360(self.lookingVector, vectorTargetPos)
		angleToTargetPos0To180 = getAngleTwoVectors0To180(self.lookingVector, vectorTargetPos)
		if (Pod.debug):
			with open("debug/" + str(self.ID) + ".debug", "a") as file:
				file.write(f"Update rotation | TargetPos {self.targetPos.x} {self.targetPos.y}\t VectorTargetPos {vectorTargetPos} \tLookingVector {self.lookingVector} \t Angles {angleToTargetPos0To360} {angleToTargetPos0To180}\n")
		if (angleToTargetPos0To360 <= 180):
			if angleToTargetPos0To180 < 18.0 or tickIndex == 0:
				self.worldAngle = (self.worldAngle - angleToTargetPos0To180) % 360
			else:
				self.worldAngle = (self.worldAngle - 18.0) % 360
		else:
			if angleToTargetPos0To180 < 18.0 or tickIndex == 0:
				self.worldAngle = (self.worldAngle + angleToTargetPos0To180) % 360
			else:
				self.worldAngle = (self.worldAngle + 18.0) % 360

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
			if (Pod.debug):
				with open("debug/" + str(self.ID) + ".debug", "a") as file:
					file.write(f"passed Checkpoint\n")
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
			"ID": self.ID,
			"isAlive": self.isAlive,
			"pos": Point(self.pos.x, self.pos.y),
			"worldAngle": self.worldAngle,
			"lookingVector": copy.deepcopy(self.lookingVector),
			"targetPos": Point(self.targetPos.x, self.targetPos.y)
		}

	def getFitness(self):
		return ((self.totalCheckpointsPassed * 30000) - getDistance(self.cpList[self.nextCheckpointId], self.pos)) / 10
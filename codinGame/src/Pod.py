import copy
import math
import numpy as np
import random
import os

from common.other.Point import Point
from common.math.distances import getDistance
from common.math.circles import isPointInCircle
from common.math.angles import getAngleTwoVectors0To180, getAngleTwoVectors0To360

def minMaxNormalization(value, maxVal):
	return value / maxVal

def minMaxUnNormalization(value, maxVal):
	return value * maxVal

def normalizeVelocity(value):
	#TODO: this calc and the one under it is wrong
	#Values can be between -800 and 800
	return minMaxNormalization(value + 800, 1600)

def normalizeDifferenceTwoPositionsVector(value):
	#Values between -16k and +16k
	return minMaxNormalization(value + 16000, 32000)

def normalizeAngle0To360(value):
	return minMaxNormalization(value, 360)

def normalizeDistance(value):
	return minMaxNormalization(value, 18000)

def unNormalizeAnglemin18max18(value):
	return minMaxUnNormalization(value, 36.0) - 18.0

def unNormalizeThrust(value):
	return minMaxUnNormalization(value, 100)

class Pod:
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

	def getObservation(self):
		#This is an optimisation, if he's dead, we don't need to recalculate everything
		if (self.isAlive == False):
			return self.observation
		self.observation = np.zeros(6)
		
		nextCpPos = self.cpList[self.nextCheckpointId]
		nextnextCpPos = self.cpList[(self.nextCheckpointId + 1) % len(self.cpList)]
		vecPosNextCpX = nextCpPos.x - self.pos.x
		vecPosNextCpY = nextCpPos.y - self.pos.y

		vecNextCpNextNextCpX = nextnextCpPos.x - nextCpPos.x
		vecNextCpNextNextCpY = nextnextCpPos.y - nextCpPos.y

		self.observation[0] = normalizeDifferenceTwoPositionsVector(vecPosNextCpX)
		self.observation[1] = normalizeDifferenceTwoPositionsVector(vecPosNextCpY)
		self.observation[2] = normalizeVelocity(self.velocityVector[0])
		self.observation[3] = normalizeVelocity(self.velocityVector[1])
		self.observation[4] = normalizeDistance(getDistance(nextCpPos, self.pos))
		self.observation[5] = normalizeAngle0To360(self.worldAngle)

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
		return self.observation

	def computeTick(self, aiOutput, tickIndex):
		if self.isAlive == False or self.didFinish == True:
			return False
		aiOutput = aiOutput[0]
		aiAngle = unNormalizeAnglemin18max18(aiOutput[0])
		thrust = min(100, unNormalizeThrust(aiOutput[1]))
		
		# if aiOutput[0] < 0.10:
		# 	aiAngle = -18.0
		# elif aiOutput[0] > 0.90:
		# 	aiAngle = 18.0
		# if aiOutput[1] < 0.10:
		# 	thrust = 0
		# elif aiOutput[1] > 0.90:
		# 	thrust = 100

		# if Pod.debug:
		# 	with open("debug/" + str(self.ID) + ".debug", "a") as file:
		# 		file.write(str(tickIndex) + " player Input not parsed: " + str(aiOutput) + "\n")
		# 		file.write(str(tickIndex) + " player Input AKA aiOutput \tthrust: " + str(thrust) + " aiAngle: " + str(aiAngle) + "\n")
		
		# _updateTargetPos(aiAngle)
		radians = math.radians((self.worldAngle + aiAngle) % 360)
		self.targetPos.x = self.pos.x + math.cos(radians) * 200 * 10
		self.targetPos.y = self.pos.y +  math.sin(radians) * 200 * 10

		if (tickIndex == 0):
			self.targetPos.x = self.cpList[self.nextCheckpointId].x
			self.targetPos.y = self.cpList[self.nextCheckpointId].y
			# _updateLookingVector()
			radians = math.radians(self.worldAngle)
			self.lookingVector[0] = math.cos(radians)
			self.lookingVector[1] = math.sin(radians)


		# _updateRotation(tickIndex)
		vectorTargetPos = np.array([self.targetPos.x - self.pos.x, self.targetPos.y - self.pos.y])
		angleToTargetPos0To360 = getAngleTwoVectors0To360(self.lookingVector, vectorTargetPos)
		angleToTargetPos0To180 = getAngleTwoVectors0To180(self.lookingVector, vectorTargetPos)
		# if (Pod.debug):
		# 	with open("debug/" + str(self.ID) + ".debug", "a") as file:
		# 		file.write("Update rotation | TargetPos {self.targetPos.x} {self.targetPos.y}\t VectorTargetPos {vectorTargetPos} \tLookingVector {self.lookingVector} \t Angles {angleToTargetPos0To360} {angleToTargetPos0To180}\n")
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

		# _updateLookingVector()
		radians = math.radians(self.worldAngle)
		self.lookingVector[0] = math.cos(radians)
		self.lookingVector[1] = math.sin(radians)

		# _updateVelocityVector(thrust)
		self.velocityVector += self.lookingVector * thrust

		# _updatePosition()
		self.pos.x += self.velocityVector[0]
		self.pos.y += self.velocityVector[1]

		# _applyFriction()
		self.velocityVector *= 0.85

		# _truncateValues()
		#truncate velocity vector values
		self.velocityVector[0] = math.trunc(self.velocityVector[0])
		self.velocityVector[1] = math.trunc(self.velocityVector[1])
		self.pos.x = round(self.pos.x)
		self.pos.y = round(self.pos.y)

		#check collisions with checkpoints
		self._checkCPCollisions()

		# _checkDeath()
		if (self.ticksSinceLastCP > 100):
			self.isAlive = False

		if (self.isAlive):
			self.ticksAlive += 1
		return self.isAlive



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
from typing import List
import random

from common.other.Point import Point
from common.math.distances import getDistance

class CheckpointGenerator:
	def __init__(self, checkpointRadius):
		self.checkpointRadius = checkpointRadius

	def generateCheckpoints(self, amt, minX, maxX, minY, maxY):
		checkpoints = []
		for _ in range(amt):
			newCp = Point(	random.randint(minX, maxX),
							random.randint(minY, maxY))
			while self.canCheckpointSpawnThere(newCp, checkpoints) == False:
				newCp = Point(	random.randint(minX, maxX),
								random.randint(minY, maxY))
			checkpoints.append(newCp)
		return checkpoints

	def canCheckpointSpawnThere(self, point: Point, checkpointsList: List[Point]) -> bool:
		for cp in checkpointsList:
			if getDistance(cp, point) < self.checkpointRadius * 2.5:
				return False
		return True
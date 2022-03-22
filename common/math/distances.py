import math
from common.other.Point import Point

def getDistance(a: Point, b: Point):
	return math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
import math
from common.other.Point import Point

def isPointInCircle(point: Point, circlePoint: Point, radius: int) -> bool:
	return (math.pow(point.x - circlePoint.x, 2) + math.pow(point.y - circlePoint.y, 2)) <= radius * radius
from Point import *
import math
import numpy as np
import numpy.linalg as LA

def getDistance(a: Point, b: Point):
	return math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))


def getAngleTwoVectors0To180(a, b):
	inner = np.inner(a, b)
	norms = LA.norm(a) * LA.norm(b)

	cos = inner / norms
	rad = np.arccos(np.clip(cos, -1.0, 1.0))
	return np.rad2deg(rad)

def getAngleTwoVectors0To360(a, b):
	radian = math.atan2(a[1], a[0]) - math.atan2(b[1], b[0])
	angle = np.rad2deg(radian)
	if angle < 0:
		angle += 360
	return angle

def isPointInCircle(point: Point, circlePoint: Point, radius: int) -> bool:
	return (math.pow(point.x - circlePoint.x, 2) + math.pow(point.y - circlePoint.y, 2)) <= radius * radius

"""
bool isPointInCircle(const Vec2 &point, const Vec2 &circle, int radius) {
        return ((std::pow(point.x - circle.x, 2) + std::pow(point.y - circle.y, 2)) <= radius * radius);
    }
"""
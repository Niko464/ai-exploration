import math
import numpy as np
import numpy.linalg as LA

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
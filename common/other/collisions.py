import math

def circleRectCollision(cx: float, cy: float, radius: float, rx: float, ry: float, rw: float, rh: float):
	testX = cx
	testY = cy

	if (cx < rx):
		testX = rx
	elif (cx > rx+rw):
		testX = rx + rw
	if (cy < ry):
		testY = ry
	elif (cy > ry + rh):
		testY = ry + rh

	distX = cx - testX;
	distY = cy - testY;
	distance = math.sqrt( (distX * distX) + (distY * distY) )

	if (distance <= radius):
		return True
	return False;
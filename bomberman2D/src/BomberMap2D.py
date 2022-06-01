

class BomberMap2D():

    EMPTY = 0
    BRICK = 1
    WALL = 2
    BOMB = 3
    PLAYER = 4

    def __init__(self, sizeY, sizeX) -> None:
        self.map = []
        self.sizeX = sizeX
        self.sizeY = sizeY
        for _ in range(sizeY):
            newRow = [BomberMap2D.EMPTY for _ in range(sizeX)]
            self.map.append(newRow)
        
        #Add some Walls
        for y in range(sizeY):
            if y % 2 == 0:
                continue
            for x in range(sizeX):
                if x % 1 == 0:
                    self.map[y][x] = self.WALL

    def _areValidCoords(self, y, x):
        if x < 0 or y < 0 or x >= self.sizeX or y >= self.sizeY:
            return False
        return True

    def isEmpty(self, y, x):
        if not self._areValidCoords(y, x):
            raise Exception("Those coords are out of range")
        return self.map[y][x] == BomberMap2D.EMPTY

    def playerMove(self, oldY, oldX, newY, newX):
        if self.map[oldY][oldX] != self.PLAYER:
            raise Exception("[2DMap] Player moved but old coords didn't have a player...")
        self.map[oldY][oldX] = self.EMPTY
        self.map[newY][newX] = self.PLAYER
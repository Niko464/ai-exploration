

class Character():
    def __init__(self, id, color, pos, map) -> None:
        self.id = id
        self.color = color
        self.y, self.x = pos
        self.map = map

    def _areValidCoords(self, y, x, sizeY, sizeX):
        if x < 0 or y < 0 or x >= sizeX or y >= sizeY:
            return False
        return True

    def move(self, yOffset: int, xOffset: int):
        xOffset = max(min(xOffset, 1), -1)
        yOffset = max(min(yOffset, 1), -1)

        potentialNewX = self.x + xOffset
        potentialNewY = self.y + yOffset

        if not self._areValidCoords(potentialNewY, potentialNewX, self.map.sizeY, self.map.sizeX):
            print(f"[Player] {id} - Tried to move to invalid coords {potentialNewY} {potentialNewX}")
            return
        if self.map.isEmpty(potentialNewY, potentialNewX) == False:
            return
        try:
            self.map.playerMove(self.y, self.x, potentialNewY, potentialNewX)
        except:
            return
        self.y = potentialNewY
        self.x = potentialNewX
from LevelObject import LevelObject
from Point import Point

class Water(LevelObject):
    id: str = "water"
    layer: int = 0
    image: str = "images\\water.png"

    def __init__(self, pos: Point):
        super().__init__(pos)
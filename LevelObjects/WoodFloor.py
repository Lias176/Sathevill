from LevelObject import LevelObject
from Point import Point

class WoodFloor(LevelObject):
    id: str = "wood_floor"
    layer: int = 0
    image: str = "images\\woodFloor.png"

    def __init__(self, pos: Point):
        super().__init__(pos)
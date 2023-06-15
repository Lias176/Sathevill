from LevelObject import LevelObject
from Point import Point

class House(LevelObject):
    id: str = "house"
    layer: int = 1
    image: str = "images\\House.png"

    def __init__(self, pos: Point):
        super().__init__(pos)
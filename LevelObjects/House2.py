from LevelObject import LevelObject
from Point import Point

class House2(LevelObject):
    id: str = "house2"
    layer: int = 1
    image: str = "images\\House2.png"

    def __init__(self, pos: Point):
        super().__init__(pos)
from LevelObject import LevelObject
from Point import Point

class RemoveObject(LevelObject):
    layer: int = 0
    image: str = "images\\remove.png"

    def __init__(self, pos: Point):
        super().__init__(pos)
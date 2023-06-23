from LevelObject import LevelObject
from Point import Point

class Sand(LevelObject):
    id: str = "sand"
    layer: int = 0
    image: str = "images\\sand.png"

    def __init__(self, pos: Point):
        super().__init__(pos)
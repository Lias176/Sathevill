from LevelObject import LevelObject
from Point import Point

class Palm(LevelObject):
    id: str = "palm"
    layer: int = 1
    image: str = "images\\palm.png"

    def __init__(self, pos: Point):
        super().__init__(pos)
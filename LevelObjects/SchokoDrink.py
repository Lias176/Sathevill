from LevelObject import LevelObject
from Point import Point

class SchokoDring(LevelObject):
    id: str = "schokoDrink"
    layer: int = 2
    image: str = "images\\schokoDrink.png"

    def __init__(self, pos: Point):
        super().__init__(pos)
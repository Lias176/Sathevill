import random
from LevelObject import LevelObject
from Point import Point

class Grass(LevelObject):
    layer: int = 0
    image: str = "images\\grass0.png"
    id: str = "grass"

    def __init__(self, pos: Point):
        self.image = "images\\grass" + str(random.randint(0, 3)) + ".png"
        super().__init__(pos)
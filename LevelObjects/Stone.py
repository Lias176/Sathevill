import random
from LevelObject import LevelObject
from Point import Point

class Stone(LevelObject):
    layer: int = 1
    image: str = "images\\stone0.png"
    id: str = "stone"

    def __init__(self, pos: Point):
        self.image = "images\\stone" + str(random.randint(0, 3)) + ".png"
        super().__init__(pos)
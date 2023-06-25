import Textures
from LevelObject import LevelObject
from Point import Point

class SchokoDring(LevelObject):
    id = "schokoDrink"
    layer = 2
    surface = Textures.SCHOKO_DRINK.surface

    def __init__(self, pos: Point):
        super().__init__(pos)
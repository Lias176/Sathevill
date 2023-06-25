import Textures
from LevelObject import LevelObject
from Point import Point

class WoodFloor(LevelObject):
    id = "wood_floor"
    layer = 0
    surface = Textures.WOOD_FLOOR.surface

    def __init__(self, pos: Point):
        super().__init__(pos)
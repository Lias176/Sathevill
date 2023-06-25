import Textures
from LevelObject import LevelObject
from Point import Point

class Sand(LevelObject):
    id = "sand"
    layer = 0
    surface = Textures.SAND.surface

    def __init__(self, pos: Point):
        super().__init__(pos)
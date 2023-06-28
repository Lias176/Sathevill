import Textures
from Enemy import Enemy
from Point import Point

class Slime(Enemy):
    id = "slime"
    surfaceRight = Textures.SLIME_RIGHT.surface.convert_alpha()
    surfaceLeft = Textures.SLIME_LEFT.surface.convert_alpha()
    surface = surfaceRight

    def __init__(self, pos: Point):
        super().__init__(pos)
        self.speed = 0.1
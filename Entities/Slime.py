import Textures
from Enemy import Enemy
from Point import Point

class Slime(Enemy):
    id = "slime"
    surfaceRight = Textures.SLIME_RIGHT.surface.convert_alpha()
    surfaceLeft = Textures.SLIME_LEFT.surface.convert_alpha()
    surface = surfaceRight

    def __init__(self, pos: Point, onDamage: callable = None):
        super().__init__(pos, onDamage)
        self.speed = 0.1
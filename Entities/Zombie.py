import Textures
from Enemy import Enemy
from Point import Point

class Zombie(Enemy):
    id = "zombie"
    surfaceRight = Textures.ZOMBIE_RIGHT.surface.convert_alpha()
    surfaceLeft = Textures.ZOMBIE_LEFT.surface.convert_alpha()
    surface = surfaceRight

    def __init__(self, pos: Point, onDamage: callable = None):
        super().__init__(pos, onDamage)
        self.speed = 0.15
        self.attackCooldownAmount = 1500
        self.seeDistance = 800
        self.attackDistance = 100
        self.maxHealth = 5
        self.health = self.maxHealth
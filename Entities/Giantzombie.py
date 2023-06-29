import Textures
from Enemy import Enemy
from Point import Point

class GiantZombie(Enemy):
    id = "giantZombie"
    surfaceRight = Textures.GIANT_ZOMBIE_RIGHT.surface.convert_alpha()
    surfaceLeft = Textures.GIANT_ZOMBIE_LEFT.surface.convert_alpha()
    surface = surfaceRight
    isBoss = True

    def __init__(self, pos: Point, onDamage: callable = None):
        super().__init__(pos, onDamage)
        self.speed = 0.1
        self.attackCooldownAmount = 200
        self.seeDistance = 1000
        self.attackDistance = 150
        self.maxHealth = 50
        self.health = self.maxHealth   
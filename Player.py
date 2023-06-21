import pygame, math
from threading import Timer
from Entity import Entity

class Player(Entity):
    def __init__(self):
        super().__init__("images\\player\\front.png")
        self.invincible: bool = False
        self.maxHealth = 3
        self.health = self.maxHealth
        self.controlAngles: dict[int, int] = { pygame.K_w: 0, pygame.K_d: 90, pygame.K_s: 180, pygame.K_a: 270, pygame.K_UP: 0, pygame.K_RIGHT: 90, pygame.K_DOWN: 180, pygame.K_LEFT: 270 }

    def update(self, time: int):
        keys = pygame.key.get_pressed()
        finalAngle: int = -1

        if(finalAngle >= 0):
            self.x += math.sin(math.radians(finalAngle)) * self.speed * time
            self.y -= math.cos(math.radians(finalAngle)) * self.speed * time

        super().update()

    def takeDamage(self, damageAmount: int):
        super().takeDamage(damageAmount)
        self.invincible = True
        timer = Timer(2, self.removeInvincability)
        timer.start()

    def removeInvincability(self):
        self.invincible = False

    def respawn(self):
        self.x = 0
        self.y = 0
        self.isAlive = True
        self.health = self.maxHealth
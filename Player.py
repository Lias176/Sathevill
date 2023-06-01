import pygame
from threading import Timer
from Entity import Entity

class Player(Entity):
    def __init__(self):
        super().__init__("images\\player\\front.png")
        self.invincible: bool = False
        self.maxHealth = 3
        self.health = self.maxHealth

    def update(self, time: int):
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_w] or keys[pygame.K_UP]):
            self.y -= self.speed * (self.speed / 2) * time
        if(keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.x += self.speed * (self.speed / 2) * time
        if(keys[pygame.K_s] or keys[pygame.K_DOWN]):
            self.y += self.speed * (self.speed / 2) * time
        if(keys[pygame.K_a] or keys[pygame.K_LEFT]):
            self.x -= self.speed * (self.speed / 2) * time

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
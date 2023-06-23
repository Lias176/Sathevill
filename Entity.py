import pygame, math
from GameObject import GameObject
from Point import Point

class Entity(GameObject):
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface, Point(0, 0))
        self.speed: float = 0.2
        self.maxHealth: int = 1
        self.health: int = self.maxHealth
        self.isAlive: bool = True
        self.x: float = 0
        self.y: float = 0

    def update(self, time: int):
        self.pos = Point(math.floor(self.x), math.floor(self.y))

    def takeDamage(self, damageAmount: int):
        self.health -= damageAmount
        if(self.health <= 0):
            self.isAlive = False
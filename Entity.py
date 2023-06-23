import pygame, math
from GameObject import GameObject
from Point import Point

class Entity(GameObject):
    def __init__(self, image: str):
        super().__init__(pygame.image.load(image), Point(0, 0))
        self.speed: float = 0.4
        self.maxHealth: int = 1
        self.health: int = self.maxHealth
        self.isAlive: bool = True
        self.x: float = 0
        self.y: float = 0

    def update(self):
        self.pos = Point(math.floor(self.x), math.floor(self.y))

    def takeDamage(self, damageAmount: int):
        self.health -= damageAmount
        if(self.health <= 0):
            self.isAlive = False
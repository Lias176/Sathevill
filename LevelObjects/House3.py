import pygame
from LevelObject import LevelObject
from Point import Point

class House3(LevelObject):
    id: str = "house3"
    layer: int = 1
    image: str = "images\\House3.png"

    def __init__(self, pos: Point):
        super().__init__(pos)
        self.collisionRect = pygame.Rect(8, 128, 299, 235)
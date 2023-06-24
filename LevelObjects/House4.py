import pygame
from LevelObject import LevelObject
from Point import Point

class House4(LevelObject):
    id: str = "house4"
    layer: int = 1
    image: str = "images\\House4.png"
    
    def __init__(self, pos: Point):
        super().__init__(pos)
        self.collisionRect = pygame.Rect(19, 136, 342, 226)
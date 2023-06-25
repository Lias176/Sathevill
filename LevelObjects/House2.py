import pygame, Textures
from LevelObject import LevelObject
from Point import Point

class House2(LevelObject):
    id = "house2"
    layer = 1
    surface = Textures.HOUSE_2.surface

    def __init__(self, pos: Point):
        super().__init__(pos)
        self.collisionRect = pygame.Rect(27, 80, 256, 256)
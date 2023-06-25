import pygame, Textures
from LevelObject import LevelObject
from Point import Point

class House3(LevelObject):
    id = "house3"
    layer = 1
    surface = Textures.HOUSE_3.surface

    def __init__(self, pos: Point):
        super().__init__(pos)
        self.collisionRect = pygame.Rect(8, 128, 299, 235)
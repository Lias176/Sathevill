import pygame, Textures
from LevelObject import LevelObject
from Point import Point

class Palm(LevelObject):
    id = "palm"
    layer = 1
    surface = Textures.PALM.surface

    def __init__(self, pos: Point):
        super().__init__(pos)
        self.collisionRect = pygame.Rect(28, 204, 68, 32)
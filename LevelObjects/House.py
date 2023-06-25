import pygame, Textures
from LevelObject import LevelObject
from Point import Point

class House(LevelObject):
    id = "house"
    layer = 1
    surface = Textures.HOUSE.surface

    def __init__(self, pos: Point):
        super().__init__(pos)
        self.collisionRect = pygame.Rect(4, 71, 377, 247)
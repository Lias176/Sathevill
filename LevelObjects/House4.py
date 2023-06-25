import pygame, Textures
from LevelObject import LevelObject
from Point import Point

class House4(LevelObject):
    id = "house4"
    layer = 1
    surface = Textures.HOUSE_4.surface
    
    def __init__(self, pos: Point):
        super().__init__(pos)
        self.collisionRect = pygame.Rect(19, 136, 342, 226)
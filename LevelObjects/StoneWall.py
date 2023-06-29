import pygame, Textures
from LevelObject import LevelObject
from Point import Point

class StoneWall(LevelObject):
    id = "stoneWall"
    layer = 0
    surface = Textures.STONE_WALL.surface

    def __init__(self, pos: Point):
        super().__init__(pos)
        self.collisionRect = pygame.Rect(0, 0, 50, 50)
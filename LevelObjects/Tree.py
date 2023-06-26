import pygame, Textures
from LevelObject import LevelObject
from Point import Point

class Tree(LevelObject):
    id = "tree"
    layer = 1
    surface = Textures.TREE.surface

    def __init__(self, pos: Point):
        super().__init__(pos)
        self.collisionRect = pygame.Rect(55, 247, 48, 60)
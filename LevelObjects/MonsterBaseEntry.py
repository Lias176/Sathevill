import pygame, Textures
from LevelObject import LevelObject
from Point import Point

class MonsterBaseEntry(LevelObject):
    id = "monsterBaseEntry"
    layer = 1
    surface = Textures.MONSTER_BASE_ENTRY.surface

    def __init__(self, pos: Point):
        super().__init__(pos)
        self.collisionRect = pygame.Rect(0, 105, 349, 139)
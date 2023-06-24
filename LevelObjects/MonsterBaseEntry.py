import pygame
from LevelObject import LevelObject
from Point import Point

class MonsterBaseEntry(LevelObject):
    id: str = "monsterBaseEntry"
    layer: int = 1
    image: str = "images\\monsterbaseEntry.png"

    def __init__(self, pos: Point):
        super().__init__(pos)
        self.collisionRect = pygame.Rect(0, 105, 249, 139)
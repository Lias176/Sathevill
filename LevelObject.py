from __future__ import annotations
import pygame
from GameObject import GameObject
from Point import Point

class LevelObject(GameObject):
    surface: pygame.Surface = None
    layer: int = 0
    id: str = ""
    idClasses: dict[str, type[LevelObject]] = {}
    isEntity: bool = False
    isInteractable: bool = False

    def __init__(self, pos: Point):
        super().__init__(self.surface, pos)
        self.collisionRect: pygame.Rect = None

    def getAbsoluteCollisionRect(self):
        return pygame.Rect(self.pos.x + self.collisionRect.left, self.pos.y + self.collisionRect.top, self.collisionRect.width, self.collisionRect.height)

    @classmethod
    def getClassById(self, id: str) -> type[LevelObject]:
        return self.idClasses[id]
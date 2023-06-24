from __future__ import annotations
import pygame
from GameObject import GameObject
from Point import Point

class LevelObject(GameObject):
    image: str = ""
    layer: int = 0
    id: str = ""

    def __init__(self, pos: Point):
        super().__init__(pygame.image.load(self.image).convert_alpha(), pos)
        self.collisionRect: pygame.Rect = None

    def getAbsoluteCollisionRect(self):
        return pygame.Rect(self.pos.x + self.collisionRect.left, self.pos.y + self.collisionRect.top, self.collisionRect.width, self.collisionRect.height)

    @staticmethod
    def getClassById(id: str) -> type[LevelObject]:
        for subclass in LevelObject.__subclasses__():
            if(subclass.id == id):
                return subclass
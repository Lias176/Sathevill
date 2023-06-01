import pygame
from GameObject import GameObject
from Point import Point

class LevelObject(GameObject):
    def __init__(self, pos: Point):
        super().__init__(pygame.image.load(self.image), pos)

def getClassById(id: int):
    for subclass in LevelObject.__subclasses__():
        if(subclass.id == id):
            return subclass
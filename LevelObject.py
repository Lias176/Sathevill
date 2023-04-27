import pygame
from GameElement import GameElement

class LevelObject(GameElement):
    def __init__(self, pos: tuple):
        GameElement.__init__(self, pygame.image.load(self.image), pos)

def getClassById(id : int):
    for subclass in LevelObject.__subclasses__():
        if(subclass.id == id):
            return subclass
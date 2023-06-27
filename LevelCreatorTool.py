import pygame
from GameObject import GameObject
from Point import Point
from enum import Enum

class LevelCreatorTools(Enum):
    PLACE = 0
    REMOVE = 1
    CONFIG = 2

class LevelCreatorTool(GameObject):
    def __init__(self, surface: pygame.Surface, type: LevelCreatorTools):
        self.type: LevelCreatorTools = type
        super().__init__(surface, Point(0, 0))
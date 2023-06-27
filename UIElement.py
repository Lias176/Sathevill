import pygame
from GameObject import GameObject
from Point import Point

class UIElement:
    def __init__(self):
        self.objects: list[GameObject] = None
        self.pos: Point = None
        self.width: int = None
        self.height: int = None

    def render(self, screen: pygame.Surface):
        pass
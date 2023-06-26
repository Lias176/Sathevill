import pygame
from GameObject import GameObject

class UIElement:
    def __init__(self):
        self.objects: list[GameObject] = None

    def render(self, screen: pygame.Surface):
        for object in self.objects:
            object.render(screen)
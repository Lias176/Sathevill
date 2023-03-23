import pygame

class GameElement:
    def __init__(self, surface : pygame.Surface, pos : tuple):
        self.surface = surface
        self.pos = pos
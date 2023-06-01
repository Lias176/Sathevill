import pygame
from Point import Point

class GameObject:
    def __init__(self, surface: pygame.Surface, pos: Point):
        self.surface: pygame.Surface = surface
        self.pos: Point = pos

    def collidepoint(self, point: Point) -> bool:
        return pygame.Rect(self.pos.x, self.pos.y, self.surface.get_width(), self.surface.get_height()).collidepoint(point.asTuple())
import pygame
from Point import Point

class GameObject:
    def __init__(self, surface: pygame.Surface, pos: Point):
        self.surface: pygame.Surface = surface
        self.pos: Point = pos

    def render(self, screen: pygame.Surface):
        self.renderAt(screen, self.pos)

    def renderAt(self, screen: pygame.Surface, pos: Point):
        screen.blit(self.surface, pos.asTuple())

    def renderOffset(self, screen: pygame.Surface, offset: Point):
        self.renderAt(screen, self.pos.offset(offset))

    def collidepoint(self, point: Point) -> bool:
        return pygame.Rect(self.pos.x, self.pos.y, self.surface.get_width(), self.surface.get_height()).collidepoint(point.asTuple())
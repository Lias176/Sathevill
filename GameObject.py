import pygame
from Point import Point

class GameObject:
    def __init__(self, surface: pygame.Surface, pos: Point):
        self.surface: pygame.Surface = surface
        self.borderSurface: pygame.Surface = None
        self.pos: Point = pos

    def render(self, screen: pygame.Surface):
        self.renderAt(screen, self.pos)

    def renderAt(self, screen: pygame.Surface, pos: Point):
        screen.blit(self.surface, pos.toTuple())
        if(self.borderSurface != None):
            screen.blit(self.borderSurface, pos.toTuple())

    def renderOffset(self, screen: pygame.Surface, offset: Point):
        self.renderAt(screen, self.pos.offset(offset))

    def getRect(self) -> pygame.Rect:
        return pygame.Rect(self.pos.x, self.pos.y, self.surface.get_width(), self.surface.get_height())

    def collidepoint(self, point: Point) -> bool:
        return self.getRect().collidepoint(point.toTuple())
    
    def colliderect(self, rect: pygame.Rect) -> bool:
        return self.getRect().colliderect(rect)

    def resize(self, width: int = None, height: int = None):
        if(width == None and height == None):
            return
        if(width == None):
            width = self.surface.get_width() * (height / self.surface.get_height())
        elif(height == None):
            height = self.surface.get_height() * (width / self.surface.get_width())
        self.surface = pygame.transform.scale(self.surface, (width, height))

    def addBoxBorder(self, color: pygame.Color):
        self.borderSurface = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA).convert_alpha()
        for x in range(1, self.borderSurface.get_width() - 1):
            self.borderSurface.set_at((x, 0), color)
            self.borderSurface.set_at((x, self.borderSurface.get_height() - 1), color)
        for y in range(1, self.borderSurface.get_height() - 1):
            self.borderSurface.set_at((0, y), color)
            self.borderSurface.set_at((self.borderSurface.get_width() - 1, y), color)

    def removeBorder(self):
        self.borderSurface = None

    def isPixelTransparent(self, pixel: Point) -> bool:
        return pygame.Color(self.surface.get_at(pixel.toTuple())).a == 0
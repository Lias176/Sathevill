import pygame, Game
from Point import Point

class GameObject:
    def __init__(self, surface: pygame.Surface, pos: Point):
        self.surface: pygame.Surface = surface
        self.surface.convert_alpha()
        self.borderSurface: pygame.Surface = None
        self.colorOverlaySurface: pygame.Surface = None
        self.overlayColor: pygame.Color = None
        self.pos: Point = pos

    def setSurface(self, surface: pygame.Surface):
        self.surface = surface.convert_alpha()
        if(self.colorOverlaySurface != None):
            self.removeOverlayColor()
            self.addOverlayColor(self.overlayColor)

    def isNotOnScreen(self, cameraPos: tuple[int, int]) -> bool:
        return self.pos.x + self.surface.get_width() < cameraPos[0] or self.pos.x > cameraPos[0] + Game.screen.get_width() or self.pos.y + self.surface.get_height() < cameraPos[1] or self.pos.y > cameraPos[1] + Game.screen.get_height()

    def getCenterPos(self) -> Point:
        return Point(self.pos.x + self.surface.get_width() / 2, self.pos.y + self.surface.get_height() / 2)

    def render(self, screen: pygame.Surface):
        self.renderAt(screen, self.pos.toTuple())

    def renderAt(self, screen: pygame.Surface, pos: tuple[int, int]):
        screen.blit(self.surface, pos)
        if(self.borderSurface != None):
            screen.blit(self.borderSurface, pos)
        if(self.colorOverlaySurface != None):
            screen.blit(self.colorOverlaySurface, pos)

    def renderMinusOffset(self, screen: pygame.Surface, offset: tuple[int, int]):
        self.renderAt(screen, (self.pos.x - offset[0], self.pos.y - offset[1]))

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
        self.setSurface(pygame.transform.scale(self.surface, (width, height)))

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
    
    def addOverlayColor(self, color: pygame.Color):
        self.overlayColor = color
        self.colorOverlaySurface = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA).convert_alpha()
        for x in range(self.surface.get_width()):
            for y in range(self.surface.get_height()):
                if(not self.isPixelTransparent(Point(x, y))):
                    self.colorOverlaySurface.set_at((x, y), color)

    def removeOverlayColor(self):
        self.colorOverlaySurface = None
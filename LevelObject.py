from __future__ import annotations
import pygame, Textures
from GameObject import GameObject
from Point import Point
from LevelObjectProperty import LevelObjectProperty

class LevelObject(GameObject):
    surface: pygame.Surface = None
    layer: int = 0
    id: str = ""
    idClasses: dict[str, type[LevelObject]] = {}
    isEntity: bool = False
    interactTextStr: str = None
    interactRect: pygame.Rect = None

    def __init__(self, pos: Point):
        super().__init__(self.surface, pos)
        self.collisionRect: pygame.Rect = None
        self.renderInteractText: bool = False
        self.interactText: GameObject = None
        self.properties: list[LevelObjectProperty] = None

    def renderAt(self, screen: pygame.Surface, pos: tuple[int, int]):
        super().renderAt(screen, pos)
        if(self.renderInteractText):
            self.interactText.renderAt(screen, (pos[0] + self.surface.get_width() - 10, pos[1] + self.surface.get_width() / 2))

    def activateInteractText(self):
        self.renderInteractText = True
        if(self.interactText != None):
            return
        indicatorSurface: pygame.Surface = Textures.PRESS_E.surface
        textSurface: pygame.Surface = pygame.font.Font("fonts\\Roboto-Bold.ttf", 25).render(self.interactTextStr, True, pygame.Color(255, 255, 255))
        surface: pygame.Surface = pygame.Surface((indicatorSurface.get_width() + textSurface.get_width(), textSurface.get_height()), pygame.SRCALPHA).convert_alpha()
        surface.fill(pygame.Color(0, 0, 0, 100))
        surface.blit(indicatorSurface, (0, 0))
        surface.blit(textSurface, (indicatorSurface.get_width(), 0))
        self.interactText = GameObject(surface, Point(0, 0))

    def getAbsoluteCollisionRect(self) -> pygame.Rect:
        return pygame.Rect(self.pos.x + self.collisionRect.left, self.pos.y + self.collisionRect.top, self.collisionRect.width, self.collisionRect.height)

    def getAbsoluteInteractRect(self) -> pygame.Rect:
        return pygame.Rect(self.pos.x + self.interactRect.left, self.pos.y + self.interactRect.top, self.interactRect.width, self.interactRect.height)

    def interact(self):
        pass

    @classmethod
    def collidesList(self, list: list[GameObject], pos: Point) -> bool:
        rect: pygame.Rect = pygame.Rect(pos.x, pos.y, self.surface.get_width(), self.surface.get_height())
        for obj in list:
            if(obj.colliderect(rect)):
                return True
        return False

    @classmethod
    def getClassById(self, id: str) -> type[LevelObject]:
        return self.idClasses[id]
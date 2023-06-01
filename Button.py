import pygame, Game
from enum import Enum
from GameObject import GameObject
from Point import Point

class PositionOffset(Enum):
    TOP_LEFT = 0
    CENTER_SCREEN = 1

class Button:
    def __init__(self, text: str, font: pygame.font.Font, fontColor: pygame.Color, bgColor: pygame.Color, rect: pygame.Rect, offset: PositionOffset, onClick: callable):
        self.onClick: callable = onClick
        if(offset == PositionOffset.TOP_LEFT):
            self.bgObject: GameObject = GameObject(pygame.Surface(rect), Point(rect.x, rect.y))
        elif(offset == PositionOffset.CENTER_SCREEN):
            self.bgObject: GameObject = GameObject(pygame.Surface((rect.width, rect.height)), Point(Game.screen.get_width() / 2 - rect.width / 2 + rect.x, Game.screen.get_height() / 2 - rect.height / 2 - rect.y))
        self.bgObject.surface.fill(bgColor)
        self.fontObject = GameObject(font.render(text, True, fontColor), Point(0, 0))
        self.fontObject.pos = Point(self.bgObject.pos.x + (rect.width / 2 - self.fontObject.surface.get_width() / 2), self.bgObject.pos.y + (rect.height / 2 - self.fontObject.surface.get_height() / 2))
        buttons.append(self)

    def render(self, screen: pygame.Surface):
        screen.blit(self.bgObject.surface, self.bgObject.pos.asTuple())
        screen.blit(self.fontObject.surface, self.fontObject.pos.asTuple())

    def remove(self):
        buttons.remove(self)

buttons: list[Button] = []

def mouseClicked(mouseButton: int, pos: Point):
    if(mouseButton != 1):
        return
    for button in buttons:
        if(button.bgObject.collidepoint(pos)):
            button.onClick()
            return
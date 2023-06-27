import pygame, Game
from enum import Enum
from GameObject import GameObject
from Point import Point
from UIElement import UIElement

class PositionOffset(Enum):
    TOP_LEFT = 0
    CENTER_SCREEN = 1

class Button(UIElement):
    def __init__(self, text: str, rect: pygame.Rect, onClick: callable, font: pygame.font.Font = pygame.font.Font("fonts\\Roboto-Bold.ttf", 30), fontColor: pygame.Color = pygame.Color(194, 194, 194), borderColor: pygame.Color = pygame.Color(194, 194, 194), bgColor: pygame.Color = pygame.Color(15, 15, 15), borderRadius: int = 30, offset: PositionOffset =  PositionOffset.CENTER_SCREEN, hoverColor: pygame.Color = pygame.Color(50, 50, 50)):
        super().__init__()
        self.isHoverd: bool = False
        font.bold = True
        self.onClick: callable = onClick
        if(offset == PositionOffset.TOP_LEFT):
            self.bgObject: GameObject = GameObject(pygame.Surface(rect, pygame.SRCALPHA).convert_alpha(), Point(rect.x, rect.y))
        elif(offset == PositionOffset.CENTER_SCREEN):
            self.bgObject: GameObject = GameObject(pygame.Surface((rect.width, rect.height), pygame.SRCALPHA).convert_alpha(), Point(Game.screen.get_width() / 2 - rect.width / 2 + rect.x, Game.screen.get_height() / 2 - rect.height / 2 - rect.y))
        self.borderColor: pygame.Color = borderColor
        self.borderRadius: int = borderRadius
        self.bgColor: pygame.Color = bgColor
        self.hoverColor: pygame.Color = hoverColor
        self.drawBg(self.bgColor)
        self.fontObject = GameObject(font.render(text, True, fontColor), Point(0, 0))
        self.fontObject.pos = self.bgObject.pos.offset(Point(rect.width / 2 - self.fontObject.surface.get_width() / 2, rect.height / 2 - self.fontObject.surface.get_height() / 2))
        buttons.append(self)

    def drawBg(self, bgColor: pygame.Color):
        self.bgObject.surface.fill(bgColor)
        pygame.draw.line(self.bgObject.surface, self.borderColor, (0, 0), (self.bgObject.surface.get_width(), 0), 2)
        pygame.draw.line(self.bgObject.surface, self.borderColor, (0, self.bgObject.surface.get_height() - 2), (self.bgObject.surface.get_width(), self.bgObject.surface.get_height() - 2), 2)
        pygame.draw.line(self.bgObject.surface, self.borderColor, (0, 0), (0, self.bgObject.surface.get_height()), 2)
        pygame.draw.line(self.bgObject.surface, self.borderColor, (self.bgObject.surface.get_width() - 2, 0), (self.bgObject.surface.get_width() - 2, self.bgObject.surface.get_height()), 2)
    
    def render(self, screen: pygame.Surface):
        self.bgObject.render(screen)
        self.fontObject.render(screen)

    def remove(self):
        buttons.remove(self)

    def onHoverEnter(self):
        self.isHoverd = True
        self.drawBg(self.hoverColor)
    
    def onHoverLeave(self):
        self.isHoverd = False
        self.drawBg(self.bgColor)

buttons: list[Button] = []

def mouseClicked(mouseButton: int, pos: Point):
    if(mouseButton != 1):
        return
    for button in buttons:
        if(button.bgObject.collidepoint(pos)):
            button.onClick()
            return
        
def mouseMotion(pos: Point):
    for button in buttons:
        if(button.bgObject.collidepoint(pos)):
            if(not button.isHoverd):
                button.onHoverEnter()
        elif(button.isHoverd):
            button.onHoverLeave()
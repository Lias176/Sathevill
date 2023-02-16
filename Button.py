import pygame
from enum import Enum

screen = None

buttons = []

def init(initScreen : pygame.Surface):
    global screen
    screen = initScreen

class Button:
    def __init__(self, text : str, font : pygame.font, fontColor : str, bgColor : str, rect : pygame.Rect, offset : Enum, onClick : callable):
        self.text = text
        self.font = font
        self.fontColor = fontColor
        self.bgColor = bgColor
        self.onClick = onClick
        if(offset == PositionOffset.TopLeft):
            self.rect = pygame.draw.rect(screen, bgColor, rect)
        elif(offset == PositionOffset.CenterScreen):
            self.rect = pygame.draw.rect(screen, bgColor, pygame.Rect((pygame.Surface.get_width(screen) / 2) - (rect.width / 2) - rect.x, (pygame.Surface.get_height(screen) / 2) - (rect.height / 2) - rect.y, rect.width, rect.height))
        self.fontRender = font.render(text, True, fontColor)
        screen.blit(self.fontRender, (self.rect.x + ((self.rect.width / 2) - (pygame.Surface.get_width(self.fontRender) / 2)), self.rect.y + ((self.rect.height / 2) - (pygame.Surface.get_height(self.fontRender) / 2))))
        buttons.append(self)

    def remove(self):
        buttons.remove(self)

def mouseClicked():
    for button in buttons:
        if(button.rect.collidepoint(pygame.mouse.get_pos())):
            button.onClick()
            return

class PositionOffset(Enum):
    TopLeft = 0,
    CenterScreen = 1
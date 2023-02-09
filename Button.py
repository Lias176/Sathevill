import pygame, gc
from enum import Enum

buttons = []

class Button:
    def __init__(self, screen : pygame.Surface, text : str, font : pygame.font, fontColor : str, bgColor : str, rect : pygame.Rect, offset : Enum, onClick : callable):
        self.screen = screen
        self.text = text
        self.font = font
        self.fontColor = fontColor
        self.bgColor = bgColor
        self.onClick = onClick
        if(offset == PositionOffset.NONE):
            self.rect = pygame.draw.rect(screen, bgColor, rect)
        elif(offset == PositionOffset.CenterScreen):
            self.rect = pygame.draw.rect(screen, bgColor, pygame.Rect((pygame.Surface.get_width(screen) / 2) - (rect.width / 2), (pygame.Surface.get_height(screen) / 2) - (rect.height / 2), rect.width, rect.height))
        self.fontRender = font.render(text, True, fontColor)
        screen.blit(self.fontRect, (self.rect.x, self.rect.y))
        # self.fontRect = screen.blit(font.render(text, True, fontColor), (self.rect.x, self.rect.y))
        print(self.fontRender, (self.rect.x, self.rect.y))
        buttons.append(self)

def mouseClicked():
    for button in buttons:
        if(button.rect.collidepoint(pygame.mouse.get_pos())):
            button.onClick()

class PositionOffset(Enum):
    NONE = 0,
    CenterScreen = 1
import pygame, Game
from enum import Enum
from GameElement import GameElement

buttons = []

class Button:
    def __init__(self, text : str, font : pygame.font, fontColor : str, bgColor : str, rect : pygame.Rect, offset : Enum, onClick : callable):
        self.onClick = onClick
        if(offset == PositionOffset.TopLeft):
            self.bgGameElement = GameElement(pygame.Surface((rect.width, rect.height)), (rect.x, rect.y))
        elif(offset == PositionOffset.CenterScreen):
            self.bgGameElement = GameElement(pygame.Surface((rect.width, rect.height)), (Game.screen.get_width() / 2 - rect.width / 2 - rect.x, (Game.screen.get_height() / 2) - (rect.height / 2) - rect.y))
        self.bgGameElement.surface.fill(bgColor)
        fontSurface = font.render(text, True, fontColor)
        self.fontGameElement = GameElement(fontSurface, (self.bgGameElement.pos[0] + (rect.width / 2 - fontSurface.get_width() / 2), self.bgGameElement.pos[1] + (rect.height / 2 - fontSurface.get_height() / 2)))
        buttons.append(self)

    def remove(self):
        buttons.remove(self)

def mouseClicked(button : int):
    if(button != 1):
        return
    for button in buttons:
        if(pygame.Rect(button.bgGameElement.pos[0], button.bgGameElement.pos[1], button.bgGameElement.surface.get_width(), button.bgGameElement.surface.get_height()).collidepoint(pygame.mouse.get_pos())):
            button.onClick()
            return

class PositionOffset(Enum):
    TopLeft = 0,
    CenterScreen = 1
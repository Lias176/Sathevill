import pygame, Game
from UIElement import UIElement
from GameObject import GameObject
from Point import Point
from Button import PositionOffset

class TextBox(UIElement):
    def __init__(self, text: str, pos: Point, offset: PositionOffset = PositionOffset.CENTER_SCREEN, font: pygame.font.Font = pygame.font.Font("fonts\\Roboto-Bold.ttf", 30), fontColor: pygame.Color = pygame.Color(194, 194, 194)):
        super().__init__()
        self.offset: PositionOffset = offset
        self.text: str = text
        self.fontRender: GameObject = GameObject(font.render(text, True, fontColor).convert_alpha(), Point(0, 0))
        if(self.offset == PositionOffset.CENTER_SCREEN):
            self.fontRender.pos = Point(Game.screen.get_width() / 2 - self.fontRender.surface.get_width() / 2, Game.screen.get_height() / 2 - self.fontRender.surface.get_height() / 2).offset(Point(pos.x, -pos.y))
        else:
            self.fontRender.pos = pos
        self.fontRender.surface.set_alpha(fontColor.a)
        self.pos = self.fontRender.pos
        self.width = self.fontRender.surface.get_width()
        self.height = self.fontRender.surface.get_height()
        
    def render(self, screen: pygame.Surface):
        self.fontRender.render(screen)

    def setPos(self, pos: Point):
        if(self.offset == PositionOffset.CENTER_SCREEN):
            self.fontRender.pos = Point(Game.screen.get_width() / 2 - self.fontRender.surface.get_width() / 2, Game.screen.get_height() / 2 - self.fontRender.surface.get_height() / 2).offset(Point(pos.x, -pos.y))
        else:
            self.fontRender.pos = pos
        self.pos = self.fontRender.pos

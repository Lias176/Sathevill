import pygame, Game
from UIElement import UIElement
from GameObject import GameObject
from Point import Point

class TextBox(UIElement):
    def __init__(self, text: str, pos: Point, font: pygame.font.Font = pygame.font.Font("fonts\\Roboto-Bold.ttf", 30), fontColor: pygame.Color = pygame.Color(194, 194, 194)):
        super().__init__()
        self.fontRender = GameObject(font.render(text, True, fontColor), Point(0, 0))
        self.objects = [self.fontRender]
        self.fontRender.pos = Point(Game.screen.get_width() / 2 - self.fontRender.surface.get_width() / 2, Game.screen.get_height() / 2 - self.fontRender.surface.get_height() / 2).offset(Point(pos.x, -pos.y))

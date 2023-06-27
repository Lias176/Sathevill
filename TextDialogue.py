import pygame, Textures, Game, math
from GameObject import GameObject
from Point import Point

class TextDialogue:
    def __init__(self, texts: list[list[str]]) -> None:
        self.texts: list[list[str]] = texts
        self.bgObject: GameObject = GameObject(Textures.SPEECH_BUBBLE.surface, Point(0, 0))
        self.bgObject.resize(width = Game.screen.get_width() - 200)
        self.bgObject.pos = Point(Game.screen.get_width() / 2 - self.bgObject.surface.get_width() / 2, Game.screen.get_height() - self.bgObject.surface.get_height())
        self.textObjects: list[GameObject] = None
        self.i: int = 0
        self.setTextIndex(0)

    def setTextIndex(self, i: int):
        self.i = i
        self.textObjects = []
        fontHeight: int = math.floor(Game.screen.get_width() / 32)
        for i, text in enumerate(self.texts[i]):
            textObject: GameObject = GameObject(pygame.font.Font("fonts\\Roboto-Bold.ttf", fontHeight).render(text, True, pygame.Color(0, 0, 0)), Point(0, 0))
            textObject.pos = Point(self.bgObject.pos.x + math.floor(Game.screen.get_width() / 64), self.bgObject.pos.y + math.floor(Game.screen.get_width() / 64) + i * fontHeight)
            self.textObjects.append(textObject)

    def increaseIndex(self) -> int:
        if(self.i >= len(self.texts) - 1):
            return -1
        self.setTextIndex(self.i + 1)
        return self.i + 1

    def render(self, screen: pygame.Surface):
        self.bgObject.render(screen)
        for textObject in self.textObjects:
            textObject.render(screen)
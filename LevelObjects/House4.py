import pygame, Textures, Game
from LevelObject import LevelObject
from Point import Point
from LevelObjectProperty import LevelObjectProperty
from LevelObjectProperty import PropertyTypes

class House4(LevelObject):
    id = "house4"
    layer = 1
    surface = Textures.HOUSE_4.surface
    interactTextStr = "Betreten"
    interactRect = pygame.Rect(269, 281, 62, 82)
    
    def __init__(self, pos: Point):
        super().__init__(pos)
        self.levelName: str = ""
        self.properties = [LevelObjectProperty("level", PropertyTypes.STRING, self.levelName)]
        self.collisionRect = pygame.Rect(19, 136, 342, 226)

    def interact(self):
        if(self.properties[0].var == ""):
            return
        Game.currentLevel.loadFile("levels\\" + self.properties[0].var + ".json")
        rect = self.getAbsoluteInteractRect()
        Game.currentLevel.overWorldPos = Point(rect.left, rect.top)
        Game.currentLevel.player.x = 550
        Game.currentLevel.player.y = 400
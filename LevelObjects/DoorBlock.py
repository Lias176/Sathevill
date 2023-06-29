import pygame, Textures, Game
from LevelObject import LevelObject
from Point import Point

class Water(LevelObject):
    id = "doorBlock"
    layer = 1
    surface = Textures.DOOR_BLOCK.surface
    interactTextStr = "Verlassen"

    def __init__(self, pos: Point):
        super().__init__(pos)
        self.collisionRect =  pygame.Rect(0, 45, 50, 5)

    def interact(self):
        Game.currentLevel.loadFile("levels\\level.json")
        Game.currentLevel.player.x = Game.currentLevel.overWorldPos.x
        Game.currentLevel.player.y = Game.currentLevel.overWorldPos.y
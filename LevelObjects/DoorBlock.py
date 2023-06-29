import pygame, Textures, Game
from LevelObject import LevelObject
from Point import Point
from Entities.NPC import NPC

class Water(LevelObject):
    id = "doorBlock"
    layer = 1
    surface = Textures.DOOR_BLOCK.surface
    interactTextStr = "Verlassen"

    def __init__(self, pos: Point):
        super().__init__(pos)
        self.collisionRect =  pygame.Rect(0, 0, 50, 50)

    def interact(self):
        Game.currentLevel.loadFile("levels\\level.json")
        Game.currentLevel.player.x = Game.currentLevel.overWorldPos.x
        Game.currentLevel.player.y = Game.currentLevel.overWorldPos.y
        if(Game.currentLevel.currentQuest == 1):
            Game.currentLevel.isNight = True
            Game.currentLevel.setCurrentQuest(2)
            Game.currentLevel.spawnRaid()
        elif(Game.currentLevel.currentQuest >= 3):
            Game.currentLevel.isNight = False
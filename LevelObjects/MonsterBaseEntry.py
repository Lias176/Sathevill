import pygame, Textures, Game
from LevelObject import LevelObject
from Point import Point

class MonsterBaseEntry(LevelObject):
    id = "monsterBaseEntry"
    layer = 1
    surface = Textures.MONSTER_BASE_ENTRY.surface
    interactTextStr = "Betreten"
    interactRect = pygame.Rect(112, 161, 126, 77)

    def __init__(self, pos: Point):
        super().__init__(pos)
        self.collisionRect = pygame.Rect(0, 105, 349, 139)

    def interact(self):
        Game.currentLevel.loadFile("levels\\cave.json")
        Game.currentLevel.player.x = 900
        Game.currentLevel.player.y = 550
        if(Game.currentLevel.currentQuest == 5):
            Game.currentLevel.setCurrentQuest(6)
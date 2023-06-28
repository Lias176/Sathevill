import Textures, Game
from LevelObject import LevelObject
from Point import Point

class SchokoDring(LevelObject):
    id = "schokoDrink"
    layer = 2
    surface = Textures.SCHOKO_DRINK.surface
    interactTextStr = "Trinken"

    def __init__(self, pos: Point):
        super().__init__(pos)

    def interact(self):
        Game.currentLevel.removeLevelObject(self)
        Game.currentLevel.player.health = min(Game.currentLevel.player.health + 1, Game.currentLevel.player.maxHealth)
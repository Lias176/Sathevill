import Textures, Game
from Entity import Entity
from Point import Point
from TextDialogue import TextDialogue
from LevelObjectProperty import LevelObjectProperty
from LevelObjectProperty import PropertyTypes

class NPC(Entity):
    id = "npc"
    surface = Textures.NPC.surface
    interactTextStr = "Reden"
    
    def __init__(self, pos: Point):
        super().__init__(pos)
        self.texts: list[list[str]] = []
        self.properties = [LevelObjectProperty("Dialouge", PropertyTypes.STRINGLISTLIST, self.texts)]

    def interact(self):
        self.renderInteractText = False
        Game.currentLevel.showText(TextDialogue(self.texts))
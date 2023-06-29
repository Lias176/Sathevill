import Textures, Game
from Entity import Entity
from Point import Point
from TextDialogue import TextDialogue
from LevelObjectProperty import LevelObjectProperty
from LevelObjectProperty import PropertyTypes

class NPC(Entity):
    id = "npc1"
    surface = Textures.NPC_1.surface
    interactTextStr = "Reden"
    
    def __init__(self, pos: Point):
        super().__init__(pos)
        self.texts: list[list[str]] = [["Willkommen"], ["Es ist echt selten, dass jemand", "unser Dorf besucht."], ["Das liegt daran, dass hier ziemlich gefärlich", "geworden ist"]]

    def interact(self):
        self.renderInteractText = False
        Game.currentLevel.showText(TextDialogue(self.texts))
        
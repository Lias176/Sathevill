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

    def interact(self):
        self.renderInteractText = False
        if(Game.currentLevel.currentQuest == 0):
            Game.currentLevel.showText(TextDialogue([["Willkommen."], 
                                       ["Es ist echt selten, dass jemand", "unser Dorf besucht."], 
                                       ["Das liegt daran, dass es in letzter Zeit", "hier ziemlich gefärlich geworden ist."],
                                       ["Unser Dorf wird nämlich nachts immer von Monstern", "angegriffen."],
                                       ["Die Sonne ist auch schon wieder am untergehen."],
                                       ["Könntest du bitte versuchen die Monster zu besiegen?"],
                                       ["Sei vorsichtig!"]]))
            Game.currentLevel.setCurrentQuest(1)
        elif(Game.currentLevel.currentQuest == 1 or Game.currentLevel.currentQuest == 2):
            Game.currentLevel.showText(TextDialogue([["Sei vorsichtig bei dem Kampf mit den Monstern"]]))
        elif(Game.currentLevel.currentQuest == 3):
            Game.currentLevel.showText(TextDialogue([["Vielen Dank, dass du die Monster besiegt hast!"], 
                                                     ["Wir konnten ihre Basis finden."],
                                                     ["Jedoch ist sie auf einer anderen Insel,", "wo wir nicht so leicht hinkommen."],
                                                     ["Eine Dorfbewohnerin wollte eine Brücke bauen."],
                                                     ["Du solltest sie einmal besuchen gehen.", "Sie ist ganz im Osten der Insel zu finden."]]))
            Game.currentLevel.setCurrentQuest(4)
        elif(Game.currentLevel.currentQuest == 4):
            Game.currentLevel.showText(TextDialogue([["Die Dorfbewohnerin im Osten der Insel", "wollte eine Brücke zur Basis der Monster bauen"]]))
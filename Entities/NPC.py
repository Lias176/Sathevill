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

    def interact(self):
        self.renderInteractText = False
        match(Game.currentLevel.currentQuest):
            case 0:
                Game.currentLevel.showText(TextDialogue([["Der Bürgermeister ist in dem Haus über mir", "zu finden."]]))
            case 4:
                Game.currentLevel.showText(TextDialogue([["Hallo, wir haben die Monsterbasis entdeckt!"],
                                                         ["Sie ist auf der Insel rechts von hier."],
                                                         ["Ich habe eine Brücke gebaut, die auf die Insel führt."],
                                                         ["Jedoch sind dort Monster, weswegen ich die Basis nicht", "erkunden kann."],
                                                         ["Könntest du für uns die Basis erkunden?"],
                                                         ["Viel Glück!"]]))
                Game.currentLevel.setCurrentQuest(5)
            case _:
                Game.currentLevel.showText(TextDialogue([["Hallo Reisender!"], 
                                       ["Willkommen in unserem abgelegenem Dorf."], 
                                       ["Du scheinst, als würdest du dich hier", "noch nicht auskennen."], 
                                       ["Du solltest mit dem Bürgermeister reden"],
                                       ["Er ist in dem Haus über mir zu finden"]]))
import GameElement, pygame

class LevelObject(GameElement.GameElement):
    def __init__(self, pos: tuple):
        GameElement.GameElement.__init__(self, pygame.image.load(self.image).convert(), pos)

def getClassById(id : int):
    for subclass in LevelObject.__subclasses__():
        if(subclass.id == id):
            return subclass
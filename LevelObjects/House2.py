import LevelObject

class House2(LevelObject.LevelObject):
    id = 6
    layer = 1

    def __init__(self, pos: tuple):
        self.image = "images\\House2.png"
        LevelObject.LevelObject.__init__(self, pos)
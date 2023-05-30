import LevelObject

class House(LevelObject.LevelObject):
    id = 4
    layer = 1

    def __init__(self, pos: tuple):
        self.image = "images\\House.png"
        LevelObject.LevelObject.__init__(self, pos)
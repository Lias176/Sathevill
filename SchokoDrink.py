import LevelObject

class SchokoDring(LevelObject.LevelObject):
    id = 0
    layer = 1

    def __init__(self, pos: tuple):
        self.image = "images\\schokoDrink.png"
        self.id = 0
        LevelObject.LevelObject.__init__(self, pos)
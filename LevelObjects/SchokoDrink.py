import LevelObject

class SchokoDring(LevelObject.LevelObject):
    id = 0
    layer = 2

    def __init__(self, pos: tuple):
        self.image = "images\\schokoDrink.png"
        LevelObject.LevelObject.__init__(self, pos)
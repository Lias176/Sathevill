import LevelObject

class Palm(LevelObject.LevelObject):
    id = 1

    def __init__(self, pos: tuple):
        self.image = "images\\palm.png"
        LevelObject.LevelObject.__init__(self, pos)
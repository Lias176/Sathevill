import LevelObject

class Tree(LevelObject.LevelObject):
    id = 2
    layer = 0

    def __init__(self, pos: tuple):
        self.image = "images\\tree.png"
        LevelObject.LevelObject.__init__(self, pos)
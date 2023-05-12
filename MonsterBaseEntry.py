import LevelObject

class MonsterBaseEntry(LevelObject.LevelObject):
    id = 5
    layer = 1

    def __init__(self, pos: tuple):
        self.image = "images\\monsterbaseEntry.png"
        LevelObject.LevelObject.__init__(self, pos)
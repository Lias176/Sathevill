import LevelObject, random

class Grass(LevelObject.LevelObject):
    id = 3
    layer = 0

    def __init__(self, pos: tuple):
        texture = random.randint(0, 3)
        match(texture):
            case 0:
                self.image = "images\\grass.png"
            case 1:
                self.image = "images\\grass1.png"
            case 2:
                self.image = "images\\grass2.png"
            case 3:
                self.image = "images\\grass3.png"
        
        LevelObject.LevelObject.__init__(self, pos)
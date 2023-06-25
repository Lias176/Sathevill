import Textures
from LevelObject import LevelObject
from Point import Point

class MonsterbaseFloor(LevelObject):
    id = "monsterbase_floor"
    layer = 0
    surface = Textures.MONSTER_BASE_FLOOR.surface

    def __init__(self, pos: Point):
        super().__init__(pos)
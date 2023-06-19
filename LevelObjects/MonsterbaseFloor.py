from LevelObject import LevelObject
from Point import Point

class MonsterbaseFloor(LevelObject):
    id: str = "monsterbase_floor"
    layer: int = 0
    image: str = "images\\monsterbaseFloor.png"

    def __init__(self, pos: Point):
        super().__init__(pos)
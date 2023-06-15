from LevelObject import LevelObject
from Point import Point

class Tree(LevelObject):
    id: str = "tree"
    layer: int = 1
    image: str = "images\\tree.png"

    def __init__(self, pos: Point):
        super().__init__(pos)
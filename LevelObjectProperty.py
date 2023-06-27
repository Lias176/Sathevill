from enum import Enum

class PropertyTypes(Enum):
    STRINGLISTLIST = 0

class LevelObjectProperty:
    def __init__(self, name: str,  type: PropertyTypes, var):
        self.type: PropertyTypes = type
        self.name: str = name
        self.var = var
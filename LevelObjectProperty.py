from enum import Enum

class PropertyTypes(Enum):
    STRINGLISTLIST = 0

class LevelObjectProperty:
    def __init__(self, name: str,  type: PropertyTypes, var):
        self.type: PropertyTypes = type
        self.name: str = name
        self.var = var

    def typeAsString(self) -> str:
        match(self.type):
            case PropertyTypes.STRINGLISTLIST:
                return "stringlistlist"

    @classmethod
    def fromString(self, name: str, str: str, var):
        type: PropertyTypes = None
        match(str):
            case "stringlistlist":
                type = PropertyTypes.STRINGLISTLIST
        return LevelObjectProperty(name, type, var)
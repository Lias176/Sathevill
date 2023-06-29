from enum import Enum

class PropertyTypes(Enum):
    STRINGLISTLIST = 0
    STRING = 1

class LevelObjectProperty:
    def __init__(self, name: str,  type: PropertyTypes, var):
        self.type: PropertyTypes = type
        self.name: str = name
        self.var = var

    def typeAsString(self) -> str:
        match(self.type):
            case PropertyTypes.STRINGLISTLIST:
                return "stringlistlist"
            case PropertyTypes.STRING:
                return "string"

    @classmethod
    def fromString(self, name: str, str: str, var):
        type: PropertyTypes = None
        match(str):
            case "stringlistlist":
                type = PropertyTypes.STRINGLISTLIST
            case "string":
                type = PropertyTypes.STRING
        return LevelObjectProperty(name, type, var)
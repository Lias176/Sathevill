import pygame
from GameObject import GameObject
from Point import Point

def isTransparent(object: GameObject, x, y) -> bool:
    try:
        return pygame.Color(object.surface.get_at((x, y))).a == 0
    except:
        return True
    
def hasNotTransparentNabor(object: GameObject, x, y) -> bool:
    return not isTransparent(object, x - 1, y - 1) or not isTransparent(object, x - 1, y) or not isTransparent(object, x - 1, y + 1) or not isTransparent(object, x, y + 1) or not isTransparent(object, x + 1, y + 1) or not isTransparent(object, x + 1, y) or not isTransparent(object, x + 1, y - 1) or not isTransparent(object, x, y - 1)

def drawBorder(object: GameObject, color: pygame.Color) ->  GameObject:
    border: GameObject = GameObject(pygame.Surface((object.surface.get_width() + 2, object.surface.get_height() + 2), pygame.SRCALPHA), Point(0, 0))
    border.pos = Point(object.pos.x - 1, object.pos.y - 1)
    for borderX in range(border.surface.get_width()):
        for borderY in range(border.surface.get_height()):
            x: int = borderX - 1
            y: int = borderY - 1
            if(isTransparent(object, x, y) and hasNotTransparentNabor(object, x, y)):
                border.surface.set_at((borderX, borderY), color)
    return border
import Textures
from Entity import Entity
from Point import Point

class NPC(Entity):
    id = "npc"
    surface = Textures.NPC.surface
    isInteractable = True
    
    def __init__(self, pos: Point):
        super().__init__(pos)
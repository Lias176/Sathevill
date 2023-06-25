import random, Textures, pygame
from LevelObject import LevelObject
from Point import Point

class Stone(LevelObject):
    layer = 1
    id = "stone"
    surface = Textures.STONE_0.surface

    def __init__(self, pos: Point):
        self.surface = pygame.image.load("images\\stone" + str(random.randint(0, 2)) + ".png")
        super().__init__(pos)
        self.collisionRect = self.surface.get_rect()
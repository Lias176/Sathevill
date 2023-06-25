import random, Textures, pygame
from LevelObject import LevelObject
from Point import Point

class Grass(LevelObject):
    layer = 0
    surface = Textures.GRASS_0.surface
    id = "grass"

    def __init__(self, pos: Point):
        self.surface = pygame.image.load("images\\grass" + str(random.randint(0, 3)) + ".png")
        super().__init__(pos)
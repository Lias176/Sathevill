import pygame
from GameElement import GameElement

class Enemy(GameElement):
    def __init__(self):
        GameElement.__init__(self, pygame.image.load("images\\enemy.png"), (0, 0))
        self.damage = 1
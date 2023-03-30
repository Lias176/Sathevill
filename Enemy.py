import pygame, GameElement

class Enemy(GameElement.GameElement):
    def __init__(self):
        GameElement.GameElement.__init__(self, pygame.image.load("images\\enemy.png"), (0, 0))
        self.damage = 1
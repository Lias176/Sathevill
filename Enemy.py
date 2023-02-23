import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        self.speed = 1
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images\\enemy.png").convert()
        self.rect = self.image.get_rect()
        self.damage = 1
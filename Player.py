import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.speed = 1
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images\\player.png").convert()
        self.rect = self.image.get_rect()

    def update(self, time : int):
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_w] or keys[pygame.K_UP]):
            self.rect.y -= self.speed * time
        if(keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.rect.x += self.speed * time
        if(keys[pygame.K_s] or keys[pygame.K_DOWN]):
            self.rect.y += self.speed * time
        if(keys[pygame.K_a] or keys[pygame.K_LEFT]):
            self.rect.x -= self.speed * time
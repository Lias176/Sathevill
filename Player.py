import pygame, Game
from threading import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.speed = 1
        self.lives = 3
        self.isAlive = True
        self.invincible = False
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

        for sprite in Game.sprites:
            try:
                sprite.damage
            except:
                continue
            if(self.rect.colliderect(sprite.rect) and self.lives > 0 and self.invincible == False):
                self.takeDamage(sprite.damage)
                if(self.lives < 0):
                    self.lives = 0
                break
        if(self.lives <= 0): 
            self.isAlive = False

    def takeDamage(self, damageAmount : int):
        self.lives -= damageAmount
        self.invincible = True
        timer = Timer(2, self.removeInvincability)
        timer.start()

    def removeInvincability(self):
        self.invincible = False
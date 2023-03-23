import pygame, GameElement, math, Level
from threading import Timer

class Player(GameElement.GameElement):
    def __init__(self):
        GameElement.GameElement.__init__(self, pygame.image.load("images\\player.png").convert(), (0, 0))
        self.speed = 1
        self.lives = 3
        self.isAlive = True
        self.invincible = False
        self.x = float(0)
        self.y = float(0)

    def update(self, time : int):
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_w] or keys[pygame.K_UP]):
            self.y -= self.speed * (self.speed / 2) * time
        if(keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.x += self.speed * (self.speed / 2) * time
        if(keys[pygame.K_s] or keys[pygame.K_DOWN]):
            self.y += self.speed * (self.speed / 2) * time
        if(keys[pygame.K_a] or keys[pygame.K_LEFT]):
            self.x -= self.speed * (self.speed / 2) * time

        self.pos = (math.floor(self.x), math.floor(self.y))

        for gameElement in Level.gameElements:
            try:
                gameElement.damage
            except:
                continue
            if(pygame.Rect(self.pos[0], self.pos[1], self.surface.get_width(), self.surface.get_height()).colliderect(pygame.Rect(gameElement.pos[0], gameElement.pos[1], gameElement.surface.get_width(), gameElement.surface.get_height())) and self.lives > 0 and self.invincible == False):
                self.takeDamage(gameElement.damage) 
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
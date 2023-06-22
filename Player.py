import pygame, math
from threading import Timer
from Entity import Entity

class Player(Entity):
    def __init__(self):
        super().__init__("images\\player\\front.png")
        self.invincible: bool = False
        self.maxHealth = 3
        self.health = self.maxHealth
        self.controlAngles: dict[int, list[int]] = { 0: [ pygame.K_w, pygame.K_UP ], 180: [ pygame.K_s, pygame.K_DOWN ], 90: [ pygame.K_d, pygame.K_RIGHT ], 270: [ pygame.K_a, pygame.K_LEFT ] }

    def update(self, time: int):
        keys = pygame.key.get_pressed()
        finalAngle: int = -1
        for angle in self.controlAngles:
            isPressed: bool = False
            for key in self.controlAngles[angle]:
                if(keys[key]):
                    isPressed = True
                    break
            if(not isPressed):
                continue
            if(finalAngle < 0):
                finalAngle = angle
                continue
            if(abs(finalAngle - angle) == 180):
                finalAngle = -1
                continue
            if(abs(finalAngle - angle) == 270):
                finalAngle = 325
                continue
            if(finalAngle == 45):
                finalAngle = 0
                continue
            finalAngle = min(finalAngle, angle) + 45

        if(finalAngle >= 0):
            self.x += math.sin(math.radians(finalAngle)) * self.speed * time
            self.y -= math.cos(math.radians(finalAngle)) * self.speed * time

        super().update()

    def takeDamage(self, damageAmount: int):
        super().takeDamage(damageAmount)
        self.invincible = True
        timer = Timer(2, self.removeInvincability)
        timer.start()

    def removeInvincability(self):
        self.invincible = False

    def respawn(self):
        self.x = 0
        self.y = 0
        self.isAlive = True
        self.health = self.maxHealth
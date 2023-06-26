import pygame, math, Game, time
from LevelObject import LevelObject
from Point import Point

class Entity(LevelObject):
    layer = 1
    isEntity = True

    def __init__(self, pos: Point):
        super().__init__(pos)
        self.speed: float = 0.2
        self.maxHealth: int = 1
        self.health: int = self.maxHealth
        self.isAlive: bool = True
        self.x: float = pos.x
        self.y: float = pos.y
        self.renderingLayer: int = 1

    def move(self, x: int, y: int):
        updatedX: bool = False
        updatedY: bool = False
        cameraPos = Game.currentLevel.cameraPos
        for levelObject in Game.currentLevel.levelObjects:
            if(levelObject.collisionRect == None or levelObject.isNotOnScreen(cameraPos)):
                continue

            # set own rendering layer
            collisionRect: pygame.Rect = levelObject.getAbsoluteCollisionRect()
            if(levelObject.layer == 1 and self.colliderect(levelObject.getRect())):
                if(levelObject.collisionRect == None or self.y + self.surface.get_height() >= collisionRect.bottom):
                    if(self.renderingLayer == 0):
                        self.renderingLayer = 1
                        Game.currentLevel.layerEntities[0].remove(self)
                        Game.currentLevel.layerEntities[1].append(self)
                elif(self.renderingLayer == 1):
                        self.renderingLayer = 0
                        Game.currentLevel.layerEntities[1].remove(self)
                        Game.currentLevel.layerEntities[0].append(self)

            # check collision
            updatedXRect: pygame.Rect = pygame.Rect(self.x + x, self.y + self.surface.get_height(), self.surface.get_width(), 1)
            updatedYRect: pygame.Rect = pygame.Rect(self.x, self.y + self.surface.get_height() + y, self.surface.get_width(), 1)
            if(collisionRect.colliderect(updatedXRect)):
                self.x = collisionRect.left - self.surface.get_width() if x > 0 else collisionRect.right
                updatedX = True
            elif(collisionRect.colliderect(updatedYRect)):
                self.y = (collisionRect.top - 1 if y > 0 else collisionRect.bottom) - self.surface.get_height()
                updatedY = True
            if(updatedX or updatedY):
                break
        if(not updatedX):
            self.x += x
        if(not updatedY):
            self.y += y

    def update(self, time: int):
        self.pos = Point(math.floor(self.x), math.floor(self.y))

    def takeDamage(self, damageAmount: int):
        self.health -= damageAmount
        if(self.health <= 0):
            self.isAlive = False
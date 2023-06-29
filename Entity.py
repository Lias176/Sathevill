import pygame, math, Game
from LevelObject import LevelObject
from Point import Point
from Timer import Timer

class Entity(LevelObject):
    layer = 1
    isEntity = True
    isEnemy: bool = False

    def __init__(self, pos: Point):
        super().__init__(pos)
        self.speed: float = 0.2
        self.maxHealth: int = 3
        self.health: int = self.maxHealth
        self.isAlive: bool = True
        self.x: float = pos.x
        self.y: float = pos.y
        self.renderingLayer: int = 1
        self.xVelocity: int = 0
        self.yVelocity: int = 0
        self.healthBar: pygame.Surface = pygame.Surface((100, 10))
        self.updateHealthBar()

    def updateHealthBar(self):
        if(not self.isEnemy):
            return
        self.healthBar.fill(pygame.Color(255, 255, 255))
        healthRect: pygame.Rect = (0, 0, 100 / (self.maxHealth / self.health), 10)
        self.healthBar.fill(pygame.Color(255, 0, 0), healthRect)

    def move(self, x: int, y: int):
        updatedX: bool = False
        updatedY: bool = False
        cameraPos = Game.currentLevel.cameraPos
        # set own rendering layer
        if 1 in Game.currentLevel.layerLevelObjects:
            for obj in Game.currentLevel.layerLevelObjects[1]:
                if(obj.isNotOnScreen(cameraPos)):
                    continue
                if(self.colliderect(obj.getRect())):
                    if(obj.collisionRect == None or self.y + self.surface.get_height() >= obj.getAbsoluteCollisionRect().bottom):
                        if(self.renderingLayer == 0):
                            self.renderingLayer = 1
                            try:
                                Game.currentLevel.layerEntities[0].remove(self)
                            except:
                                pass
                            Game.currentLevel.layerEntities[1].append(self)
                    elif(self.renderingLayer == 1):
                            self.renderingLayer = 0
                            try:
                                Game.currentLevel.layerEntities[1].remove(self)
                            except:
                                pass
                            Game.currentLevel.layerEntities[0].append(self)
        else:
            self.renderingLayer = 1
        for levelObject in Game.currentLevel.collisionObjects:
            if(levelObject.isNotOnScreen(cameraPos)):
                continue

            collisionRect: pygame.Rect = levelObject.getAbsoluteCollisionRect()
            updatedXRect: pygame.Rect = pygame.Rect(self.x + x, self.y + self.surface.get_height(), self.surface.get_width(), 1)
            updatedYRect: pygame.Rect = pygame.Rect(self.x, self.y + self.surface.get_height() + y, self.surface.get_width(), 1)
            if(collisionRect.colliderect(updatedXRect)):
                self.x = collisionRect.left - self.surface.get_width() if x > 0 else collisionRect.right
                updatedX = True
            elif(collisionRect.colliderect(updatedYRect)):
                self.y = (collisionRect.top - 1 if y > 0 else collisionRect.bottom) - self.surface.get_height()
                updatedY = True
        if(not updatedX):
            self.x += x
        if(not updatedY):
            self.y += y

    def update(self, time: int):
        if(self.xVelocity != 0):
            if(self.xVelocity < 0):
                self.x += self.xVelocity
                self.xVelocity = min(self.xVelocity + time, 0)
            else:
                self.x += self.xVelocity
                self.xVelocity = max(self.xVelocity - time, 0)
        if(self.yVelocity != 0):
            if(self.yVelocity < 0):
                self.y += self.yVelocity
                self.yVelocity = min(self.yVelocity + time, 0)
            else:
                self.y += self.yVelocity
                self.yVelocity = max(self.yVelocity - time, 0)

        self.pos = Point(math.floor(self.x), math.floor(self.y))

    def takeDamage(self, damageAmount: int, removeFromList: bool = True):
        self.health -= damageAmount
        if(self.health <= 0):
            self.isAlive = False
            if(removeFromList):
                Game.currentLevel.removeEntity(self)
            return
        self.addOverlayColor(pygame.Color(255, 0, 0, 150))
        removeColorTimer = Timer(500, self.removeOverlayColor)
        removeColorTimer.start()
        self.updateHealthBar()

    def removeColor(self):
        self.removeOverlayColor()

    def renderAt(self, screen: pygame.Surface, pos: tuple[int, int]):
        super().renderAt(screen, pos)
        if(self.isEnemy):
            screen.blit(self.healthBar, (pos[0] + self.surface.get_width() / 2 - 50, pos[1] - 20))
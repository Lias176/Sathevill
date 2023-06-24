import pygame, math, Textures, Game
from threading import Timer
from Entity import Entity
from Point import Point
from Animation import Animation
from Directions import Directions

class Player(Entity):
    def __init__(self):
        self.WALK_UP_ANIMATION = Animation(self, [ Textures.PLAYER_WALK_UP_0.surface, Textures.PLAYER_WALK_UP_1.surface ], 250)
        self.WALK_RIGHT_ANIMATION = Animation(self, [ Textures.PLAYER_WALK_RIGHT_0.surface, Textures.PLAYER_WALK_RIGHT_1.surface ], 250)
        self.WALK_DOWN_ANIMATION = Animation(self, [ Textures.PLAYER_WALK_DOWN_0.surface, Textures.PLAYER_WALK_DOWN_1.surface ], 250)
        self.WALK_LEFT_ANIMATION = Animation(self, [ Textures.PLAYER_WALK_LEFT_0.surface, Textures.PLAYER_WALK_LEFT_1.surface ], 250)

        super().__init__(Textures.PLAYER_DOWN.surface)
        self.invincible: bool = False
        self.maxHealth: int = 3
        self.health: int = self.maxHealth
        self.direction: Directions = Directions.DOWN
        self.movedLastFrame: bool = False
        self.walkAnimation: Animation = None

    def update(self, time: int):
        keys = pygame.key.get_pressed()
        directionPoint: Point = Point(0, 0)
        if(keys[pygame.K_w] or keys[pygame.K_UP]):
            directionPoint.y += 1
        if(keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            directionPoint.x += 1
        if(keys[pygame.K_s] or keys[pygame.K_DOWN]):
            directionPoint.y -= 1
        if(keys[pygame.K_a] or keys[pygame.K_LEFT]):
            directionPoint.x -= 1

        if not directionPoint.equals(Point(0, 0)):
            self.movedLastFrame = True
            angle: int = -1
            if(directionPoint.x == 0):
                angle = 0 if directionPoint.y == 1 else 180
            elif(directionPoint.y == 0):
                angle = 90 if directionPoint.x == 1 else 270
            else:
                if(directionPoint.y > 0):
                    angle = math.degrees(math.atan(directionPoint.y / directionPoint.x))
                else:
                    angle = 180 + math.degrees(math.atan(directionPoint.y / directionPoint.x))
                if(angle < 0):
                    angle = 360 + angle
            if(angle == 0):
                if(not self.walkAnimation == self.WALK_UP_ANIMATION):
                    self.direction = Directions.UP
                    if(self.walkAnimation != None):
                        self.walkAnimation.stop()
                    self.walkAnimation = self.WALK_UP_ANIMATION
                    self.walkAnimation.play()
            elif(angle == 180):
                if(not self.walkAnimation == self.WALK_DOWN_ANIMATION):
                    self.direction = Directions.DOWN
                    if(self.walkAnimation != None):
                        self.walkAnimation.stop()
                    self.walkAnimation = self.WALK_DOWN_ANIMATION
                    self.walkAnimation.play()
            elif(angle < 180):
                if(not self.walkAnimation == self.WALK_RIGHT_ANIMATION):
                    self.direction = Directions.RIGHT
                    if(self.walkAnimation != None):
                        self.walkAnimation.stop()
                    self.walkAnimation = self.WALK_RIGHT_ANIMATION
                    self.walkAnimation.play()
            elif(not self.walkAnimation == self.WALK_LEFT_ANIMATION):
                self.direction = Directions.LEFT
                if(self.walkAnimation != None):
                    self.walkAnimation.stop()
                self.walkAnimation = self.WALK_LEFT_ANIMATION
                self.walkAnimation.play()
            x: int = math.sin(math.radians(angle)) * self.speed * time
            y: int = -(math.cos(math.radians(angle)) * self.speed * time)

            updatedX: bool = False
            updatedY: bool = False
            for levelObject in Game.currentLevel.levelObjects:
                if(levelObject.collisionRect == None):
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
                if(updatedX or updatedY):
                    break
            if(not updatedX):
                self.x += x
            if(not updatedY):
                self.y += y
        else:
            if(self.walkAnimation != None):
                self.walkAnimation.stop()
                self.walkAnimation = None
            if(self.movedLastFrame):
                match(self.direction):
                    case Directions.UP:
                        self.surface = Textures.PLAYER_UP.surface
                    case Directions.RIGHT:
                        self.surface = Textures.PLAYER_RIGHT.surface
                    case Directions.DOWN:
                        self.surface = Textures.PLAYER_DOWN.surface
                    case Directions.LEFT:
                        self.surface = Textures.PLAYER_LEFT.surface
            self.movedLastFrame = False

        super().update(time)

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
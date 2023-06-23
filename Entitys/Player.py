import pygame, math, Textures
from threading import Timer
from Entity import Entity
from Point import Point
from Directions import Directions

class Player(Entity):
    def __init__(self):
        super().__init__(Textures.PLAYER_DOWN.surface)
        self.invincible: bool = False
        self.maxHealth: int = 3
        self.health: int = self.maxHealth
        self.lastWalkAnimationUpdate: int = 0
        self.currentWalkAnimationFrame: int = 0
        self.direction: Directions = Directions.DOWN
        self.walkedLastFrame: bool = False

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

        angle: int = -1
        if not directionPoint.equals(Point(0, 0)):
            angle: int = 0
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
            self.x += math.sin(math.radians(angle)) * self.speed * time
            self.y -= math.cos(math.radians(angle)) * self.speed * time

        self.setAnimation(angle, time)

        super().update(time)

    def setAnimation(self, angle: int, time: int):
        if(angle < 0):
            if(self.walkedLastFrame):
                match(self.direction):
                    case Directions.UP:
                        self.surface = Textures.PLAYER_UP.surface
                    case Directions.RIGHT:
                        self.surface = Textures.PLAYER_RIGHT.surface
                    case Directions.DOWN:
                        self.surface = Textures.PLAYER_DOWN.surface
                    case Directions.LEFT:
                        self.surface = Textures.PLAYER_LEFT.surface
            self.walkedLastFrame = False
            self.lastWalkAnimationUpdate = 0
            return
        self.walkedLastFrame = True
        if(angle == 0):
            if(not self.direction == Directions.UP):
                self.surface = Textures.PLAYER_WALK_UP_0.surface
                self.direction = Directions.UP
        elif(angle == 180):
            if(not self.direction == Directions.DOWN):
                self.surface = Textures.PLAYER_WALK_DOWN_0.surface
                self.direction = Directions.DOWN
        elif(angle < 180):
            if(not self.direction == Directions.RIGHT):
                self.surface = Textures.PLAYER_WALK_RIGHT_0.surface
                self.direction = Directions.RIGHT
        else:
            if(not self.direction == Directions.LEFT):
                self.surface = Textures.PLAYER_WALK_LEFT_0.surface
                self.direction = Directions.LEFT

        nextFrame: bool = False
        if(self.lastWalkAnimationUpdate > 250):
            self.lastWalkAnimationUpdate = self.lastWalkAnimationUpdate - 250
            nextFrame = True
        else:
            self.lastWalkAnimationUpdate += time
        if(not nextFrame):
            return
        
        self.currentWalkAnimationFrame = 1 if self.currentWalkAnimationFrame == 0 else 0
        match(self.direction):
            case Directions.UP:
                self.surface = Textures.PLAYER_WALK_UP_0.surface if self.currentWalkAnimationFrame == 1 else Textures.PLAYER_WALK_UP_1.surface
                return
            case Directions.RIGHT:
                self.surface = Textures.PLAYER_WALK_RIGHT_0.surface if self.currentWalkAnimationFrame == 1 else Textures.PLAYER_WALK_RIGHT_1.surface
                return
            case Directions.DOWN:
                self.surface = Textures.PLAYER_WALK_DOWN_0.surface if self.currentWalkAnimationFrame == 1 else Textures.PLAYER_WALK_DOWN_1.surface
                return
            case Directions.LEFT:
                self.surface = Textures.PLAYER_WALK_LEFT_0.surface if self.currentWalkAnimationFrame == 1 else Textures.PLAYER_WALK_LEFT_1.surface
                return

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
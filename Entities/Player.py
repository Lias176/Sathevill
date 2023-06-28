import pygame, math, Textures, Game, time
from Timer import Timer
from Entity import Entity
from Point import Point
from Animation import Animation
from Directions import Directions
from LevelObject import LevelObject

class Player(Entity):
    id = "player"
    surface = Textures.PLAYER_DOWN.surface

    def __init__(self, pos: Point):
        self.WALK_UP_ANIMATION = Animation(self, [ Textures.PLAYER_WALK_UP_0.surface, Textures.PLAYER_WALK_UP_1.surface ], 250, True)
        self.WALK_RIGHT_ANIMATION = Animation(self, [ Textures.PLAYER_WALK_RIGHT_0.surface, Textures.PLAYER_RIGHT.surface,  Textures.PLAYER_WALK_RIGHT_1.surface, Textures.PLAYER_RIGHT.surface ], 250, True)
        self.WALK_DOWN_ANIMATION = Animation(self, [ Textures.PLAYER_WALK_DOWN_0.surface, Textures.PLAYER_WALK_DOWN_1.surface ], 250, True)
        self.WALK_LEFT_ANIMATION = Animation(self, [ Textures.PLAYER_WALK_LEFT_0.surface, Textures.PLAYER_LEFT.surface, Textures.PLAYER_WALK_LEFT_1.surface, Textures.PLAYER_LEFT.surface ], 250, True)

        super().__init__(pos)
        self.invincible: bool = False
        self.maxHealth: int = 3
        self.health: int = self.maxHealth
        self.direction: Directions = Directions.DOWN
        self.movedLastFrame: bool = False
        self.walkAnimation: Animation = None
        self.canAttack: bool = True

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
                angle = math.degrees(math.atan(directionPoint.y / directionPoint.x)) + (180 if directionPoint.y <= 0 else 0)
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
            self.move(math.sin(math.radians(angle)) * self.speed * time, -(math.cos(math.radians(angle)) * self.speed * time))
        else:
            if(self.walkAnimation != None):
                self.walkAnimation.stop()
                self.walkAnimation = None
            if(self.movedLastFrame):
                match(self.direction):
                    case Directions.UP:
                        self.setSurface(Textures.PLAYER_UP.surface)
                    case Directions.RIGHT:
                        self.setSurface(Textures.PLAYER_RIGHT.surface)
                    case Directions.DOWN:
                        self.setSurface(Textures.PLAYER_DOWN.surface)
                    case Directions.LEFT:
                        self.setSurface(Textures.PLAYER_LEFT.surface)
            self.movedLastFrame = False

        super().update(time)

    def checkRenderInteraction(self, object: LevelObject):
        aimRect: pygame.Rect = self.getAimRect()
        if(object.colliderect(aimRect)):
            if(not object.renderInteractText):
                object.activateInteractText()
        elif(object.renderInteractText):
            object.renderInteractText = False

    def move(self, x: int, y: int):
        super().move(x, y)
        for obj in Game.currentLevel.interactableObjects:
            if(obj.isNotOnScreen(Game.currentLevel.cameraPos)):
                continue
            self.checkRenderInteraction(obj)
    
    def interact(self):
        for entity in Game.currentLevel.entities:
            if(entity.renderInteractText == False):
                continue
            entity.interact()
            break
        for object in Game.currentLevel.levelObjects:
            if(object.renderInteractText == False):
                continue
            object.interact()
            break

    def takeDamage(self, damageAmount: int):
        super().takeDamage(damageAmount, False)
        self.invincible = True
        invincabilityTimer = Timer(1000, self.removeInvincability)
        invincabilityTimer.start()

    def removeColor(self):
        self.removeOverlayColor()

    def removeInvincability(self):
        self.invincible = False

    def respawn(self):
        self.x = 0
        self.y = 0
        self.isAlive = True
        self.health = self.maxHealth

    def getAimRect(self) -> pygame.Rect:
        centerPos: Point = self.getCenterPos()
        match(self.direction):
            case Directions.UP:
                return pygame.Rect(centerPos.x - 40, self.y - 50, 80, 50)
            case Directions.RIGHT:
                return pygame.Rect(self.x + 36, centerPos.y - 40, 50, 80)
            case Directions.LEFT:
                return pygame.Rect(self.x - 45, centerPos.y - 40, 50, 80)
            case Directions.DOWN:
                return pygame.Rect(centerPos.x - 40, self.y + 90, 80, 50)

    def attack(self):
        if(not self.canAttack):
            return
        centerPos: Point = self.getCenterPos()
        hasHitEnemy: bool = False
        for entity in Game.currentLevel.entities:
            if(entity == self or entity.isNotOnScreen(Game.currentLevel.cameraPos) or not entity.colliderect(self.getAimRect()) or not entity.isEnemy):
                continue
            hasHitEnemy = True
            entity.takeDamage(1)
            entityCenterPos = entity.getCenterPos()
            angle: int = 0
            if(centerPos.x != entityCenterPos.x):
                angle = math.degrees(math.atan((centerPos.y - entityCenterPos.y) / (centerPos.x - entityCenterPos.x))) + (90 if entityCenterPos.x > centerPos.x else 270)
            entity.xVelocity = math.sin(math.radians(angle)) * self.speed * 200
            entity.yVelocity = -(math.cos(math.radians(angle)) * self.speed * 200)
        if(hasHitEnemy):
            self.canAttack = False
            timer: Timer = Timer(1000, self.canAttackTrue)
            timer.start()

    def canAttackTrue(self):
        self.canAttack = True
            
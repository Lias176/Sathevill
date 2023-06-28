import pygame, Game, math
from Entity import Entity
from Point import Point
from Entities.Player import Player
from Directions import Directions

class Enemy(Entity):
    isEnemy = True
    surfaceRight: pygame.Surface = None
    surfaceLeft: pygame.Surface = None
    surface = surfaceRight

    def __init__(self, pos: Point):
        super().__init__(pos)
        self.attackCooldown: int = 0
        self.seeDistance: int = 350
        self.attackDistance: int = 65
        self.damage: int = 1
        self.direction: Directions = Directions.RIGHT
        self.attackCooldownAmount: int = 2000

    def update(self, time: int):
        super().update(time)
        player: Player = Game.currentLevel.player
        centerPos: Point = self.getCenterPos()
        playerCenterPos: Point = player.getCenterPos()
        distance = centerPos.getDistance(playerCenterPos)
        if(self.attackCooldown > 0):
            self.attackCooldown -= time
        if(distance <= self.seeDistance and distance > self.attackDistance):
            angle: float = -1
            if(centerPos.x == playerCenterPos.x):
                angle = 0
            else:
                angle = math.degrees(math.atan((centerPos.y - playerCenterPos.y) / (centerPos.x - playerCenterPos.x))) + (90 if playerCenterPos.x > centerPos.x else 270)
            if(angle > 180):
                if(self.direction != Directions.LEFT):
                    self.direction = Directions.LEFT
                    self.setSurface(self.surfaceLeft)
            elif(self.direction != Directions.RIGHT):
                self.direction = Directions.RIGHT
                self.setSurface(self.surfaceRight)
            self.move(math.sin(math.radians(angle)) * self.speed * time, -(math.cos(math.radians(angle)) * self.speed * time))
        elif(distance <= self.attackDistance and self.attackCooldown <= 0 and not player.invincible):
            player.takeDamage(self.damage)
            self.attackCooldown = self.attackCooldownAmount
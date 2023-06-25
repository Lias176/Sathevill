import Textures, Game, math
from Entity import Entity
from Point import Point
from Directions import Directions
from .Player import Player

class Slime(Entity):
    id = "slime"
    surface = Textures.SLIME_RIGHT.surface

    def __init__(self, pos: Point):
        super().__init__(pos)
        self.speed = 0.05
        self.direction: Directions = Directions.RIGHT
        self.damage: int = 1

    def update(self, time: int):
        super().update(time)
        player: Player = Game.currentLevel.player
        centerPos: Point = self.getCenterPos()
        playerCenterPos: Point = player.getCenterPos()
        distance = centerPos.getDistance(playerCenterPos)
        if(distance < 350 and distance > 50):
            angle: float = -1
            if(centerPos.x == playerCenterPos.x):
                angle = 0
            else:
                angle = math.degrees(math.atan((centerPos.y - playerCenterPos.y) / (centerPos.x - playerCenterPos.x))) + (90 if playerCenterPos.x > centerPos.x else 270)
            if(angle > 180):
                if(self.direction != Directions.LEFT):
                    self.direction = Directions.LEFT
                    self.setSurface(Textures.SLIME_LEFT.surface)
            elif(self.direction != Directions.RIGHT):
                self.direction = Directions.RIGHT
                self.setSurface(Textures.SLIME_RIGHT.surface)
            self.move(math.sin(math.radians(angle)) * self.speed * time, -(math.cos(math.radians(angle)) * self.speed * time))
        elif(distance <= 50):
            if(not player.invincible):
                player.takeDamage(self.damage)
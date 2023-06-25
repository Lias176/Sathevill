from __future__ import annotations
import math

class Point:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    @staticmethod
    def fromTuple(point: tuple[int, int]) -> Point:
        return Point(point[0], point[1])

    def toTuple(self) -> tuple[int, int]:
        return (self.x, self.y)
    
    def toString(self) -> str:
        return "x: " + str(self.x) + " y: " + str(self.y)
    
    def equals(self, p: Point) -> bool:
        return self.x == p.x and self.y == p.y
    
    def reverseSign(self) -> Point:
        return Point(-self.x, -self.y)
    
    def offset(self, offset: Point) -> Point:
        return Point(self.x + offset.x, self.y + offset.y)
    
    def getDistance(self, p: Point) -> int:
        return math.floor(math.sqrt((self.x - p.x) ** 2 + (self.y - p.y) ** 2))
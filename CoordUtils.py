from Point import Point
import math

def blockFromPoint(point: Point) -> Point:
    return Point(math.floor(point.x / 50), math.floor(point.y / 50))

def pointFromBlock(block: Point) -> Point:
    return Point(block.x * 50, block.y * 50)

def snapToLevelGrid(point: Point) -> Point:
    return pointFromBlock(blockFromPoint(point))
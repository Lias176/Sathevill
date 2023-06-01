from __future__ import annotations

class Point:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    @staticmethod
    def fromTuple(point: tuple[int, int]) -> Point:
        return Point(point[0], point[1])

    def asTuple(self) -> tuple[int, int]:
        return (self.x, self.y)
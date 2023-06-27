import pygame
from UIElement import UIElement
from Point import Point
from InputBox import InputBox

class InputBoxList(UIElement):
    def __init__(self, pos: Point, boxWidth: int, boxHeight: int, texts: list[list[str]]):
        self.pos: Point = pos
        self.boxWidth: int = boxWidth
        self.boxHeight: int = boxHeight
        self.texts: list[list[str]] = texts
        self.boxes: list[InputBox] = []
        if(len(self.texts) == 0):
            self.texts.append([])
        self.boxes.append(InputBox(self.pos, self.boxWidth, self.boxHeight, self.texts[0], self.onType))
        self.onType()

    def remove(self):
        for box in self.boxes:
            box.remove()
        
    def render(self, screen: pygame.Surface):
        for box in self.boxes:
            box.render(screen)

    def updatePositions(self):
        for i, box in enumerate(self.boxes):
            box.setPos(Point(box.pos.x, (self.boxes[i - 1].pos.y + self.boxes[i - 1].height + 10) if i >= 1 else self.pos.y))

    def onType(self):
        if(len(self.boxes) == 0):
            return
        removedBox: bool = False
        for i, box in enumerate(self.boxes):
            if(i >= len(self.boxes) - 1):
                continue
            if(box.isEmpty()):
                self.boxes[i].remove()
                self.boxes.pop(i)
                self.texts.pop(i)
                removedBox = True
            
        while(not self.boxes[-1].isEmpty()):
            while(len(self.texts) <= len(self.boxes)):
                self.texts.append([])
            self.boxes.append(InputBox(Point(self.pos.x, self.boxes[-1].pos.y + self.boxes[-1].height + 10), self.boxWidth, self.boxHeight, self.texts[len(self.boxes)], self.onType))

        if(removedBox):
            self.updatePositions()
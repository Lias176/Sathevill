from __future__ import annotations
import pygame
from UIElement import UIElement
from Point import Point
from GameObject import GameObject

class InputBox(UIElement):
    inputBoxes: list[InputBox] = []

    def __init__(self, pos: Point, width: int, height: int, text: list[str], onType: callable = None):
        self.pos = pos
        self.text: list[str] = text
        self.selected: bool = False
        self.width = width
        self.height = height
        self.onType: callable = onType
        self.bgObject = GameObject(pygame.Surface((width, height)), pos)
        self.bgObject.surface.fill(pygame.Color(30, 30, 30))
        self.fontRender: list[GameObject] = None
        self.inputBoxes.append(self)
        self.currentLine: int = 0
        self.runOnType: bool = False
        self.updateFontRender()
        self.runOnType = True

    def remove(self):
        self.inputBoxes.remove(self)

    def render(self, screen: pygame.Surface):
        self.bgObject.render(screen)
        if(self.fontRender != None):
            for text in self.fontRender:
                text.render(screen)

    def setPos(self, pos: Point):
        self.pos = pos
        self.bgObject.pos = pos
        if(self.fontRender == None):
            return
        for i, line in enumerate(self.fontRender):
            line.pos = self.pos.offset(Point(5, 5 + i * 20))

    def updateFontRender(self):
        self.fontRender = []
        for i, line in enumerate(self.text):
            self.fontRender.append(GameObject(pygame.font.Font("fonts\\Roboto-Regular.ttf", 20).render(line, True, pygame.Color(255, 255, 255)), self.pos.offset(Point(5, 5 + i * 20))))
        if(self.runOnType and self.onType != None):
            self.onType()

    def removeLetter(self):
        if((len(self.text) <= self.currentLine or self.text[self.currentLine] == "") and len(self.text) > 0):
            self.text.pop(self.currentLine)
            self.currentLine = max(self.currentLine - 1, 0)
            return
        self.text[self.currentLine] = self.text[self.currentLine][:-1]
        if(self.text[self.currentLine] == ""):
            self.text.pop(self.currentLine)
            self.currentLine = max(self.currentLine - 1, 0)
        self.updateFontRender()

    def addLetter(self, letter: str):
        if(letter == "space"):
            letter = " "
        elif(letter == "return" or letter == "down"):
            self.currentLine += 1
            return
        elif(letter == "backspace"):
            self.removeLetter()
            return
        elif(letter == "up"):
            self.currentLine = max(self.currentLine - 1, 0)
            return

        while(len(self.text) <= self.currentLine):
            self.text.append("")
        self.text[self.currentLine] += letter
        self.updateFontRender()

    def isEmpty(self) -> bool:
        for line in self.text:
            if line != "":
                return False
        return True

    @classmethod
    def onClick(self, button: int, pos: Point):
        if(button != 1):
            return
        for box in self.inputBoxes:
            if(box.bgObject.collidepoint(pos)):
                box.selected = True
                return
            box.selected = False

    @classmethod
    def onKey(self, key: int):
        for box in self.inputBoxes:
            if(not box.selected):
                continue
            box.addLetter(pygame.key.name(key))
            break
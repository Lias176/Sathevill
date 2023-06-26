from __future__ import annotations
import pygame
from GameObject import GameObject

class Animation:
    animations: list[Animation] = []

    def __init__(self, object: GameObject, surfaces: list[pygame.Surface], frameDuration: int, loop: bool):
        self.surfaces: list[pygame.Surface] = surfaces
        self.frameDuration: int = frameDuration
        self.object: GameObject = object
        self.animations.append(self)
        self.timeSinceLastUpdate: int = 0
        self.currentFrame: int = 0
        self.isRunning: bool = False
        self.loop: bool = loop

    def update(self, time: int):
        if(not self.isRunning):
            return
        self.timeSinceLastUpdate += time
        if(self.timeSinceLastUpdate < self.frameDuration):
            return
        self.timeSinceLastUpdate -= self.frameDuration
        if(self.currentFrame >= len(self.surfaces) - 1):
            if(not self.loop):
                self.stop()
                return
            self.currentFrame = 0
        else:
            self.currentFrame += 1
        self.object.setSurface(self.surfaces[self.currentFrame])

    def play(self):
        self.object.setSurface(self.surfaces[0])
        self.isRunning = True
    
    def stop(self):
        self.isRunning = False
        self.currentFrame = 0
        self.timeSinceLastUpdate = 0
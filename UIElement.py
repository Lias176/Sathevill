import pygame
from dataclasses import dataclass

@dataclass
class UIElement:
    surface: pygame.Surface
    pos: tuple
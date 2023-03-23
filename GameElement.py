import pygame
from dataclasses import dataclass

@dataclass
class GameElement:
    surface: pygame.Surface
    pos: tuple
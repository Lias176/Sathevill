import pygame, Button
from enum import Enum

screen = None

def setMenu(menu):
    if(menu == Menus.MainMenu):
        button = Button.Button(screen, "Play", pygame.font.SysFont("Arial", 25), "black", "white", pygame.Rect(0, 0, 100, 50), Button.PositionOffset.CenterScreen, mainMenu_playOnClick)

class Menus(Enum):
    MainMenu = 0

def mainMenu_playOnClick():
    print("aa")
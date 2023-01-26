import pygame, Button
from enum import Enum

screen = None

def setMenu(menu):
    if(menu == Menus.MainMenu):
        button = Button.Button(screen, "Play", pygame.font.SysFont("Arial", 25), "black", "white", pygame.Rect(40, 40, 100, 50), mainMenu_playOnClick)

class Menus(Enum):
    MainMenu = 0

def mainMenu_playOnClick():
    print("aa")
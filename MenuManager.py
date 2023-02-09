import pygame, Button, sys
from enum import Enum

screen = None

def setMenu(menu):
    if(menu == Menus.MainMenu):
        playButton = Button.Button("Play", pygame.font.SysFont("Arial", 30, True), "black", "white", pygame.Rect(0, 60, 400, 50), Button.PositionOffset.CenterScreen, mainMenu_playButtonOnClick)
        optionsButton = Button.Button("Options", pygame.font.SysFont("Arial", 30, True), "black", "white", pygame.Rect(0, 0, 400, 50), Button.PositionOffset.CenterScreen, mainMenu_optionsButtonOnClick)
        quitButton = Button.Button("Quit", pygame.font.SysFont("Arial", 30, True), "black", "white", pygame.Rect(0, -60, 400, 50), Button.PositionOffset.CenterScreen, mainMenu_quitButtonOnClick)

class Menus(Enum):
    MainMenu = 0

def mainMenu_playButtonOnClick():
    print("play")

def mainMenu_optionsButtonOnClick():
    print("options")

def mainMenu_quitButtonOnClick():
    sys.exit()
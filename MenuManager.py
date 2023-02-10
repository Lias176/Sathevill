import pygame, Button, sys
from enum import Enum

screen = None

buttons = []

def setMenu(menu):
    global buttons
    if(len(buttons) > 0):
        for button in buttons:
            button.remove()
        buttons = []
        screen.fill("black")

    if(menu == Menus.MainMenu):
        buttons = [
            Button.Button("Play", pygame.font.SysFont("Arial", 30, True), "black", "white", pygame.Rect(0, 60, 400, 50), Button.PositionOffset.CenterScreen, mainMenu_playButtonOnClick),
            Button.Button("Options", pygame.font.SysFont("Arial", 30, True), "black", "white", pygame.Rect(0, 0, 400, 50), Button.PositionOffset.CenterScreen, mainMenu_optionsButtonOnClick),
            Button.Button("Quit", pygame.font.SysFont("Arial", 30, True), "black", "white", pygame.Rect(0, -60, 400, 50), Button.PositionOffset.CenterScreen, mainMenu_quitButtonOnClick),
        ]
    elif(menu == Menus.OptionsMenu):
        buttons = [
            Button.Button("Back", pygame.font.SysFont("Arial", 30, True), "black", "white", pygame.Rect(0, 60, 400, 50), Button.PositionOffset.CenterScreen, optionsMenu_backButtonOnClick)
        ]

class Menus(Enum):
    MainMenu = 0,
    OptionsMenu = 1

# MainMenu
def mainMenu_playButtonOnClick():
    print("play")

def mainMenu_optionsButtonOnClick():
    setMenu(Menus.OptionsMenu)

def mainMenu_quitButtonOnClick():
    sys.exit()

# OptionsMenu
def optionsMenu_backButtonOnClick():
    setMenu(Menus.MainMenu)
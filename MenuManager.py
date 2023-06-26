import pygame, sys, functools, Game, os, tkinter, Level
from enum import Enum
from tkinter import filedialog
from Button import Button
from LevelCreator import LevelCreator
from UIElement import UIElement
from TextBox import TextBox
from Point import Point

class Menus(Enum):
    MainMenu = 0,
    OptionsMenu = 1,
    PlayMenu = 2,
    PauseMenu = 3,
    DeathMenu = 4,
    LevelCreatorMenu = 5

uiElements: list[UIElement] = []
currentMenu = None

def keyPressed(key : int):
    match key:
        case pygame.K_ESCAPE:
            match(currentMenu):
                case Menus.PauseMenu:
                    Game.currentLevel.pause(False)
                case Menus.LevelCreatorMenu:
                    Game.currentLevelCreator.openMenu(False)
                
def render(screen : pygame.Surface):
    screen.fill(pygame.Color(15, 15, 15))
    for uiElement in uiElements:
        uiElement.render(screen)

def setMenu(menu):
    global currentMenu, uiElements
    currentMenu = menu
    if(len(uiElements) > 0):
        for uiElement in uiElements:
            if(type(uiElement) == Button):
                uiElement.remove()
        uiElements = []
    
    match menu:
        case Menus.MainMenu:
            uiElements = [
                Button("Play", pygame.Rect(0, 90, 400, 50), mainMenu_playButtonOnClick),
                Button("Options", pygame.Rect(0, 30, 400, 50), mainMenu_optionsButtonOnClick),
                Button("Level creator", pygame.Rect(0, -30, 400, 50), mainMenu_levelCreatorButtonOnClick),
                Button("Quit", pygame.Rect(0, -90, 400, 50), mainMenu_quitButtonOnClick)
            ]
        case Menus.OptionsMenu:
            uiElements = [
                Button("Back", pygame.Rect(0, 0, 400, 50), optionsMenu_backButtonOnClick)
            ]
        case Menus.PlayMenu:
            uiElements = [
                Button("Back", pygame.Rect(0, 150, 400, 50), playMenu_backButtonOnClick),
                Button("Save 1", pygame.Rect(0, 90, 400, 50), functools.partial(playMenu_saveButtonOnClick, 1)),
                Button("Save 2", pygame.Rect(0, 30, 400, 50), functools.partial(playMenu_saveButtonOnClick, 2)),
                Button("Save 3", pygame.Rect(0, -30, 400, 50), functools.partial(playMenu_saveButtonOnClick, 3)),
                Button("Save 4", pygame.Rect(0, -90, 400, 50), functools.partial(playMenu_saveButtonOnClick, 4)),
                Button("Save 5", pygame.Rect(0, -150, 400, 50), functools.partial(playMenu_saveButtonOnClick, 5))
            ]
        case Menus.PauseMenu:
            uiElements = [
                Button("Continue", pygame.Rect(0, 30, 400, 50), pauseMenu_continueButtonOnClick),
                Button("Back to Main Menu", pygame.Rect(0, -30, 400, 50), pauseMenu_backToMainMenuOnClick)
            ]
        case Menus.DeathMenu:
            uiElements = [
                TextBox("Du bist gestorben!", Point(0, 115), pygame.font.Font("fonts\\Roboto-Bold.ttf", 60)),
                Button("Respawn", pygame.Rect(0, 30, 400, 50), deathMenu_respawnOnClick),
                Button("Back to Main Menu", pygame.Rect(0, -30, 400, 50), deathMenu_backToMainMenuOnClick)
            ]
        case Menus.LevelCreatorMenu:
            uiElements = [
                Button("Back to LevelCreator", pygame.Rect(0, 90, 400, 50), levelCreatorMenu_backToLevelCreatorOnClick),
                Button("Load Level", pygame.Rect(0, 30, 400, 50), levelCreatorMenu_loadLevelOnClick),
                Button("Save Level", pygame.Rect(0, -30, 400, 50), levelCreatorMenu_saveLevelOnClick),
                Button("Back to Main Menu", pygame.Rect(0, -90, 400, 50), levelCreatorMenu_backToMainMenuOnClick)
            ]

# MainMenu
def mainMenu_playButtonOnClick():
    setMenu(Menus.PlayMenu)

def mainMenu_optionsButtonOnClick():
    setMenu(Menus.OptionsMenu)

def mainMenu_levelCreatorButtonOnClick():
    Game.currentLevelCreator = LevelCreator()
    Game.state = Game.GameState.IN_LEVEL_CREATOR
    setMenu(None)

def mainMenu_quitButtonOnClick():
    sys.exit()

# PlayMenu
def playMenu_backButtonOnClick():
    setMenu(Menus.MainMenu)

def playMenu_saveButtonOnClick(saveNumber : int):
    saveFile = os.path.expanduser("~\\sathevill\\save" + str(saveNumber) + ".json")
    Game.currentLevel = Level.Level(saveFile)
    Game.currentLevel.join()

# OptionsMenu
def optionsMenu_backButtonOnClick():
    setMenu(Menus.MainMenu)

# PauseMenu
def pauseMenu_continueButtonOnClick():
    Game.currentLevel.pause(False)

def pauseMenu_optionsButtonOnClick():
    setMenu(Menus.OptionsMenu)

def pauseMenu_backToMainMenuOnClick():
    Game.currentLevel.leave()

def deathMenu_backToMainMenuOnClick():
    Game.currentLevel.leave()

def deathMenu_respawnOnClick():
    Game.currentLevel.respawn()

#LevelCreatorMenu
def levelCreatorMenu_backToMainMenuOnClick():
    Game.currentLevelCreator = None
    setMenu(Menus.MainMenu)

def levelCreatorMenu_backToLevelCreatorOnClick():
    Game.currentLevelCreator.openMenu(False)

def levelCreatorMenu_saveLevelOnClick():
    root = tkinter.Tk()
    root.withdraw()
    filePath = filedialog.asksaveasfilename(filetypes=[("JSON File", ".json")], parent=root)
    Game.currentLevelCreator.saveToFile(filePath if filePath.endswith(".json") else filePath + ".json")

def levelCreatorMenu_loadLevelOnClick():
    root = tkinter.Tk()
    root.withdraw()
    filePath = filedialog.askopenfilename(filetypes=[("JSON File", ".json")], parent=root)
    Game.currentLevelCreator.loadFromFile(filePath)
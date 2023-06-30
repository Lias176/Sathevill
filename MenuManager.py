import pygame, sys, functools, Game, os, Level, Textures
from enum import Enum
from Button import Button
from LevelCreator import LevelCreator
from UIElement import UIElement
from TextBox import TextBox
from Point import Point
from InputBox import InputBox

class Menus(Enum):
    MainMenu = 0,
    OptionsMenu = 1,
    PlayMenu = 2,
    PauseMenu = 3,
    DeathMenu = 4,
    LevelCreatorMenu = 5
    GAME_COMPLETE = 6

uiElements: list[UIElement] = []
currentMenu = None

def keyPressed(key : int):
    match key:
        case pygame.K_ESCAPE:
            match(currentMenu):
                case Menus.PauseMenu:
                    Game.currentLevel.openPauseMenu(False)
                case Menus.LevelCreatorMenu:
                    Game.currentLevelCreator.openMenu(False)
                
def render(screen: pygame.Surface):
    Textures.MENU_BG.render(screen)
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
                TextBox("Sathevill", Point(0, 300), font = pygame.font.Font("fonts\\Roboto-Bold.ttf", 150), fontColor = pygame.Color(255, 255, 255, 135)),
                Button("Play", pygame.Rect(0, 30, 400, 50), playMenu_saveButtonOnClick),
                Button("Quit", pygame.Rect(0, -30, 400, 50), mainMenu_quitButtonOnClick)
            ]
        case Menus.PauseMenu:
            uiElements = [
                Button("Continue", pygame.Rect(0, 30, 400, 50), pauseMenu_continueButtonOnClick),
                Button("Back to Main Menu", pygame.Rect(0, -30, 400, 50), pauseMenu_backToMainMenuOnClick)
            ]
        case Menus.DeathMenu:
            uiElements = [
                TextBox("Du bist gestorben!", Point(0, 115), font = pygame.font.Font("fonts\\Roboto-Bold.ttf", 60)),
                Button("Respawn", pygame.Rect(0, 30, 400, 50), playMenu_saveButtonOnClick),
                Button("Back to Main Menu", pygame.Rect(0, -30, 400, 50), deathMenu_backToMainMenuOnClick)
            ]
        case Menus.LevelCreatorMenu:
            uiElements = [
                Button("Back to LevelCreator", pygame.Rect(0, 90, 400, 50), levelCreatorMenu_backToLevelCreatorOnClick),
                Button("Load Level", pygame.Rect(0, 30, 400, 50), levelCreatorMenu_loadLevelOnClick),
                Button("Save Level", pygame.Rect(0, -30, 400, 50), levelCreatorMenu_saveLevelOnClick),
                Button("Back to Main Menu", pygame.Rect(0, -90, 400, 50), levelCreatorMenu_backToMainMenuOnClick)
            ]
        case Menus.GAME_COMPLETE:
            uiElements = [
                TextBox("Gewonnen", Point(0, 0), font = pygame.font.Font("fonts\\Roboto-Bold.ttf", 100))
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

def playMenu_saveButtonOnClick():
    saveFile = os.path.expanduser("~\\sathevill\\save.json")
    Game.currentLevel = Level.Level(saveFile)
    Game.currentLevel.join()

# OptionsMenu
def optionsMenu_backButtonOnClick():
    setMenu(Menus.MainMenu)

# PauseMenu
def pauseMenu_continueButtonOnClick():
    Game.currentLevel.openPauseMenu(False)

def pauseMenu_optionsButtonOnClick():
    setMenu(Menus.OptionsMenu)

def pauseMenu_backToMainMenuOnClick():
    Game.currentLevel.leave()

def deathMenu_backToMainMenuOnClick():
    Game.currentLevel.leave()

#LevelCreatorMenu
def levelCreatorMenu_backToMainMenuOnClick():
    for uiElement in Game.currentLevelCreator.configUI:
            if(type(uiElement) == InputBox):
                uiElement.remove()
    Game.currentLevelCreator = None
    setMenu(Menus.MainMenu)

def levelCreatorMenu_backToLevelCreatorOnClick():
    Game.currentLevelCreator.openMenu(False)

def levelCreatorMenu_saveLevelOnClick():
    # root = tkinter.Tk()
    # root.withdraw()
    # filePath = filedialog.asksaveasfilename(filetypes=[("JSON File", ".json")], parent=root)
    # Game.currentLevelCreator.saveToFile(filePath if filePath.endswith(".json") else filePath + ".json")
    pass

def levelCreatorMenu_loadLevelOnClick():
    # root = tkinter.Tk()
    # root.withdraw()
    # filePath = filedialog.askopenfilename(filetypes=[("JSON File", ".json")], parent=root)
    # Game.currentLevelCreator.loadFromFile(filePath)
    pass
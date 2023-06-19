import pygame, sys, functools, Game, os, tkinter, Level
from enum import Enum
from tkinter import filedialog
from Button import Button
from Button import PositionOffset
from LevelCreator import LevelCreator

class Menus(Enum):
    MainMenu = 0,
    OptionsMenu = 1,
    PlayMenu = 2,
    PauseMenu = 3,
    DeathMenu = 4,
    LevelCreatorMenu = 5

buttons : list[Button] = []
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
    for button in buttons:
        button.render(screen)

def setMenu(menu):
    global currentMenu, buttons
    currentMenu = menu
    if(len(buttons) > 0):
        for button in buttons:
            button.remove()
        buttons = []
    
    match menu:
        case Menus.MainMenu:
            buttons = [
                Button("Play", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, 90, 400, 50), PositionOffset.CENTER_SCREEN, mainMenu_playButtonOnClick),
                Button("Options", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, 30, 400, 50), PositionOffset.CENTER_SCREEN, mainMenu_optionsButtonOnClick),
                Button("Level creator", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, -30, 400, 50), PositionOffset.CENTER_SCREEN, mainMenu_levelCreatorButtonOnClick),
                Button("Quit", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, -90, 400, 50), PositionOffset.CENTER_SCREEN, mainMenu_quitButtonOnClick)
            ]
        case Menus.OptionsMenu:
            buttons = [
                Button("Back", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, 0, 400, 50), PositionOffset.CENTER_SCREEN, optionsMenu_backButtonOnClick)
            ]
        case Menus.PlayMenu:
            buttons = [
                Button("Back", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, 150, 400, 50), PositionOffset.CENTER_SCREEN, playMenu_backButtonOnClick),
                Button("Save 1", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, 90, 400, 50), PositionOffset.CENTER_SCREEN, functools.partial(playMenu_saveButtonOnClick, 1)),
                Button("Save 2", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, 30, 400, 50), PositionOffset.CENTER_SCREEN, functools.partial(playMenu_saveButtonOnClick, 2)),
                Button("Save 3", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, -30, 400, 50), PositionOffset.CENTER_SCREEN, functools.partial(playMenu_saveButtonOnClick, 3)),
                Button("Save 4", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, -90, 400, 50), PositionOffset.CENTER_SCREEN, functools.partial(playMenu_saveButtonOnClick, 4)),
                Button("Save 5", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, -150, 400, 50), PositionOffset.CENTER_SCREEN, functools.partial(playMenu_saveButtonOnClick, 5))
            ]
        case Menus.PauseMenu:
            buttons = [
                Button("Continue", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, 30, 400, 50), PositionOffset.CENTER_SCREEN, pauseMenu_continueButtonOnClick),
                Button("Back to Main Menu", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, -30, 400, 50), PositionOffset.CENTER_SCREEN, pauseMenu_backToMainMenuOnClick)
            ]
        case Menus.DeathMenu:
            buttons = [
                Button("Respawn", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, 30, 400, 50), PositionOffset.CENTER_SCREEN, deathMenu_respawnOnClick),
                Button("Back to Main Menu", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, -30, 400, 50), PositionOffset.CENTER_SCREEN, deathMenu_backToMainMenuOnClick)
            ]
        case Menus.LevelCreatorMenu:
            buttons = [
                Button("Back to LevelCreator", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, 90, 400, 50), PositionOffset.CENTER_SCREEN, levelCreatorMenu_backToLevelCreatorOnClick),
                Button("Load Level", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, 30, 400, 50), PositionOffset.CENTER_SCREEN, levelCreatorMenu_loadLevelOnClick),
                Button("Save Level", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, -30, 400, 50), PositionOffset.CENTER_SCREEN, levelCreatorMenu_saveLevelOnClick),
                Button("Back to Main Menu", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, -90, 400, 50), PositionOffset.CENTER_SCREEN, levelCreatorMenu_backToMainMenuOnClick)
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
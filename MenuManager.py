import pygame, Button, sys, functools, Game, os, LevelCreator, tkinter, Level
from enum import Enum
from tkinter import filedialog

class Menus(Enum):
    MainMenu = 0,
    OptionsMenu = 1,
    PlayMenu = 2,
    PauseMenu = 3,
    DeathMenu = 4,
    LevelCreatorMenu = 5

screen = None
buttons = []
currentMenu = None

def init(initScreen : pygame.Surface):
    global screen
    screen = initScreen

def keyPressed(key : int):
    match key:
        case pygame.K_ESCAPE:
            match(currentMenu):
                case Menus.PauseMenu:
                    Level.pause(False)
                case Menus.LevelCreatorMenu:
                    LevelCreator.openMenu(False)
                
def getGameElements():
    finalGameElements = []
    for button in buttons:
        finalGameElements.append(button.bgGameElement)
        finalGameElements.append(button.fontGameElement)
    return finalGameElements

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
                Button.Button("Play", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, 90, 400, 50), Button.PositionOffset.CenterScreen, mainMenu_playButtonOnClick),
                Button.Button("Options", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, 30, 400, 50), Button.PositionOffset.CenterScreen, mainMenu_optionsButtonOnClick),
                Button.Button("Level creator", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, -30, 400, 50), Button.PositionOffset.CenterScreen, mainMenu_levelCreatorButtonOnClick),
                Button.Button("Quit", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, -90, 400, 50), Button.PositionOffset.CenterScreen, mainMenu_quitButtonOnClick)
            ]
        case Menus.OptionsMenu:
            buttons = [
                Button.Button("Back", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, 0, 400, 50), Button.PositionOffset.CenterScreen, optionsMenu_backButtonOnClick)
            ]
        case Menus.PlayMenu:
            buttons = [
                Button.Button("Back", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, 150, 400, 50), Button.PositionOffset.CenterScreen, playMenu_backButtonOnClick),
                Button.Button("Save 1", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, 90, 400, 50), Button.PositionOffset.CenterScreen, functools.partial(playMenu_saveButtonOnClick, 1)),
                Button.Button("Save 2", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, 30, 400, 50), Button.PositionOffset.CenterScreen, functools.partial(playMenu_saveButtonOnClick, 2)),
                Button.Button("Save 3", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, -30, 400, 50), Button.PositionOffset.CenterScreen, functools.partial(playMenu_saveButtonOnClick, 3)),
                Button.Button("Save 4", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, -90, 400, 50), Button.PositionOffset.CenterScreen, functools.partial(playMenu_saveButtonOnClick, 4)),
                Button.Button("Save 5", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, -150, 400, 50), Button.PositionOffset.CenterScreen, functools.partial(playMenu_saveButtonOnClick, 5))
            ]
        case Menus.PauseMenu:
            buttons = [
                Button.Button("Continue", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, 30, 400, 50), Button.PositionOffset.CenterScreen, pauseMenu_continueButtonOnClick),
                Button.Button("Back to Main Menu", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, -30, 400, 50), Button.PositionOffset.CenterScreen, pauseMenu_backToMainMenuOnClick)
            ]
        case Menus.DeathMenu:
            buttons = [
                Button.Button("Respawn", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, 30, 400, 50), Button.PositionOffset.CenterScreen, deathMenu_respawnOnClick),
                Button.Button("Back to Main Menu", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, -30, 400, 50), Button.PositionOffset.CenterScreen, deathMenu_backToMainMenuOnClick)
            ]
        case Menus.LevelCreatorMenu:
            buttons = [
                Button.Button("Back to LevelCreator", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, 90, 400, 50), Button.PositionOffset.CenterScreen, levelCreatorMenu_backToLevelCreatorOnClick),
                Button.Button("Load Level", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, 30, 400, 50), Button.PositionOffset.CenterScreen, levelCreatorMenu_loadLevelOnClick),
                Button.Button("Save Level", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, -30, 400, 50), Button.PositionOffset.CenterScreen, levelCreatorMenu_saveLevelOnClick),
                Button.Button("Back to Main Menu", pygame.font.SysFont("Arial", 30, True), pygame.Color(15, 15, 15), pygame.Color(194, 194, 194), pygame.Rect(0, -90, 400, 50), Button.PositionOffset.CenterScreen, levelCreatorMenu_backToMainMenuOnClick)
            ]

# MainMenu
def mainMenu_playButtonOnClick():
    setMenu(Menus.PlayMenu)

def mainMenu_optionsButtonOnClick():
    setMenu(Menus.OptionsMenu)

def mainMenu_levelCreatorButtonOnClick():
    LevelCreator.openLevelEditor()

def mainMenu_quitButtonOnClick():
    sys.exit()

# PlayMenu
def playMenu_backButtonOnClick():
    setMenu(Menus.MainMenu)

def playMenu_saveButtonOnClick(saveNumber : int):
    saveFile = os.path.expanduser("~\\sathevill\\save" + str(saveNumber) + ".json")
    Level.loadSave(saveFile)

# OptionsMenu
def optionsMenu_backButtonOnClick():
    setMenu(Menus.MainMenu)

# PauseMenu
def pauseMenu_continueButtonOnClick():
    Level.pause(False)

def pauseMenu_optionsButtonOnClick():
    setMenu(Menus.OptionsMenu)

def pauseMenu_backToMainMenuOnClick():
    Level.leaveGame()

def deathMenu_backToMainMenuOnClick():
    Level.leaveGame()

def deathMenu_respawnOnClick():
    Level.respawn()

#LevelCreatorMenu
def levelCreatorMenu_backToMainMenuOnClick():
    LevelCreator.leaveLevelCreator()

def levelCreatorMenu_backToLevelCreatorOnClick():
    LevelCreator.openMenu(False)

def levelCreatorMenu_saveLevelOnClick():
    root = tkinter.Tk()
    root.withdraw()
    filePath = filedialog.asksaveasfilename(filetypes=[("JSON File", ".json")], parent=root)
    LevelCreator.saveToFile(filePath if filePath.endswith(".json") else filePath + ".json")

def levelCreatorMenu_loadLevelOnClick():
    root = tkinter.Tk()
    root.withdraw()
    filePath = filedialog.askopenfilename(filetypes=[("JSON File", ".json")], parent=root)
    LevelCreator.loadFile(filePath)
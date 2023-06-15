import MenuManager, Button, pygame
from Point import Point
from Level import Level
from enum import Enum
from LevelCreator import LevelCreator

class GameState(Enum):
    IN_LEVEL = 0
    IN_MENU = 1
    IN_LEVEL_CREATOR = 2

state: GameState = GameState.IN_MENU
currentLevel: Level = None
screen: pygame.Surface = None
currentLevelCreator: LevelCreator = None

def init(initScreen : pygame.Surface):
    global screen
    screen = initScreen

def mouseClicked(button: int, pos: Point):
    match state:
        case GameState.IN_LEVEL_CREATOR:
            currentLevelCreator.mousePressed(button, pos)
    Button.mouseClicked(button, pos)

def update(time: int):
    match state:
        case GameState.IN_LEVEL:
            currentLevel.update(time)
        case GameState.IN_LEVEL_CREATOR:
            currentLevelCreator.update()

def render(screen: pygame.Surface):
    screen.fill("black")
    match state:
        case GameState.IN_LEVEL:
            currentLevel.render(screen)
        case GameState.IN_LEVEL_CREATOR:
            currentLevelCreator.render(screen)
        case GameState.IN_MENU:
            MenuManager.render(screen)

def keyPressed(key: int):
    match state:
        case GameState.IN_LEVEL:
            currentLevel.keyPressed(key)
        case GameState.IN_LEVEL_CREATOR:
            currentLevelCreator.keyPressed(key)
        case GameState.IN_MENU:
            MenuManager.keyPressed(key)

def mouseWheel(y: int):
    match state:
        case GameState.IN_LEVEL_CREATOR:
            currentLevelCreator.mouseWheel(y)
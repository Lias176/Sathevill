import MenuManager, LevelCreator, Button, pygame
from Point import Point
from Level import Level
from enum import Enum

class GameState(Enum):
    IN_LEVEL = 0
    IN_MENU = 1
    IN_LEVEL_CREATOR = 2

state: GameState = GameState.IN_MENU
currentLevel: Level = None
screen: pygame.Surface = None

def init(initScreen : pygame.Surface):
    global screen
    screen = initScreen

def mouseClicked(button: int, pos: Point):
    match state:
        case GameState.IN_LEVEL_CREATOR:
            LevelCreator.mouseClicked(button)
    Button.mouseClicked(button, pos)

def update(time: int):
    match state:
        case GameState.IN_LEVEL:
            currentLevel.update(time)
        case GameState.IN_LEVEL_CREATOR:
            LevelCreator.update()

def render(screen: pygame.Surface):
    screen.fill("black")
    match state:
        case GameState.IN_LEVEL:
            currentLevel.render(screen)
        case GameState.IN_LEVEL_CREATOR:
            LevelCreator.render(screen)
        case GameState.IN_MENU:
            MenuManager.render(screen)

def keyPressed(key: int):
    match state:
        case GameState.IN_LEVEL:
            currentLevel.keyPressed(key)
        case GameState.IN_LEVEL_CREATOR:
            LevelCreator.keyPressed(key)
        case GameState.IN_MENU:
            MenuManager.keyPressed(key)

def mouseWheel(y: int):
    match state:
        case GameState.IN_LEVEL_CREATOR:
            LevelCreator.mouseWheel(y)
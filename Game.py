import MenuManager, Button, pygame
from Point import Point
from Level import Level
from enum import Enum
from LevelCreator import LevelCreator
from Animation import Animation
from LevelObject import LevelObject
from Entity import Entity
from Timer import Timer
from InputBox import InputBox

class GameState(Enum):
    IN_LEVEL = 0
    IN_MENU = 1
    IN_LEVEL_CREATOR = 2

state: GameState = GameState.IN_MENU
currentLevel: Level = None
screen: pygame.Surface = None
currentLevelCreator: LevelCreator = None

def init(initScreen: pygame.Surface):
    global screen
    screen = initScreen
    for subclass in LevelObject.__subclasses__():
        LevelObject.idClasses[subclass.id] = subclass
    for subclass in Entity.__subclasses__():
        LevelObject.idClasses[subclass.id] = subclass

def mouseClicked(button: int, pos: Point):
    match state:
        case GameState.IN_LEVEL_CREATOR:
            currentLevelCreator.mousePressed(button, pos)
        case GameState.IN_LEVEL:
            currentLevel.mousePressed(button, pos)
    Button.mouseClicked(button, pos)
    InputBox.onClick(button, pos)

def mouseUp(button: int):
    match state:
        case GameState.IN_LEVEL_CREATOR:
            currentLevelCreator.mouseUp(button)

def update(time: int):
    match state:
        case GameState.IN_LEVEL:
            currentLevel.update(time)
        case GameState.IN_LEVEL_CREATOR:
            currentLevelCreator.update()
    if(state != GameState.IN_LEVEL or currentLevel.isPaused == False):
        for animation in Animation.animations:
            animation.update(time)
    for timer in Timer.timers:
        timer.update(time)

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
            InputBox.onKey(key)
        case GameState.IN_MENU:
            MenuManager.keyPressed(key)

def mouseWheel(y: int):
    match state:
        case GameState.IN_LEVEL_CREATOR:
            currentLevelCreator.mouseWheel(y)

def mouseMotion(pos: Point):
    Button.mouseMotion(pos)
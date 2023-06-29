import MenuManager, Button, pygame, math, Textures
from Point import Point
from Level import Level
from enum import Enum
from LevelCreator import LevelCreator
from Animation import Animation
from LevelObject import LevelObject
from Entity import Entity
from Timer import Timer
from InputBox import InputBox
from Enemy import Enemy
from GameObject import GameObject
from threading import Thread

class GameState(Enum):
    IN_LEVEL = 0
    IN_MENU = 1
    IN_LEVEL_CREATOR = 2

state: GameState = GameState.IN_MENU
currentLevel: Level = None
screen: pygame.Surface = None
currentLevelCreator: LevelCreator = None

def loadNightOverlay():
        Textures.NIGHT_OVERLAY = GameObject(pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA).convert_alpha(), Point(0, 0))
        screenMidX: int = screen.get_width() / 2
        screenMidY: int = screen.get_height() / 2
        for y in range(Textures.NIGHT_OVERLAY.surface.get_height()):
            for x in range(Textures.NIGHT_OVERLAY.surface.get_width()):
                Textures.NIGHT_OVERLAY.surface.set_at((x, y), pygame.Color(0, 0, 0, min(math.floor(math.sqrt((x - screenMidX) ** 2 + (y - screenMidY) ** 2) / 1.75), 255)))

def init(initScreen: pygame.Surface):
    global screen
    screen = initScreen
    for subclass in LevelObject.__subclasses__():
        LevelObject.idClasses[subclass.id] = subclass
    for subclass in Entity.__subclasses__():
        LevelObject.idClasses[subclass.id] = subclass
    for subclass in Enemy.__subclasses__():
        LevelObject.idClasses[subclass.id] = subclass
    thread: Thread = Thread(target = loadNightOverlay)
    thread.start()

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
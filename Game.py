import Level, MenuManager, LevelCreator, Button, pygame

inGame = False
currentLevel : Level.Level = None
inLevelEditor = False
screen : pygame.Surface = None

def init(initScreen : pygame.Surface):
    global screen
    screen = initScreen

def mouseClicked(button : int):
    if(inLevelEditor):
        LevelCreator.mouseClicked(button)
    Button.mouseClicked(button)

def update(time : int):
    if(inGame):
        currentLevel.update(time)
    elif(inLevelEditor):
        LevelCreator.update()

def getGameElements():
    if(inGame and currentLevel != None):
        return currentLevel.getGameElements()
    elif(inLevelEditor):
        return LevelCreator.getGameElements()
    else:
        return MenuManager.getGameElements()

def keyPressed(key : int):
    if(inGame and currentLevel != None):
        currentLevel.keyPressed(key)
    elif(inLevelEditor):
        LevelCreator.keyPressed(key)
    else:
        MenuManager.keyPressed(key)

def mouseWheel(y : int):
    if(inLevelEditor):
        LevelCreator.mouseWheel(y)
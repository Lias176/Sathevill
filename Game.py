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

def render(screen : pygame.Surface):
    screen.fill("black")
    if(inGame and currentLevel != None):
        currentLevel.render(screen)
    elif(inLevelEditor):
        LevelCreator.render(screen)
    else:
        MenuManager.render(screen)

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
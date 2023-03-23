import Level, MenuManager, LevelCreator, Button

inGame = False
inLevelEditor = False

def mouseClicked(button : int):
    if(inLevelEditor):
        LevelCreator.mouseClicked(button)
    Button.mouseClicked(button)

def update(time : int):
    if(inGame):
        Level.update(time)
    elif(inLevelEditor):
        LevelCreator.update()

def getGameElements():
    if(inGame):
        return Level.getGameElements()
    elif(inLevelEditor):
        return LevelCreator.getGameElements()
    else:
        return MenuManager.getGameElements()

def keyPressed(key : int):
    if(inGame):
        Level.keyPressed(key)
    elif(inLevelEditor):
        LevelCreator.keyPressed(key)
    else:
        MenuManager.keyPressed(key)

def mouseWheel(y : int):
    if(inLevelEditor):
        LevelCreator.mouseWheel(y)
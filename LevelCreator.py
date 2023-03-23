import pygame, GameElement, json, math, Game, MenuManager, LevelObject

screen = None
levelObjects = []
ui = []
selectableObjects = []
selectedObject = None
selectObjectBgPanel = None
camera = (0, 0)
rightDownMousePos = (0, 0)
rightDownCamPos = (0, 0)

def init(initScreen : pygame.Surface):
    global screen
    screen = initScreen

def openLevelEditor():
    global sprites, ui, selectObjectBgPanel
    sprites = pygame.sprite.Group()
    ui = []
    selectObjectBgPanel = GameElement.GameElement(pygame.Surface((screen.get_width() / 5, screen.get_height())), (0, 0))
    selectObjectBgPanel.surface.fill((40, 40, 40))
    selectObjectBgPanel.surface.set_alpha(200)
    ui.append(selectObjectBgPanel)
    defaultObjectsFile = open("defaultObjects.json")
    defaultObjects = json.loads(defaultObjectsFile.read())
    curY = 50
    for i, obj in enumerate(defaultObjects):
        image = pygame.image.load(obj["image"]).convert()
        selectableObjects.append(LevelObject.LevelObject(GameElement.GameElement(image, (selectObjectBgPanel.surface.get_width() / 2 - image.get_width() / 2, curY)), obj["value"]))
        ui.append(selectableObjects[i].gameElement)
        curY += image.get_height() + 50

def leaveLevelCreator():
    global levelObjects, ui, selectableObjects, selectedObject, selectObjectBgPanel, camera, rightDownCamPos, rightDownMousePos
    levelObjects = []
    ui = []
    selectableObjects = []
    selectedObject = None
    selectObjectBgPanel = None
    camera = (0, 0)
    rightDownCamPos = (0, 0)
    rightDownMousePos = (0, 0)
    Game.inLevelEditor = False
    MenuManager.setMenu(MenuManager.Menus.MainMenu)

def getLevelObjects() -> list[GameElement.GameElement]:
    offsetLevelObjects = []
    for levelObject in levelObjects:
        offsetLevelObjects.append(GameElement.GameElement(levelObject.gameElement.surface, (levelObject.gameElement.pos[0] - camera[0], levelObject.gameElement.pos[1] - camera[1])))
    return offsetLevelObjects

def blockFromPoint(point: tuple) -> tuple:
    return(math.floor(point[0] / 50), math.floor(point[1] / 50))

def pointFromBlock(block: tuple) -> tuple:
    return(block[0] * 50, block[1] * 50)

def update():
    mouse = pygame.mouse.get_pressed(3)
    if(mouse[0]):
        leftDown()
    elif(mouse[2]):
        rightDown()

def keyPressed(key : int):
    match(key):
        case pygame.K_ESCAPE:
            openMenu(True)

def mouseClicked(button : int):
    global selectedObject, selectObjectBgPanel, rightDownMousePos, rightDownCamPos
    mousePos = pygame.mouse.get_pos()
    if(button == 1):
        if(selectObjectBgPanel.surface.get_rect().collidepoint(mousePos)):
            for selectableObj in selectableObjects:
                rect = pygame.Rect(selectableObj.gameElement.pos, (selectableObj.gameElement.surface.get_width(), selectableObj.gameElement.surface.get_height()))
                if(rect.collidepoint(mousePos)):
                    selectedObject = selectableObj
    elif(button == 3):
        rightDownMousePos = mousePos
        rightDownCamPos = camera

def leftDown():
    mousePos = pygame.mouse.get_pos()
    worldMousePos = (mousePos[0] + camera[0], mousePos[1] + camera[1])
    if(selectObjectBgPanel.surface.get_rect().collidepoint(mousePos) == False and selectedObject != None):
        for levelObject in levelObjects:
            if(blockFromPoint(levelObject.gameElement.pos) == blockFromPoint(worldMousePos)):
                if(levelObject.gameElement.surface == selectedObject.gameElement.surface):
                    return
                else:
                    levelObjects.remove(levelObject)
        levelObjects.append(LevelObject.LevelObject(GameElement.GameElement(selectedObject.gameElement.surface, pointFromBlock(blockFromPoint(worldMousePos))), selectedObject.value))

def rightDown():
    global camera
    mousePos = pygame.mouse.get_pos()
    camera = (rightDownCamPos[0] + rightDownMousePos[0] - mousePos[0], rightDownCamPos[1] + rightDownMousePos[1] - mousePos[1])

def openMenu(open : bool):
    if(open):
        Game.inLevelEditor = False
        MenuManager.setMenu(MenuManager.Menus.LevelCreatorMenu)
    else:
        Game.inLevelEditor = True
        MenuManager.setMenu(None)

def saveToFile(path : str):
    levelFile = open(path, "w")
    level = []
    for levelObject in levelObjects:
        level.append((levelObject.value, blockFromPoint(levelObject.gameElement.pos)))
    json.dump(level, levelFile)
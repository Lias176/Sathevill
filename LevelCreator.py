import pygame, json, math, Game, MenuManager, LevelObject, LevelObjects.SchokoDrink, LevelObjects.Palm, LevelObjects.Tree, LevelObjects.Grass, LevelObjects.House, LevelObjects.MonsterBaseEntry, LevelObjects.House2
from GameElement import GameElement

removeObject = None
levelObjects = []
ui = []
selectableObjects = []
selectedObject = None
selectObjectBgPanel = None
camera = (0, 0)
rightDownMousePos = (0, 0)
rightDownCamPos = (0, 0)
selectObjectScrollOffset = 0
selectObjectPanelHeight = 0

def openLevelEditor():
    global levelObjects, ui, selectObjectBgPanel, removeObject, selectObjectPanelHeight
    Game.inLevelEditor = True
    MenuManager.setMenu(None)
    ui = []
    levelObjects = []
    selectObjectBgPanel = GameElement(pygame.Surface((Game.screen.get_width() / 5, Game.screen.get_height())), (0, 0))
    selectObjectBgPanel.surface.fill((40, 40, 40))
    selectObjectBgPanel.surface.set_alpha(200)
    ui.append(selectObjectBgPanel)
    curY = 50
    for obj in LevelObject.LevelObject.__subclasses__():
        object = obj((0, 0))
        object.pos = (selectObjectBgPanel.surface.get_width() / 2 - object.surface.get_width() / 2, curY)
        selectableObjects.append(object)
        curY += object.surface.get_height() + 50
    removeImage = pygame.image.load("images\\remove.png")
    removeObject = GameElement(removeImage, (selectObjectBgPanel.surface.get_width() / 2 - removeImage.get_width() / 2, curY))
    curY += removeObject.surface.get_height() + 50
    selectObjectPanelHeight = curY
    selectableObjects.append(removeObject)

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

def render(screen : pygame.Surface):
    for levelObject in levelObjects:
        screen.blit(levelObject.surface, (levelObject.pos[0] - camera[0], levelObject.pos[1] - camera[1]))
    for uiElement in ui:
        screen.blit(uiElement.surface, uiElement.pos)
    for selectableObject in selectableObjects:
        screen.blit(selectableObject.surface, (selectableObject.pos[0], selectableObject.pos[1] + selectObjectScrollOffset))

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
                rect = pygame.Rect((selectableObj.pos[0], selectableObj.pos[1] + selectObjectScrollOffset), (selectableObj.surface.get_width(), selectableObj.surface.get_height()))
                if(rect.collidepoint(mousePos)):
                    selectedObject = selectableObj
    elif(button == 3):
        rightDownMousePos = mousePos
        rightDownCamPos = camera

def mouseWheel(y : int):
    global selectObjectScrollOffset
    mousePos = pygame.mouse.get_pos()
    if(selectObjectBgPanel.surface.get_rect().collidepoint(mousePos)):
        if(y > 0):
            selectObjectScrollOffset += 20
        else:
            selectObjectScrollOffset -= 20
        if(selectObjectScrollOffset > 0):
            selectObjectScrollOffset = 0
        elif(selectObjectScrollOffset < -selectObjectPanelHeight + selectObjectBgPanel.surface.get_height()):
            selectObjectScrollOffset = -selectObjectPanelHeight + selectObjectBgPanel.surface.get_height()

def leftDown():
    mousePos = pygame.mouse.get_pos()
    worldMousePos = (mousePos[0] + camera[0], mousePos[1] + camera[1])
    if(selectObjectBgPanel.surface.get_rect().collidepoint(mousePos) == False and selectedObject != None):
        for levelObject in levelObjects:
            if(blockFromPoint(levelObject.pos) == blockFromPoint(worldMousePos)):
                if(selectedObject.surface != removeObject.surface and levelObject.id == selectedObject.id):
                    return
                elif(selectedObject.surface == removeObject.surface or levelObject.layer == selectedObject.layer):
                    levelObjects.remove(levelObject)
        if(selectedObject.surface == removeObject.surface):
            return
        levelObjects.append(type(selectedObject)(pointFromBlock(blockFromPoint(worldMousePos))))

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
        level.append((levelObject.id, blockFromPoint(levelObject.pos)))
    json.dump(level, levelFile)

def loadFile(file : str):
    saveFile = open(file)
    for obj in json.loads(saveFile.read()):
        levelObjects.append(LevelObject.getClassById(obj[0])((pointFromBlock(obj[1]))))
    MenuManager.setMenu(None)
    Game.inLevelEditor = True
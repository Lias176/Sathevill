import pygame, json, math, Game, MenuManager, LevelObject, LevelObjects.SchokoDrink, LevelObjects.Palm, LevelObjects.Tree, LevelObjects.Grass, LevelObjects.House, LevelObjects.MonsterBaseEntry, LevelObjects.House2
from GameObject import GameObject
from Point import Point

removeTool: GameObject = None
levelObjects = []
selectableObjects = []
selectedObject = None
selectObjectBgPanel = None
camera = (0, 0)
rightDownMousePos = (0, 0)
rightDownCamPos = (0, 0)
selectObjectScrollOffset = 0
selectObjectPanelHeight = 0

def openLevelEditor():
    global levelObjects, selectObjectBgPanel, removeTool, selectObjectPanelHeight
    Game.state = Game.GameState.IN_LEVEL_CREATOR
    MenuManager.setMenu(None)
    levelObjects = []
    selectObjectBgPanel = GameObject(pygame.Surface((Game.screen.get_width() / 5, Game.screen.get_height())), Point(0, 0))
    selectObjectBgPanel.surface.fill((40, 40, 40))
    selectObjectBgPanel.surface.set_alpha(200)
    curY = 50
    for obj in LevelObject.LevelObject.__subclasses__():
        object = obj((0, 0))
        object.pos = Point(selectObjectBgPanel.surface.get_width() / 2 - object.surface.get_width() / 2, curY)
        selectableObjects.append(object)
        curY += object.surface.get_height() + 50
    removeImage = pygame.image.load("images\\remove.png")
    removeTool = GameObject(removeImage, Point(selectObjectBgPanel.surface.get_width() / 2 - removeImage.get_width() / 2, curY))
    curY += removeTool.surface.get_height() + 50
    selectObjectPanelHeight = curY
    selectableObjects.append(removeTool)

def leaveLevelCreator():
    global levelObjects, selectableObjects, selectedObject, selectObjectBgPanel, camera, rightDownCamPos, rightDownMousePos
    levelObjects = []
    selectableObjects = []
    selectedObject = None
    selectObjectBgPanel = None
    camera = (0, 0)
    rightDownCamPos = (0, 0)
    rightDownMousePos = (0, 0)
    Game.state = Game.GameState.IN_MENU
    MenuManager.setMenu(MenuManager.Menus.MainMenu)

def render(screen : pygame.Surface):
    for levelObject in levelObjects:
        screen.blit(levelObject.surface, (levelObject.pos.x - camera[0], levelObject.pos.y - camera[1]))
    screen.blit(selectObjectBgPanel.surface, selectObjectBgPanel.pos.asTuple())
    for selectableObject in selectableObjects:
        screen.blit(selectableObject.surface, (selectableObject.pos.x, selectableObject.pos.y + selectObjectScrollOffset))

def blockFromPoint(point: Point) -> Point:
    return Point(math.floor(point.x / 50), math.floor(point.y / 50))

def pointFromBlock(block: Point) -> Point:
    return Point(block.x * 50, block.y * 50)

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
                rect = pygame.Rect((selectableObj.pos.x, selectableObj.pos.y + selectObjectScrollOffset), (selectableObj.surface.get_width(), selectableObj.surface.get_height()))
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
    worldMousePos: Point = Point(mousePos[0] + camera[0], mousePos[1] + camera[1])
    if(selectObjectBgPanel.surface.get_rect().collidepoint(mousePos) == False and selectedObject != None):
        for levelObject in levelObjects:
            if(blockFromPoint(levelObject.pos) == blockFromPoint(worldMousePos)):
                if(selectedObject.surface != removeTool.surface and levelObject.id == selectedObject.id):
                    return
                elif(selectedObject.surface == removeTool.surface or levelObject.layer == selectedObject.layer):
                    levelObjects.remove(levelObject)
        if(selectedObject.surface == removeTool.surface):
            return
        levelObjects.append(type(selectedObject)(pointFromBlock(blockFromPoint(worldMousePos))))

def rightDown():
    global camera
    mousePos = pygame.mouse.get_pos()
    camera = (rightDownCamPos[0] + rightDownMousePos[0] - mousePos[0], rightDownCamPos[1] + rightDownMousePos[1] - mousePos[1])

def openMenu(open : bool):
    if(open):
        Game.state = Game.GameState.IN_MENU
        MenuManager.setMenu(MenuManager.Menus.LevelCreatorMenu)
    else:
        Game.state = Game.GameState.IN_LEVEL_CREATOR
        MenuManager.setMenu(None)

def saveToFile(path : str):
    levelFile = open(path, "w")
    level = []
    for levelObject in levelObjects:
        level.append((levelObject.id, blockFromPoint(levelObject.pos).asTuple()))
    json.dump(level, levelFile)

def loadFile(file : str):
    global levelObjects
    saveFile = open(file)
    levelObjects = []
    for obj in json.loads(saveFile.read()):
        levelObjects.append(LevelObject.getClassById(obj[0])(pointFromBlock(Point.fromTuple(obj[1]))))
    MenuManager.setMenu(None)
    Game.state = Game.GameState.IN_LEVEL_CREATOR
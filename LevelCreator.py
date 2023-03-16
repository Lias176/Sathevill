import pygame, UIElement, json

screen = None
levelObjects = []
ui = []
selectableObjects = []
selectedObject = None
selectObjectBgPanel = None

def init(initScreen : pygame.Surface):
    global screen
    screen = initScreen

def openLevelEditor(file : str):
    global sprites, ui, selectObjectBgPanel
    sprites = pygame.sprite.Group()
    ui = []
    selectObjectBgPanel = UIElement.UIElement(pygame.Surface((screen.get_width() / 5, screen.get_height())), (0, 0))
    selectObjectBgPanel.surface.fill((40, 40, 40))
    selectObjectBgPanel.surface.set_alpha(100)
    ui.append(selectObjectBgPanel)
    defaultObjectsFile = open("defaultObjects.json")
    defaultObjects = json.loads(defaultObjectsFile.read())
    curY = 50
    for i, obj in enumerate(defaultObjects):
        image = pygame.image.load(obj["image"]).convert()
        selectableObjects.append(UIElement.UIElement(image, (selectObjectBgPanel.surface.get_width() / 2 - image.get_width() / 2, curY)))
        ui.append(selectableObjects[i])
        curY += image.get_height() + 50

def blockFromPoint(point: tuple) -> tuple:
    return(int(point[0] / 50), int(point[1] / 50))

def pointFromBlock(block: tuple) -> tuple:
    return(block[0] * 50, block[1] * 50)

def update():
    mouse = pygame.mouse.get_pressed(3)
    if(mouse[0]):
        mouseDown()

def mouseClicked():
    global selectedObject, selectObjectBgPanel
    mousePos = pygame.mouse.get_pos()
    if(selectObjectBgPanel.surface.get_rect().collidepoint(mousePos)):
        for selectableObj in selectableObjects:
            rect = pygame.Rect(selectableObj.pos, (selectableObj.surface.get_width(), selectableObj.surface.get_height()))
            if(rect.collidepoint(mousePos)):
                selectedObject = selectableObj

def mouseDown():
    mousePos = pygame.mouse.get_pos()
    if(selectObjectBgPanel.surface.get_rect().collidepoint(mousePos) == False and selectedObject != None):
        for levelObject in levelObjects:
            rect = pygame.Rect(levelObject.pos, (levelObject.surface.get_width(), levelObject.surface.get_height()))
            if(rect.collidepoint(mousePos)):
                if(levelObject.surface == selectedObject.surface):
                    return
                else:
                    levelObjects.remove(levelObject)
        levelObjects.append(UIElement.UIElement(selectedObject.surface, pointFromBlock(blockFromPoint(mousePos))))
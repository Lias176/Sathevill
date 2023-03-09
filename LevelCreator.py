import pygame, UIElement, json

screen = None
sprites = pygame.sprite.Group()
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
        curY + image.get_height() + 50

def getSprites() -> pygame.sprite.Group:
    return sprites

def mouseClicked():
    global selectedObject, selectObjectBgPanel
    mousePos = pygame.mouse.get_pos()
    if(selectObjectBgPanel.surface.get_rect().collidepoint(mousePos)):
        for selectableObj in selectableObjects:
            rect = pygame.Rect(selectableObj.pos, (selectableObj.surface.get_width(), selectableObj.surface.get_height()))
            if(rect.collidepoint(mousePos)):
                selectedObject = selectableObj
    else:
        pass
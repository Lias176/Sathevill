import pygame, json, Game, MenuManager, collections, LevelObjects.SchokoDrink, LevelObjects.Palm, LevelObjects.Tree, LevelObjects.Grass, LevelObjects.House, LevelObjects.MonsterBaseEntry, LevelObjects.House2, CoordUtils, LevelObjects.MonsterbaseFloor, LevelObjects.WoodFloor, LevelObjects.Water, LevelObjects.House3
from GameObject import GameObject
from Point import Point
from io import TextIOWrapper
from LevelObject import LevelObject
from LevelCreatorTool import LevelCreatorTool
from LevelCreatorTool import LevelCreatorTools

class LevelCreator:
    def __init__(self):
        self.levelObjects: list[LevelObject] = []
        self.layerLevelObjects: dict[int, list[LevelObject]] = {}
        self.selectObjectBGPanel: GameObject = GameObject(pygame.Surface((Game.screen.get_width() / 8, Game.screen.get_height())), Point(0, 0))
        self.selectObjectBGPanel.surface.fill(pygame.Color(40, 40, 40))
        self.selectObjectBGPanel.surface.set_alpha(200)
        self.selectableObjects: list[LevelObject] = []
        self.rightDownMousePos: Point = Point(0, 0)
        self.rightDownCamPos: Point = Point(0, 0)
        self.cameraPos: Point = Point(0, 0)
        for levelObjectClass in LevelObject.__subclasses__():
            object: levelObjectClass = levelObjectClass(Point(0, 0))
            if(object.surface.get_width() > self.selectObjectBGPanel.surface.get_width() - 50):
                object.resize(width = self.selectObjectBGPanel.surface.get_width() - 50)
            object.pos = Point(self.selectObjectBGPanel.surface.get_width() / 2 - object.surface.get_width() / 2, 50 if len(self.selectableObjects) == 0 else self.selectableObjects[-1].pos.y + self.selectableObjects[-1].surface.get_height() + 50)
            self.selectableObjects.append(object)
        self.selectedType: type[LevelObject] = type(self.selectableObjects[0])

        self.placeTool: LevelCreatorTool = LevelCreatorTool(self.selectedType(Point(0, 0)).surface, LevelCreatorTools.PLACE)
        self.removeTool: LevelCreatorTool = LevelCreatorTool(pygame.image.load("images\\remove.png"), LevelCreatorTools.REMOVE)
        self.tools: list[LevelCreatorTool] = [ self.placeTool, self.removeTool ]
        self.selectedTool: LevelCreatorTool = self.tools[0]
        self.updateToolPanel()

    def updateToolPanel(self):
        toolBGPanelWidth = 25
        for tool in self.tools:
            tool.removeBorder()
            if(tool.surface.get_height() > tool.surface.get_width()):
                tool.resize(height = 50)
            else:
                tool.resize(width = 50)
            toolBGPanelWidth += tool.surface.get_width() + 25
        self.toolBGPanel: GameObject = GameObject(pygame.Surface((toolBGPanelWidth, 75)), Point(Game.screen.get_width() - toolBGPanelWidth, 0))
        self.toolBGPanel.surface.fill(pygame.Color(40, 40, 40))
        self.selectObjectBGPanel.surface.set_alpha(200)
        for i, tool in enumerate(self.tools):
            tool.pos = Point(self.toolBGPanel.pos.x + 25 if i == 0 else self.tools[i - 1].pos.x + self.tools[i - 1].surface.get_width() + 25, 12.5)
        self.selectedTool.addBoxBorder(pygame.Color(255, 255, 255))

    def render(self, screen: pygame.Surface):
        i: int = 0
        while True:
            if not i in self.layerLevelObjects:
                break
            for levelObject in self.layerLevelObjects[i]:
                levelObject.renderOffset(screen, self.cameraPos.reverseSign())
            i += 1
        self.selectObjectBGPanel.render(screen)
        for selectableObject in self.selectableObjects:
            selectableObject.render(screen)
        self.toolBGPanel.render(screen)
        for tool in self.tools:
            tool.render(screen)

    def update(self):
        mouse: tuple[bool, bool, bool] = pygame.mouse.get_pressed(3)
        if(mouse[0]):
            self.leftHeld()
        if(mouse[2]):
            self.rightHeld()

    def keyPressed(self, key: int):
        match(key):
            case pygame.K_ESCAPE:
                self.openMenu(True)

    def addLevelObject(self, object: LevelObject):
        self.levelObjects.append(object)
        for i in range(object.layer + 1):
            if i in self.layerLevelObjects:
                continue
            self.layerLevelObjects[i] = []
        self.layerLevelObjects[object.layer].append(object)

    def removeLevelObject(self, object: LevelObject):
        self.levelObjects.remove(object)
        self.layerLevelObjects[object.layer].remove(object)

    def mousePressed(self, button: int, pos: Point):
        if(button == 1):
            if(self.selectObjectBGPanel.collidepoint(pos)):
                for selectableObject in self.selectableObjects:
                    if(not selectableObject.collidepoint(pos)):
                        continue
                    self.selectedType = type(selectableObject)
                    self.placeTool.surface = self.selectedType(Point(0, 0)).surface
                    self.updateToolPanel()
                    break
            elif(self.toolBGPanel.collidepoint(pos)):
                for tool in self.tools:
                    if(not tool.collidepoint(pos)):
                        continue
                    self.selectedTool = tool
                    self.updateToolPanel()
                    break
        elif(button == 3):
            self.rightDownMousePos = pos
            self.rightDownCamPos = self.cameraPos
    
    def mouseWheel(self, y: int):
        mousePos: Point = Point.fromTuple(pygame.mouse.get_pos())
        if(not self.selectObjectBGPanel.collidepoint(mousePos)):
            return
        for selectableObject in self.selectableObjects:
            selectableObject.pos.y += 20 if y > 0 else -20
        if(self.selectableObjects[0].pos.y > 50):
            offset: int = 50 - self.selectableObjects[0].pos.y
            for selectableObject in self.selectableObjects:
                selectableObject.pos.y += offset
        maxOffset: int = Game.screen.get_height() - self.selectableObjects[-1].surface.get_height() - 50
        if self.selectableObjects[-1].pos.y < maxOffset:
            offset: int = maxOffset - self.selectableObjects[-1].pos.y
            for selectableObject in self.selectableObjects:
                selectableObject.pos.y += offset

    def leftHeld(self):
        mousePos: Point = Point.fromTuple(pygame.mouse.get_pos())
        worldMousePos: Point = mousePos.offset(self.cameraPos)
        if(self.selectObjectBGPanel.collidepoint(mousePos) or self.toolBGPanel.collidepoint(mousePos) or self.selectedType == None):
            return
        for levelObject in self.levelObjects:
            if(self.selectedTool.type == LevelCreatorTools.REMOVE and CoordUtils.blockFromPoint(levelObject.pos).equals(CoordUtils.blockFromPoint(worldMousePos))):
                self.removeLevelObject(levelObject)
                return
            if(type(levelObject) == self.selectedType and CoordUtils.blockFromPoint(levelObject.pos).equals(CoordUtils.blockFromPoint(worldMousePos))):
                return
            if(levelObject.layer != self.selectedType.layer or not CoordUtils.blockFromPoint(levelObject.pos).equals(CoordUtils.blockFromPoint(worldMousePos))):
                continue
            self.removeLevelObject(levelObject)
        if(self.selectedTool.type == LevelCreatorTools.REMOVE):
            return
        self.addLevelObject(self.selectedType(CoordUtils.snapToLevelGrid(worldMousePos)))

    def rightHeld(self):
        mousePos: Point = Point.fromTuple(pygame.mouse.get_pos())
        self.cameraPos = self.rightDownCamPos.offset(Point(self.rightDownMousePos.x - mousePos.x, self.rightDownMousePos.y - mousePos.y))

    def openMenu(self, open: bool):
        if(open):
            Game.state = Game.state.IN_MENU
            MenuManager.setMenu(MenuManager.Menus.LevelCreatorMenu)
        else:
            Game.state = Game.state.IN_LEVEL_CREATOR
            MenuManager.setMenu(None)

    def saveToFile(self, path: str):
        level: dict[str, list[tuple[int, int]]] = {}
        for levelObject in self.levelObjects:
            if not levelObject.id in level:
                level[levelObject.id]: list[tuple[int, int]] = []
            level[levelObject.id].append(CoordUtils.blockFromPoint(levelObject.pos).asTuple())
        levelFile: TextIOWrapper = open(path, "w")
        json.dump(level, levelFile)
        levelFile.close()

    def loadFromFile(self, path: str):
        self.levelObjects = []
        levelFile: TextIOWrapper = open(path, "r")
        level: dict[str, list[tuple[int, int]]] = json.loads(levelFile.read())
        for id in level.keys():
            objectType: type[LevelObject] = LevelObject.getClassById(id)
            for pos in level[id]:
                self.addLevelObject(objectType(CoordUtils.pointFromBlock(Point.fromTuple(pos))))
        self.openMenu(False)
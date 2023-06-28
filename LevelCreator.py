import pygame, json, Game, Textures, MenuManager, collections, LevelObjects.SchokoDrink, LevelObjects.Palm, LevelObjects.Tree, LevelObjects.Grass, LevelObjects.House, LevelObjects.MonsterBaseEntry, LevelObjects.House2, CoordUtils, LevelObjects.MonsterbaseFloor, LevelObjects.WoodFloor, LevelObjects.Water, LevelObjects.House3, LevelObjects.House4, LevelObjects.Sand, LevelObjects.Stone, Entities.Slime, Entities.NPC
from GameObject import GameObject
from Point import Point
from io import TextIOWrapper
from LevelObject import LevelObject
from LevelCreatorTool import LevelCreatorTool
from LevelCreatorTool import LevelCreatorTools
from Entity import Entity
from Entities.Player import Player
from LevelObjectProperty import PropertyTypes
from LevelObjectProperty import LevelObjectProperty
from TextBox import TextBox
from UIElement import UIElement
from Button import PositionOffset
from InputBoxList import InputBoxList

class LevelCreator:
    def __init__(self):
        self.firstMouseHold: bool = True
        self.levelObjects: list[LevelObject] = []
        self.layerLevelObjects: dict[int, list[LevelObject]] = {}
        self.selectObjectBGPanel: GameObject = GameObject(pygame.Surface((Game.screen.get_width() / 8, Game.screen.get_height())), Point(0, 0))
        self.selectObjectBGPanel.surface.fill(pygame.Color(40, 40, 40))
        self.selectObjectBGPanel.surface.set_alpha(200)
        self.selectableObjects: list[LevelObject] = []
        self.rightDownMousePos: Point = Point(0, 0)
        self.rightDownCamPos: Point = Point(0, 0)
        self.cameraPos: Point = Point(0, 0)
        classes: list[type[LevelObject]] = LevelObject.__subclasses__()
        classes.extend(Entity.__subclasses__())
        classes.remove(Player)
        for levelObjectClass in classes:
            if(levelObjectClass == Entity):
                continue
            object: levelObjectClass = levelObjectClass(Point(0, 0))
            if(object.surface.get_width() > self.selectObjectBGPanel.surface.get_width() - 50):
                object.resize(width = self.selectObjectBGPanel.surface.get_width() - 50)
            object.pos = Point(self.selectObjectBGPanel.surface.get_width() / 2 - object.surface.get_width() / 2, 50 if len(self.selectableObjects) == 0 else self.selectableObjects[-1].pos.y + self.selectableObjects[-1].surface.get_height() + 50)
            self.selectableObjects.append(object)
        self.selectedType: type[LevelObject] = type(self.selectableObjects[0])
        self.placePreviewObject: LevelObject = None
        self.updatePreviewObject()

        self.placeTool: LevelCreatorTool = LevelCreatorTool(self.selectedType(Point(0, 0)).surface, LevelCreatorTools.PLACE)
        self.removeTool: LevelCreatorTool = LevelCreatorTool(pygame.image.load("images\\remove.png"), LevelCreatorTools.REMOVE)
        self.configTool: LevelCreatorTool = LevelCreatorTool(Textures.GEAR.surface, LevelCreatorTools.CONFIG)
        self.tools: list[LevelCreatorTool] = [ self.placeTool, self.removeTool, self.configTool ]
        self.selectedTool: LevelCreatorTool = self.tools[0]
        self.updateToolPanel()

        self.configBGPanel = GameObject(pygame.Surface((Game.screen.get_width() / 6, Game.screen.get_height() - self.toolBGPanel.surface.get_height()), pygame.SRCALPHA).convert_alpha(), Point(Game.screen.get_width() - Game.screen.get_width() / 6, 0 + self.toolBGPanel.surface.get_height()))
        self.configBGPanel.surface.fill(pygame.Color(40, 40, 40, 200))
        self.renderConfigPanel: bool = False
        self.configUI: list[UIElement] = []

    def updatePreviewObject(self):
        self.placePreviewObject: LevelObject = self.selectedType(Point(0, 0))
        self.placePreviewObject.surface = self.placePreviewObject.surface.copy()
        self.placePreviewObject.surface.set_alpha(50)

    def updateToolPanel(self):
        toolBGPanelWidth = 25
        for tool in self.tools:
            tool.removeBorder()
            if(tool.surface.get_height() > tool.surface.get_width()):
                tool.resize(height = 50)
            else:
                tool.resize(width = 50)
            toolBGPanelWidth += tool.surface.get_width() + 25
        self.toolBGPanel: GameObject = GameObject(pygame.Surface((toolBGPanelWidth, 75), pygame.SRCALPHA).convert_alpha(), Point(Game.screen.get_width() - toolBGPanelWidth, 0))
        self.toolBGPanel.surface.fill(pygame.Color(40, 40, 40, 200))
        for i, tool in enumerate(self.tools):
            tool.pos = Point(self.toolBGPanel.pos.x + 25 if i == 0 else self.tools[i - 1].pos.x + self.tools[i - 1].surface.get_width() + 25, 12.5)
        self.selectedTool.addBoxBorder(pygame.Color(255, 255, 255))

    def render(self, screen: pygame.Surface):
        for i in self.layerLevelObjects:
            for levelObject in self.layerLevelObjects[i]:
                if(levelObject.isNotOnScreen(self.cameraPos.toTuple())):
                    continue
                levelObject.renderMinusOffset(screen, self.cameraPos.toTuple())
        self.selectObjectBGPanel.render(screen)
        for selectableObject in self.selectableObjects:
            if(selectableObject.isNotOnScreen((0, 0))):
                continue
            selectableObject.render(screen)
        self.toolBGPanel.render(screen)
        for tool in self.tools:
            tool.render(screen)
        if(self.canPlaceAt(Point.fromTuple(pygame.mouse.get_pos())) and self.selectedTool.type == LevelCreatorTools.PLACE):
            self.placePreviewObject.renderMinusOffset(screen, self.cameraPos.toTuple())
        if(self.renderConfigPanel):
            self.configBGPanel.render(screen)
            for uiElement in self.configUI:
                uiElement.render(screen)

    def update(self):
        mouse: tuple[bool, bool, bool] = pygame.mouse.get_pressed(3)
        if(mouse[0]):
            self.leftHeld()
        if(mouse[2]):
            self.rightHeld()
        self.placePreviewObject.pos = CoordUtils.snapToLevelGrid(Point.fromTuple(pygame.mouse.get_pos()).offset(self.cameraPos))

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
                    self.placeTool.setSurface(self.selectedType(Point(0, 0)).surface)
                    self.updateToolPanel()
                    self.updatePreviewObject()
                    break
            elif(self.toolBGPanel.collidepoint(pos)):
                for tool in self.tools:
                    if(not tool.collidepoint(pos)):
                        continue
                    self.selectedTool = tool
                    self.updateToolPanel()
                    break
            elif(self.selectedTool.type == LevelCreatorTools.CONFIG):
                for levelObject in self.levelObjects:
                    if(levelObject.properties == None or not pygame.Rect(levelObject.pos.x - self.cameraPos.x, levelObject.pos.y - self.cameraPos.y, levelObject.surface.get_width(), levelObject.surface.get_height()).collidepoint(pos.toTuple())):
                        continue
                    self.openConfigMenu(levelObject)
                    break
        elif(button == 3):
            self.rightDownMousePos = pos
            self.rightDownCamPos = self.cameraPos

    def openConfigMenu(self, levelObject: LevelObject):
        for uiElement in self.configUI:
            if(type(uiElement) == InputBoxList):
                uiElement.remove()
        self.configUI = []
        self.renderConfigPanel = True
        for property in levelObject.properties:
            titleBox: TextBox = TextBox(property.name, Point(self.configBGPanel.pos.x + 10, (self.configUI[-1].pos.y + 10) if len(self.configUI) > 0 else self.configBGPanel.pos.y + 10), offset = PositionOffset.TOP_LEFT, font = pygame.font.Font("fonts\\Roboto-Regular.ttf", 25), fontColor = pygame.Color(255, 255, 255))
            self.configUI.append(titleBox)
            match(property.type):
                case PropertyTypes.STRINGLISTLIST:
                    boxList: InputBoxList = InputBoxList(Point(self.configBGPanel.pos.x + 10, self.configUI[-1].pos.y + self.configUI[-1].height + 10), self.configBGPanel.surface.get_width() - 20, 100, property.var)
                    self.configUI.append(boxList)

    def mouseUp(self, button: int):
        if(button == 1):
            if(self.firstMouseHold):
                self.firstMouseHold = False
    
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

    def canPlaceAt(self, pos: Point) -> bool:
        return not self.selectObjectBGPanel.collidepoint(pos) and not self.toolBGPanel.collidepoint(pos)

    def leftHeld(self):
        mousePos: Point = Point.fromTuple(pygame.mouse.get_pos())
        worldMousePos: Point = mousePos.offset(self.cameraPos)
        if(not self.canPlaceAt(mousePos) or self.firstMouseHold):
            return
        if(self.selectedTool.type == LevelCreatorTools.PLACE):
            for levelObject in self.levelObjects:
                if(type(levelObject) == self.selectedType and CoordUtils.blockFromPoint(levelObject.pos).equals(CoordUtils.blockFromPoint(worldMousePos))):
                    return
                if(levelObject.layer != self.selectedType.layer or not CoordUtils.blockFromPoint(levelObject.pos).equals(CoordUtils.blockFromPoint(worldMousePos))):
                    continue
                self.removeLevelObject(levelObject)
            self.addLevelObject(self.selectedType(CoordUtils.snapToLevelGrid(worldMousePos)))
        elif(self.selectedTool.type == LevelCreatorTools.REMOVE):
            for levelObject in self.levelObjects:
                if(levelObject.collidepoint(worldMousePos) and not levelObject.isPixelTransparent(worldMousePos.offset(levelObject.pos.reverseSign()))):
                    self.removeLevelObject(levelObject)
                    break

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
        level: dict[str, list[list]] = {}
        for levelObject in self.levelObjects:
            if not levelObject.id in level:
                level[levelObject.id]: list[list] = []
            listObj = CoordUtils.blockFromPoint(levelObject.pos).toList()
            if(levelObject.properties != None):
                for property in levelObject.properties:
                    listObj.append([property.name, property.typeAsString(), property.var])
            level[levelObject.id].append(listObj)
        levelFile: TextIOWrapper = open(path, "w")
        json.dump(level, levelFile)
        levelFile.close()

    def loadFromFile(self, path: str):
        self.levelObjects = []
        self.layerLevelObjects = {}
        levelFile: TextIOWrapper = open(path, "r")
        level: dict[str, list[tuple[int, int]]] = json.loads(levelFile.read())
        for id in level.keys():
            objectType: type[LevelObject] = LevelObject.getClassById(id)
            for obj in level[id]:
                pos: Point = Point(obj[0], obj[1])
                object: LevelObject = objectType(CoordUtils.pointFromBlock(pos))
                for i in range(2, len(obj)):
                    property: LevelObjectProperty = LevelObjectProperty.fromString(obj[i][0], obj[i][1], obj[i][2])
                    index: int = i - 2
                    if(len(object.properties) < index):
                        object.properties.append(property)
                    else:
                        object.properties[index] = property
                self.addLevelObject(object)

        self.openMenu(False)
import json, MenuManager, Game, pygame, Textures, CoordUtils
from Entities.Player import Player
from Entity import Entity
from Point import Point
from io import TextIOWrapper
from LevelObject import LevelObject

class Level:
    def __init__(self, file: str):
        self.player: Player = Player(Point(0, 0))
        self.entities: list[Entity] = []
        self.layerEntities: dict[int, list[Entity]] = { 0: [], 1: [] }
        self.addEntity(self.player)
        self.levelObjects: list[LevelObject] = []
        self.layerLevelObjects: dict[int, list[LevelObject]] = {}
        self.saveFilePath: str = file
        self.cameraPos: Point = Point(0, 0)
        try:
            saveFile: TextIOWrapper = open(self.saveFilePath, "r")
            save: dict[str, any] = json.loads(saveFile.read())
            self.player.x = save["location"]["x"]
            self.player.y = save["location"]["y"]
            self.player.health = save["health"]
            saveFile.close()
        except:
            self.player.x = 0
            self.player.y = 0
            self.player.health = self.player.maxHealth
        levelFile: TextIOWrapper = open("level.json", "r")
        level: dict[str, list[tuple[int, int]]] = json.loads(levelFile.read())
        for id in level.keys():
            objectType: type[LevelObject] = LevelObject.getClassById(id)
            for pos in level[id]:
                if(objectType.isEntity):
                    self.addEntity(objectType(CoordUtils.pointFromBlock(Point.fromTuple(pos))))
                else:
                    self.addLevelObject(objectType(CoordUtils.pointFromBlock(Point.fromTuple(pos))))

    def addEntity(self, entity: Entity):
        self.entities.append(entity)
        self.layerEntities[1].append(entity)

    def join(self):
        MenuManager.setMenu(None)
        Game.state = Game.GameState.IN_LEVEL
        if(self.player.health <= 0):
            self.respawn()

    def save(self):
        save: dict[str, any] = {
            "location": {
                "x": self.player.x,
                "y": self.player.y
            },
            "health": self.player.health
        }
        saveFile: TextIOWrapper = open(self.saveFilePath, "w")
        json.dump(save, saveFile)
        saveFile.close()

    def leave(self):
        self.save()
        Game.state = Game.GameState.IN_MENU
        MenuManager.setMenu(MenuManager.Menus.MainMenu)

    def pause(self, pause: bool):
        if(pause):
            Game.state = Game.GameState.IN_MENU
            MenuManager.setMenu(MenuManager.Menus.PauseMenu)
        else:
            Game.state = Game.GameState.IN_LEVEL
            MenuManager.setMenu(None)

    def keyPressed(self, key: int):
        match(key):
            case pygame.K_ESCAPE:
                self.pause(True)

    def update(self, time: int):
        for entity in self.entities:
            entity.update(time)
        if(self.player.isAlive == False and MenuManager.currentMenu != MenuManager.Menus.DeathMenu):
            Game.state = Game.GameState.IN_MENU
            MenuManager.setMenu(MenuManager.Menus.DeathMenu)
        self.cameraPos = Point(self.player.pos.x - Game.screen.get_width() / 2 + self.player.surface.get_width() / 2, self.player.pos.y - Game.screen.get_height() / 2 + self.player.surface.get_height() / 2)

    def render(self, screen : pygame.Surface):
        for i in self.layerLevelObjects:
            for levelObject in self.layerLevelObjects[i]:
                levelObject.renderOffset(screen, self.cameraPos.reverseSign())
            if i in self.layerEntities:
                for entity in self.layerEntities[i]:
                    entity.renderOffset(screen, self.cameraPos.reverseSign())
        for i in range(self.player.health):
            Textures.HEART.renderAt(screen, Point(Textures.HEART.surface.get_width() * i + 2, 2))

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
    
    def respawn(self):
        self.player.respawn()
        MenuManager.setMenu(None)
        Game.state = Game.GameState.IN_LEVEL
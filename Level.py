import json, MenuManager, Game, pygame, Textures, CoordUtils
from Player import Player
from Entity import Entity
from Point import Point
from io import TextIOWrapper
from LevelObject import LevelObject

class Level:
    def __init__(self, file: str):
        self.player: Player = Player()
        self.entities: list[Entity] = []
        self.entities.append(self.player)
        self.levelObjects: list[LevelObject] = []
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
                self.levelObjects.append(objectType(CoordUtils.pointFromBlock(Point.fromTuple(pos))))

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
        self.player.update(time)
        if(self.player.isAlive == False and MenuManager.currentMenu != MenuManager.Menus.DeathMenu):
            Game.state = Game.GameState.IN_MENU
            MenuManager.setMenu(MenuManager.Menus.DeathMenu)
        self.cameraPos = Point(self.player.pos.x - Game.screen.get_width() / 2 + self.player.surface.get_width() / 2, self.player.pos.y - Game.screen.get_height() / 2 + self.player.surface.get_height() / 2)

    def render(self, screen : pygame.Surface):
        for levelObject in self.levelObjects:
            levelObject.renderOffset(screen, self.cameraPos.reverseSign())
        for entity in self.entities:
            entity.renderOffset(screen, self.cameraPos.reverseSign())
        for i in range(self.player.health):
            Textures.HEART.renderAt(screen, Point(Textures.HEART.surface.get_width() * i + 2, 2))
    
    def respawn(self):
        self.player.respawn()
        MenuManager.setMenu(None)
        Game.state = Game.GameState.IN_LEVEL
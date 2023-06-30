import json, MenuManager, Game, pygame, Textures, CoordUtils, random, math
from Entities.Player import Player
from Entity import Entity
from Point import Point
from io import TextIOWrapper
from LevelObject import LevelObject
from GameObject import GameObject
from TextDialogue import TextDialogue
from LevelObjectProperty import LevelObjectProperty
from Entities.Zombie import Zombie
from Entities.Slime import Slime
from Enemy import Enemy
from TextBox import TextBox
from threading import Thread
from Entities.NPC import NPC
from LevelObjects.Water import Water
from LevelObjects.WoodFloor import WoodFloor

class Level:
    def __init__(self, file: str):
        self.player: Player = Player(Point(0, 0))
        self.entities: list[Entity] = []
        self.layerEntities: dict[int, list[Entity]] = { 0: [], 1: [] }
        self.addEntity(self.player)
        self.levelObjects: list[LevelObject] = []
        self.currentFile = "levels\\level.json"
        self.layerLevelObjects: dict[int, list[LevelObject]] = {}
        self.interactableObjects: list[LevelObject] = []
        self.collisionObjects: list[LevelObject] = []
        self.saveFilePath: str = file
        self.dialogue: TextDialogue = None
        self.raid: list[Enemy] = []
        self.isPaused: bool = False
        self.currentQuest: int = None
        self.cameraPos: tuple[int, int] = (0, 0)
        self.bossBar: GameObject = None
        self.raidHealth: int = 0
        self.bossBarTitle: TextBox = None
        self.questDisplay: GameObject = None
        self.overWorldPos: Point = None
        self.isNight: bool = False
        self.maxRaidHealth: int = 0

        try:
            saveFile = open(file, "r")
            string = ""
            for line in saveFile.readlines():
                string += line
            save = json.loads(string)
            self.player.x = save["location"]["x"]
            self.player.y = save["location"]["y"]
            self.player.health = save["health"]
            self.currentQuest = save["currentQuest"]
            self.currentFile = save["currentFile"]
            self.overWorldPos = Point.fromTuple(save["overworldPos"])
            saveFile.close()
        except:
            pass

        self.loadFile(self.currentFile)

    def loadFile(self, path: str):
        self.currentFile = path
        self.entities = []
        self.layerEntities = { 0: [], 1: [] }
        self.addEntity(self.player)
        if(path == "levels\\level.json"):
            for raidEnemy in self.raid:
                self.addEntity(raidEnemy)
        self.levelObjects = []
        self.layerLevelObjects = {}
        self.interactableObjects = []
        self.collisionObjects = []
        levelFile: TextIOWrapper = open(path, "r")
        level: dict[str, list[list]] = json.loads(levelFile.read())
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
                if(objectType.isEntity):
                    self.addEntity(object)
                else:
                    self.addLevelObject(object)
                if(objectType.interactTextStr != None):
                    self.interactableObjects.append(object)
                if(object.collisionRect != None):
                    self.collisionObjects.append(object)
        if(self.currentQuest != None):
            if(self.currentQuest >= 1 and self.currentQuest <= 3):
                for entity in self.entities:
                    if(type(entity) == NPC):
                        self.removeEntity(entity)
                        break
                if(self.currentQuest == 2 and len(self.raid) == 0):
                    self.spawnRaid()
                    self.isNight = True
            elif(self.currentQuest >= 4 and path == "levels\\level.json"):
                for entity in self.entities:
                    if(type(entity) == NPC):
                        entity.x = 2300
                        entity.y = 1050
                        break
                removeObjects: list[LevelObject] = []
                for levelObject in self.levelObjects:
                    coords: Point = levelObject.pos
                    if(type(levelObject) == Water and coords.x >= 2400 and coords.x <= 2800 and coords.y >= 900 and coords.y <= 1100):
                        removeObjects.append(levelObject)
                for obj in removeObjects:
                    self.removeLevelObject(obj)
                for x in range(2400, 2801, 50):
                    for y in range(900, 1101, 50):
                        self.addLevelObject(WoodFloor(Point(x, y)))

    def getRandomEnemyPos(self, type: type[Enemy]):
        pos: Point = Point(random.randint(-950, 2358), random.randint(-340, 2459))
        while(type.collidesList(self.collisionObjects, pos)):
            pos = Point(random.randint(-950, 2358), random.randint(-340, 2459))
        return pos

    def onRaidDamage(self):
        self.raidHealth = 0
        for enemy in self.raid:
            self.raidHealth += enemy.health
        self.updateRaidBossBar()
        if(self.raidHealth == 0 and self.currentQuest == 2):
            self.setCurrentQuest(3)

    def updateRaidBossBar(self):
        self.bossBar = GameObject(pygame.Surface((Game.screen.get_width() * 0.8, 10)), Point(Game.screen.get_width() * 0.1, 45))
        self.bossBar.surface.fill(pygame.Color(255, 255, 255))
        if(self.raidHealth == 0):
            return
        healthRect: pygame.Rect = (0, 0, self.bossBar.surface.get_width() / (self.maxRaidHealth / self.raidHealth), 10)
        self.bossBar.surface.fill(pygame.Color(255, 0, 0), healthRect)
        if(self.bossBarTitle == None or self.bossBarTitle.text != "Monster"):
            self.bossBarTitle = TextBox("Monster", Point(0, Game.screen.get_height() / 2 - 20), font = pygame.font.Font("fonts\\Roboto-Bold.ttf", 40), fontColor = pygame.Color(255, 255, 255))

    def spawnRaid(self):
        self.raid = []
        for i in range(7 - math.floor(math.log(random.random() * 5 + 1, 1.75))):
            type: type[Enemy] = Zombie if random.random() >= 0.85 else Slime
            enemy: Enemy = type(self.getRandomEnemyPos(type), self.onRaidDamage)
            self.addEntity(enemy)
            self.raid.append(enemy)
        type: type[Enemy] = Zombie if random.random() >= 0.85 else Slime
        enemy: Enemy = Zombie(self.getRandomEnemyPos(type), self.onRaidDamage)
        self.addEntity(enemy)
        self.raid.append(enemy)
        for enemy in self.raid:
            self.maxRaidHealth += enemy.maxHealth
        self.onRaidDamage()
            
    def addEntity(self, entity: Entity):
        self.entities.append(entity)
        self.layerEntities[1].append(entity)

    def removeEntity(self, entity: Entity):
        self.entities.remove(entity)
        self.layerEntities[entity.renderingLayer].remove(entity)
        try:
            self.raid.remove(entity)
        except:
            pass
        try:
            self.interactableObjects.remove(entity)
        except:
            pass

    def setCurrentQuest(self, i: int):
        self.currentQuest = i
        self.updateQuestDisplay()
        self.save()

    def updateQuestDisplay(self):
        fontSurface: pygame.Surface = pygame.font.Font("fonts\\Roboto-Bold.ttf", 30).render("Quest: " + self.getCurrentQuestAsString(), True, pygame.Color(255, 255, 255))
        bgSurface: pygame.Surface = pygame.Surface((fontSurface.get_width(), fontSurface.get_height()), pygame.SRCALPHA).convert_alpha()
        bgSurface.fill(pygame.Color(0, 0, 0, 100))
        bgSurface.blit(fontSurface, (0, 0))
        self.questDisplay = GameObject(bgSurface, Point(Game.screen.get_width() - fontSurface.get_width(), 0))

    def join(self):
        MenuManager.setMenu(None)
        Game.state = Game.GameState.IN_LEVEL
        if(self.player.health <= 0):
            self.respawn()
        if(self.currentQuest == None):
            self.player.x = -95
            self.player.y = 755
            self.update(0)
            self.entities[1].interact()
            self.currentQuest = 0
        self.updateQuestDisplay()

    def save(self):
        save: dict[str, any] = {
            "location": {
                "x": self.player.x,
                "y": self.player.y
            },
            "health": self.player.health,
            "currentQuest": self.currentQuest,
            "currentFile": self.currentFile,
            "overworldPos": self.overWorldPos.toTuple()
        }
        saveFile: TextIOWrapper = open(self.saveFilePath, "w")
        json.dump(save, saveFile)
        saveFile.close()

    def leave(self):
        self.save()
        Game.state = Game.GameState.IN_MENU
        MenuManager.setMenu(MenuManager.Menus.MainMenu)

    def openPauseMenu(self, pause: bool):
        if(pause):
            Game.state = Game.GameState.IN_MENU
            MenuManager.setMenu(MenuManager.Menus.PauseMenu)
        else:
            Game.state = Game.GameState.IN_LEVEL
            MenuManager.setMenu(None)

    def keyPressed(self, key: int):
        match(key):
            case pygame.K_ESCAPE:
                self.openPauseMenu(True)
            case pygame.K_e:
                if(not self.isPaused):
                    self.player.interact()

    def showText(self, dialogue: TextDialogue):
        self.isPaused = True
        self.dialogue = dialogue

    def update(self, time: int):
        if(self.isPaused):
            return

        for entity in self.entities:
            entity.update(time)
        if(self.player.isAlive == False and MenuManager.currentMenu != MenuManager.Menus.DeathMenu):
            Game.state = Game.GameState.IN_MENU
            MenuManager.setMenu(MenuManager.Menus.DeathMenu)
        self.cameraPos = (self.player.pos.x - Game.screen.get_width() / 2 + self.player.surface.get_width() / 2, self.player.pos.y - Game.screen.get_height() / 2 + self.player.surface.get_height() / 2)

    def getCurrentQuestAsString(self) -> str:
        if(self.currentQuest == 0):
            return "Rede mit dem Bürgermeister"
        elif(self.currentQuest == 1 or self.currentQuest == 2):
            return "Besiege die Monster"
        elif(self.currentQuest == 3):
            return "Berichte dem Bürgermeister von deinem Sieg gegen die Monster"
        elif(self.currentQuest == 4):
            return "Besuche die Dorfbewohnerin im Osten der Insel"
        elif(self.currentQuest == 5):
            return "Erkunde die Basis der Monster"
        elif(self.currentQuest == 6):
            return "Besiege den Boss"

    def render(self, screen: pygame.Surface):
        for i in self.layerLevelObjects:
            for levelObject in self.layerLevelObjects[i]:
                if(levelObject.isNotOnScreen(self.cameraPos)):
                    continue
                levelObject.renderMinusOffset(screen, self.cameraPos)
            if i in self.layerEntities:
                for entity in self.layerEntities[i]:
                    if(entity.isNotOnScreen(self.cameraPos)):
                        continue
                    entity.renderMinusOffset(screen, self.cameraPos)
        if(self.isNight):
            Textures.NIGHT_OVERLAY.render(screen)
        for i in range(self.player.health):
            Textures.HEART.renderAt(screen, (Textures.HEART.surface.get_width() * i + 2 * i + 2, 2))
        if(self.dialogue != None):
            self.dialogue.render(screen)
        if(len(self.raid) > 0):
            self.bossBar.render(screen)
            self.bossBarTitle.render(screen)
        if(self.questDisplay != None and self.dialogue == None):
            self.questDisplay.render(screen)

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
        try:
            self.interactableObjects.remove(object)
        except:
            pass
        try:
            self.collisionObjects.remove(object)
        except:
            pass
    
    def respawn(self):
        self.player.respawn()
        MenuManager.setMenu(None)
        Game.state = Game.GameState.IN_LEVEL

    def mousePressed(self, button: int, pos: Point):
        if(button != 1):
            return
        if(not self.isPaused):
            self.player.attack()
            return
        if(self.dialogue != None):
            if(self.dialogue.increaseIndex() < 0):
                self.dialogue = None
                self.isPaused = False
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

class Level:
    def __init__(self, file: str):
        self.player: Player = Player(Point(0, 0))
        self.entities: list[Entity] = []
        self.layerEntities: dict[int, list[Entity]] = { 0: [], 1: [] }
        self.addEntity(self.player)
        self.levelObjects: list[LevelObject] = []
        self.layerLevelObjects: dict[int, list[LevelObject]] = {}
        self.interactableObjects: list[LevelObject] = []
        self.collisionObjects: list[LevelObject] = []
        self.particles: list[GameObject] = []
        self.saveFilePath: str = file
        self.dialogue: TextDialogue = None
        self.raid: list[Enemy] = []
        self.isPaused: bool = False
        self.cameraPos: tuple[int, int] = (0, 0)
        self.bossBar: GameObject = None
        self.bossBarTitle: TextBox = None
        self.maxRaidHealth: int = 0
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
        self.spawnRaid()

    def getRandomEnemyPos(self, type: type[Enemy]):
        pos: Point = Point(random.randint(-950, 2358), random.randint(-340, 2459))
        while(type.collidesList(self.collisionObjects, pos)):
            pos = Point(random.randint(-950, 2358), random.randint(-340, 2459))
        return pos

    def onRaidDamage(self):
        self.updateRaidBossBar()

    def updateRaidBossBar(self):
        self.bossBar = GameObject(pygame.Surface((Game.screen.get_width() * 0.8, 10)), Point(Game.screen.get_width() * 0.1, 45))
        self.bossBar.surface.fill(pygame.Color(255, 255, 255))
        raidHealth = 0
        for enemy in self.raid:
            raidHealth += enemy.health
        if(raidHealth == 0):
            return
        healthRect: pygame.Rect = (0, 0, self.bossBar.surface.get_width() / (self.maxRaidHealth / raidHealth), 10)
        self.bossBar.surface.fill(pygame.Color(255, 0, 0), healthRect)
        if(self.bossBarTitle == None or self.bossBarTitle.text != "Monster"):
            self.bossBarTitle = TextBox("Monster", Point(0, Game.screen.get_height() / 2 - 20), font = pygame.font.Font("fonts\\Roboto-Bold.ttf", 40), fontColor = pygame.Color(255, 255, 255))

    def spawnRaid(self):
        self.raid = []
        for i in range(8 - math.floor(math.log(random.random() * 5 + 1, 1.75))):
            type: type[Enemy] = Zombie if random.random() >= 0.8 else Slime
            pos: Point = self.getRandomEnemyPos(type)
            enemy: Enemy = Zombie(pos, self.onRaidDamage) if random.random() >= 0.9 else Slime(pos, self.onRaidDamage)
            self.addEntity(enemy)
            self.raid.append(enemy)
        for enemy in self.raid:
            self.maxRaidHealth += enemy.maxHealth
        self.updateRaidBossBar()
            
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
            if(entity.isNotOnScreen(self.cameraPos)):
                continue
            entity.update(time)
        if(self.player.isAlive == False and MenuManager.currentMenu != MenuManager.Menus.DeathMenu):
            Game.state = Game.GameState.IN_MENU
            MenuManager.setMenu(MenuManager.Menus.DeathMenu)
        self.cameraPos = (self.player.pos.x - Game.screen.get_width() / 2 + self.player.surface.get_width() / 2, self.player.pos.y - Game.screen.get_height() / 2 + self.player.surface.get_height() / 2)

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
        for particle in self.particles:
            if(particle.isNotOnScreen(self.cameraPos)):
                continue
            particle.renderMinusOffset(screen, self.cameraPos)
        for i in range(self.player.health):
            Textures.HEART.renderAt(screen, (Textures.HEART.surface.get_width() * i + 2 * i + 2, 2))
        if(self.dialogue != None):
            self.dialogue.render(screen)
        if(len(self.raid) > 0):
            self.bossBar.render(screen)
            self.bossBarTitle.render(screen)

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
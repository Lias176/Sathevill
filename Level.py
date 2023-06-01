import Player, json, MenuManager, Game, pygame
from GameElement import GameElement

class Level:
    def __init__(self, file : str):
        self.player = Player.Player()
        self.entities = []
        self.entities.append(self.player)
        self.saveFilePath = file
        self.maxLives = 3
        self.lives = []
        self.ui = []
        self.cameraPos = (0, 0)
        try:
            saveFile = open(self.saveFilePath, "r")
            save = json.loads(saveFile.read())
            self.player.x = save["location"]["x"]
            self.player.y = save["location"]["y"]
            self.player.lives = save["lives"]
        except:
            self.player.x = 0
            self.player.y = 0
            self.player.lives = self.maxLives


    def join(self):
        MenuManager.setMenu(None)
        Game.inGame = True
        if(self.player.lives <= 0):
            self.respawn()

    def save(self):
        save = {
            "location": {
                "x": self.player.x,
                "y": self.player.y
            },
            "lives": self.player.lives
        }
        saveFile = open(self.saveFilePath, "w")
        json.dump(save, saveFile)
        saveFile.close()

    def leave(self):
        self.save()
        Game.inGame = False
        MenuManager.setMenu(MenuManager.Menus.MainMenu)

    def pause(self, pause : bool):
        if(pause):
            Game.inGame = False
            MenuManager.setMenu(MenuManager.Menus.PauseMenu)
        else:
            Game.inGame = True
            MenuManager.setMenu(None)

    def keyPressed(self, key : int):
        match(key):
            case pygame.K_ESCAPE:
                self.pause(True)

    def update(self, time : int):
        self.player.update(time)
        while(len(self.lives) > self.player.lives):
            self.ui.remove(self.lives[len(self.lives) - 1])
            self.lives.pop()
        while(len(self.lives) < self.player.lives):
            self.lives.append(GameElement(pygame.image.load("images\\heart.png"), (40 * len(self.lives) + 5, 5)))
            self.ui.append(self.lives[len(self.lives) - 1])
        if(self.player.isAlive == False and MenuManager.currentMenu != MenuManager.Menus.DeathMenu):
            Game.inGame = False
            MenuManager.setMenu(MenuManager.Menus.DeathMenu)
        self.cameraPos = (self.player.pos[0] - Game.screen.get_width() / 2 + self.player.surface.get_width() / 2, self.player.pos[1] - Game.screen.get_height() / 2 + self.player.surface.get_height() / 2)

    def render(self, screen : pygame.Surface):
        offsetGameElements : list[GameElement] = []
        for entity in self.entities:
            screen.blit(entity.surface, (entity.pos[0] - self.cameraPos[0], entity.pos[1] - self.cameraPos[1]))
        for uiElement in self.ui:
            screen.blit(uiElement.surface, uiElement.pos)
    
    def respawn(self):
        self.player.x = 0
        self.player.y = 0
        self.player.isAlive = True
        self.player.lives = self.maxLives
        MenuManager.setMenu(None)
        Game.inGame = True
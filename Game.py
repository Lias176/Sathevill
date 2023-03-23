import pygame, Player, MenuManager, Enemy, copy, json, LevelCreator, GameElement

inGame = False
inLevelEditor = False
camera = (0, 0)
screen = None
sprites = pygame.sprite.Group()
player = None
currentSave = None
ui = []
lives = []

def loadSave(file : str):
    MenuManager.setMenu(None)
    global inGame, player, currentSave
    inGame = True
    player = Player.Player()
    sprites.add(player)
    enemy = Enemy.Enemy()
    enemy.rect.x = 500
    enemy.rect.y = 500
    sprites.add(enemy)
    currentSave = file
    try:
        saveFile = open(file)
        save = json.loads(saveFile.read())
        player.x = save["location"]["x"]
        player.y = save["location"]["y"]
        player.lives = save["lives"]
    except:
        player.x = 0
        player.y = 0
        player.lives = 3
    if(player.lives <= 0):
        respawn()

def leaveGame():
    save()
    global inGame, sprites, player, ui, lives
    inGame = False
    player = None
    sprites = pygame.sprite.Group()
    lives = []
    ui = []
    MenuManager.setMenu(MenuManager.Menus.MainMenu)

def save():
    global currentSave
    save = {
        "location": {
            "x": player.x,
            "y": player.y
        },
        "lives": player.lives
    }
    saveFile = open(currentSave, "w")
    json.dump(save, saveFile)

def init(initScreen : pygame.Surface):
    global screen
    screen = initScreen

def update(time : int):
    global inGame, player, camera
    player.update(time)
    while(len(lives) > player.lives):
        ui.remove(lives[len(lives) - 1])
        lives.pop()
    while(len(lives) < player.lives):
        lives.append(GameElement.GameElement(pygame.image.load("images\\heart.png").convert(), (40 * len(lives) + 5, 5)))
        ui.append(lives[len(lives) - 1])
    if(player.isAlive == False and MenuManager.currentMenu != MenuManager.Menus.DeathMenu):
        inGame = False
        MenuManager.setMenu(MenuManager.Menus.DeathMenu)
    camera = (player.rect.x - screen.get_width() / 2 + player.image.get_width() / 2, player.rect.y - screen.get_height() / 2 + player.image.get_height() / 2)

def getSprites() -> pygame.sprite.Group:
    global sprites
    offsetSprites = pygame.sprite.Group()
    for sprite in sprites:
        offsetSprite = copy.copy(sprite)
        offsetSprite.rect = sprite.rect.copy()
        offsetSprite.rect.x -= camera[0]
        offsetSprite.rect.y -= camera[1]
        offsetSprites.add(offsetSprite)
    return offsetSprites

def keyPressed(key : int):
    match(key):
        case pygame.K_ESCAPE:
            pause(True)

def pause(pause : bool):
    global inGame
    if(pause):
        inGame = False
        MenuManager.setMenu(MenuManager.Menus.PauseMenu)
    else:
        inGame = True
        MenuManager.setMenu(None)

def respawn():
    global player, inGame
    player.x = 0
    player.y = 0
    player.isAlive = True
    player.lives = 3
    MenuManager.setMenu(None)
    inGame = True

def openLevelCreator():
    global inLevelEditor
    inLevelEditor = True
    LevelCreator.openLevelEditor()
    MenuManager.setMenu(None)
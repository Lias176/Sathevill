import pygame, Player, MenuManager, Enemy, copy, json

inGame = False

cameraX = 0
cameraY = 0
screen = None
sprites = pygame.sprite.Group()
player = None
currentSave = None
ui = []
lives = []

def loadSave(file : str):
    MenuManager.setMenu(None)
    global inGame
    inGame = True
    global player
    player = Player.Player()
    sprites.add(player)
    enemy = Enemy.Enemy()
    enemy.rect.x = 500
    enemy.rect.y = 500
    sprites.add(enemy)
    global currentSave
    currentSave = file
    try:
        saveFile = open(file)
        save = json.loads(saveFile.read())
        player.rect.x = save["location"]["x"]
        player.rect.y = save["location"]["y"]
        player.lives = save["lives"]
    except:
        player.rect.x = 0
        player.rect.y = 0
        player.lives = 3
    if(player.lives <= 0):
        respawn()

def leave():
    save()
    global inGame
    global sprites
    global player
    global ui
    global lives
    inGame = False
    player = None
    sprites = pygame.sprite.Group()
    lives = []
    ui = []
    MenuManager.setMenu(MenuManager.Menus.MainMenu)

def save():
    save = {
        "location": {
            "x": player.rect.x,
            "y": player.rect.y
        },
        "lives": player.lives
    }
    global currentSave
    saveFile = open(currentSave, "w")
    json.dump(save, saveFile)

def init(initScreen : pygame.Surface):
    global screen
    screen = initScreen

def update(time : int):
    global inGame
    global player
    global cameraX
    global cameraY
    player.update(time)
    while(len(lives) > player.lives):
        ui.remove(lives[len(lives) - 1])
        lives.pop()
    while(len(lives) < player.lives):
        lives.append((pygame.image.load("images\\heart.png").convert(), (40 * len(lives) + 5, 5)))
        ui.append(lives[len(lives) - 1])
    if(player.isAlive == False and MenuManager.currentMenu != MenuManager.Menus.DeathMenu):
        inGame = False
        MenuManager.setMenu(MenuManager.Menus.DeathMenu)
    cameraX = player.rect.x - pygame.Surface.get_width(screen) / 2 + player.image.get_width() / 2
    cameraY = player.rect.y - pygame.Surface.get_height(screen) / 2 + player.image.get_height() / 2

def getSprites() -> pygame.sprite.Group:
    global sprites
    offsetSprites = pygame.sprite.Group()
    for sprite in sprites:
        offsetSprite = copy.copy(sprite)
        offsetSprite.rect = sprite.rect.copy()
        offsetSprite.rect.x -= cameraX
        offsetSprite.rect.y -= cameraY
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
        MenuManager.setMenu(None)
        inGame = True

def respawn():
    global player
    player.rect.x = 0
    player.rect.y = 0
    player.isAlive = True
    player.lives = 3
    global inGame
    MenuManager.setMenu(None)
    inGame = True
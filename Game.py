import pygame, Player, MenuManager, Enemy, copy

inGame = False

cameraX = 0
cameraY = 0
screen = None
sprites = pygame.sprite.Group()
player = None

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

def leave():
    global inGame
    global sprites
    inGame = False
    sprites = pygame.sprite.Group()

def init(initScreen : pygame.Surface):
    global screen
    screen = initScreen

def update(time : int):
    global player
    global cameraX
    global cameraY
    player.update(time)
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
    if(pause):
        global inGame
        inGame = False
        MenuManager.setMenu(MenuManager.Menus.PauseMenu)
    else:
        MenuManager.setMenu(None)
        inGame = True
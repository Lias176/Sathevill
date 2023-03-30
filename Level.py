import Player, Enemy, json, MenuManager, Game, GameElement, pygame

player = None
currentSave = None
screen = None
gameElements = []
lives = []
ui = []
camera = (0, 0)

def init(initScreen : pygame.Surface):
    global screen
    screen = initScreen

def keyPressed(key : int):
    match(key):
        case pygame.K_ESCAPE:
            pause(True)

def loadSave(file : str):
    global player, currentSave
    MenuManager.setMenu(None)
    Game.inGame = True
    player = Player.Player()
    gameElements.append(player)
    enemy = Enemy.Enemy()
    enemy.pos = (250, 250)
    gameElements.append(enemy)
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
    global gameElements, player, lives
    Game.inGame = False
    player = None
    gameElements = []
    lives = []
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

def update(time : int):
    global player, camera
    player.update(time)
    while(len(lives) > player.lives):
        ui.remove(lives[len(lives) - 1])
        lives.pop()
    while(len(lives) < player.lives):
        lives.append(GameElement.GameElement(pygame.image.load("images\\heart.png"), (40 * len(lives) + 5, 5)))
        ui.append(lives[len(lives) - 1])
    if(player.isAlive == False and MenuManager.currentMenu != MenuManager.Menus.DeathMenu):
        Game.inGame = False
        MenuManager.setMenu(MenuManager.Menus.DeathMenu)
    camera = (player.pos[0] - screen.get_width() / 2 + player.surface.get_width() / 2, player.pos[1] - screen.get_height() / 2 + player.surface.get_height() / 2)

def getGameElements():
    finalGameElements = []
    for gameElement in gameElements:
        finalGameElements.append(GameElement.GameElement(gameElement.surface, (gameElement.pos[0] - camera[0], gameElement.pos[1] - camera[1])))
    for uiElement in ui:
        finalGameElements.append(uiElement)
    return finalGameElements

def pause(pause : bool):
    if(pause):
        Game.inGame = False
        MenuManager.setMenu(MenuManager.Menus.PauseMenu)
    else:
        Game.inGame = True
        MenuManager.setMenu(None)

def respawn():
    global player
    player.x = 0
    player.y = 0
    player.isAlive = True
    player.lives = 3
    MenuManager.setMenu(None)
    Game.inGame = True
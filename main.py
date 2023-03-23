import sys, pygame, MenuManager, Button, os, Game, LevelCreator, Level

if(os.path.isdir(os.path.expanduser("~\\sathevill")) == False):
    os.mkdir(os.path.expanduser("~\\sathevill"))

pygame.init()

screen = pygame.display.set_mode((1920, 1032))
clock = pygame.time.Clock()

MenuManager.init(screen)
Button.init(screen)
Level.init(screen)
LevelCreator.init(screen)

MenuManager.setMenu(MenuManager.Menus.MainMenu)

while True:
    for event in pygame.event.get():
        match(event.type):
            case pygame.QUIT:
                sys.exit()
            case pygame.MOUSEBUTTONDOWN:
                Game.mouseClicked(event.button)
            case pygame.KEYDOWN:
                Game.keyPressed(event.key)

    Game.update(clock.get_time())
    
    screen.fill("black")
    for gameElement in Game.getGameElements():
        screen.blit(gameElement.surface, gameElement.pos)

    pygame.display.flip()
    clock.tick()
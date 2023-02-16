import sys, pygame, MenuManager, Button, os, Game

if(os.path.isdir(os.path.expanduser("~\\sathevill")) == False):
    os.mkdir(os.path.expanduser("~\\sathevill"))

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

MenuManager.init(screen)
Button.init(screen)
Game.init(screen)

MenuManager.setMenu(MenuManager.Menus.MainMenu)

while True:
    for event in pygame.event.get():
        match(event.type):
            case pygame.QUIT:
                sys.exit()
            case pygame.MOUSEBUTTONDOWN:
                if(event.button == 1):
                    Button.mouseClicked()
            case pygame.KEYDOWN:
                if(Game.inGame):
                    Game.keyPressed(event.key)
                else:
                    MenuManager.keyPressed(event.key)

    if(Game.inGame):
        screen.fill("black")
        Game.update(clock.get_time())
    if(Game.inGame):
        Game.getSprites().draw(screen)

    pygame.display.flip()
    clock.tick()
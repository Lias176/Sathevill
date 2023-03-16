import sys, pygame, MenuManager, Button, os, Game, LevelCreator

if(os.path.isdir(os.path.expanduser("~\\sathevill")) == False):
    os.mkdir(os.path.expanduser("~\\sathevill"))

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

MenuManager.init(screen)
Button.init(screen)
Game.init(screen)
LevelCreator.init(screen)

MenuManager.setMenu(MenuManager.Menus.MainMenu)

while True:
    for event in pygame.event.get():
        match(event.type):
            case pygame.QUIT:
                sys.exit()
            case pygame.MOUSEBUTTONDOWN:
                if(event.button == 1):
                    if(Game.inLevelEditor):
                        LevelCreator.mouseClicked()
                    else:
                        Button.mouseClicked()
            case pygame.KEYDOWN:
                if(Game.inGame):
                    Game.keyPressed(event.key)
                else:
                    MenuManager.keyPressed(event.key)

    if(Game.inGame):
        Game.update(clock.get_time())
    elif(Game.inLevelEditor):
        LevelCreator.update()
    if(Game.inGame):
        screen.fill("black")
        Game.getSprites().draw(screen)
        for uiElement in Game.ui:
            screen.blit(uiElement.surface, uiElement.pos)
    elif(Game.inLevelEditor):
        screen.fill("black")
        for levelObject in LevelCreator.levelObjects:
            screen.blit(levelObject.surface, levelObject.pos)
        for uiElement in LevelCreator.ui:
            screen.blit(uiElement.surface, uiElement.pos)

    pygame.display.flip()
    clock.tick()
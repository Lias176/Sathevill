import sys, pygame, MenuManager, Button, os, Game, LevelCreator

if(os.path.isdir(os.path.expanduser("~\\sathevill")) == False):
    os.mkdir(os.path.expanduser("~\\sathevill"))

pygame.init()

screen = pygame.display.set_mode((1920, 1032))
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
                if(Game.inLevelEditor):
                    LevelCreator.mouseClicked(event.button)
                if(event.button == 1):
                    if(Game.inLevelEditor == False):
                        Button.mouseClicked()
            case pygame.KEYDOWN:
                if(Game.inGame):
                    Game.keyPressed(event.key)
                elif(Game.inLevelEditor):
                    LevelCreator.keyPressed(event.key)
                else:
                    MenuManager.keyPressed(event.key)

    if(Game.inGame):
        Game.update(clock.get_time())
    elif(Game.inLevelEditor):
        LevelCreator.update()
    if(Game.inGame):
        screen.fill("black")
        Game.getSprites().draw(screen)
        for gameElement in Game.ui:
            screen.blit(gameElement.surface, gameElement.pos)
    elif(Game.inLevelEditor):
        screen.fill("black")
        for levelObject in LevelCreator.getLevelObjects():
            screen.blit(levelObject.surface, levelObject.pos)
        for gameElement in LevelCreator.ui:
            screen.blit(gameElement.surface, gameElement.pos)

    pygame.display.flip()
    clock.tick()
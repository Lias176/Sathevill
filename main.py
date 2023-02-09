import sys, pygame, MenuManager, Button

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

MenuManager.screen = screen

MenuManager.setMenu(MenuManager.Menus.MainMenu)

while True:
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            sys.exit()
        elif(event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            Button.mouseClicked()

    pygame.display.flip()
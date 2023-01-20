import sys, pygame, MenuManager

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

while True:
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            sys.exit()

    pygame.display.flip() 
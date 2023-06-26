import sys, pygame, os
from Point import Point

if(os.path.isdir(os.path.expanduser("~\\sathevill")) == False):
    os.mkdir(os.path.expanduser("~\\sathevill"))

pygame.init()

screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
clock = pygame.time.Clock()

import Game, MenuManager

Game.init(screen)

MenuManager.setMenu(MenuManager.Menus.MainMenu)

while True:
    for event in pygame.event.get():
        match(event.type):
            case pygame.QUIT:
                sys.exit()
            case pygame.MOUSEBUTTONDOWN:
                Game.mouseClicked(event.button, Point.fromTuple(event.pos))
            case pygame.MOUSEBUTTONUP:
                Game.mouseUp(event.button)
            case pygame.KEYDOWN:
                Game.keyPressed(event.key)
            case pygame.MOUSEWHEEL:
                Game.mouseWheel(event.y)
            case pygame.MOUSEMOTION:
                Game.mouseMotion(Point.fromTuple(event.pos))

    Game.update(clock.get_time())
    Game.render(screen)

    pygame.display.flip()
    clock.tick()
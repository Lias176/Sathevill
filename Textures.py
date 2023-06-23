import pygame
from GameObject import GameObject
from Point import Point

HEART = GameObject(pygame.image.load("images\\heart.png"), Point(0, 0))
PLAYER_DOWN = GameObject(pygame.image.load("images\\player\\down.png"), Point(0, 0))
PLAYER_RIGHT = GameObject(pygame.image.load("images\\player\\right.png"), Point(0, 0))
PLAYER_UP = GameObject(pygame.image.load("images\\player\\up.png"), Point(0, 0))
PLAYER_LEFT = GameObject(pygame.image.load("images\\player\\left.png"), Point(0, 0))
PLAYER_WALK_DOWN_0 = GameObject(pygame.image.load("images\\player\\walk\\down0.png"), Point(0, 0))
PLAYER_WALK_DOWN_1 = GameObject(pygame.image.load("images\\player\\walk\\down1.png"), Point(0, 0))
PLAYER_WALK_LEFT_0 = GameObject(pygame.image.load("images\\player\\walk\\left0.png"), Point(0, 0))
PLAYER_WALK_LEFT_1 = GameObject(pygame.image.load("images\\player\\walk\\left1.png"), Point(0, 0))
PLAYER_WALK_UP_0 = GameObject(pygame.image.load("images\\player\\walk\\up0.png"), Point(0, 0))
PLAYER_WALK_UP_1 = GameObject(pygame.image.load("images\\player\\walk\\up1.png"), Point(0, 0))
PLAYER_WALK_RIGHT_0 = GameObject(pygame.image.load("images\\player\\walk\\right0.png"), Point(0, 0))
PLAYER_WALK_RIGHT_1 = GameObject(pygame.image.load("images\\player\\walk\\right1.png"), Point(0, 0))
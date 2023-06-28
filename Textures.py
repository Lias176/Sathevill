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
SLIME_LEFT = GameObject(pygame.image.load("images\\slime\\left.png"), Point(0, 0))
SLIME_RIGHT = GameObject(pygame.image.load("images\\slime\\right.png"), Point(0, 0))
GRASS_0 = GameObject(pygame.image.load("images\\grass0.png"), Point(0, 0))
HOUSE = GameObject(pygame.image.load("images\\House.png"), Point(0, 0))
HOUSE_2 = GameObject(pygame.image.load("images\\House2.png"), Point(0, 0))
HOUSE_3 = GameObject(pygame.image.load("images\\House3.png"), Point(0, 0))
HOUSE_4 = GameObject(pygame.image.load("images\\House4.png"), Point(0, 0))
MONSTER_BASE_ENTRY = GameObject(pygame.image.load("images\\monsterbaseEntry.png"), Point(0, 0))
MONSTER_BASE_FLOOR = GameObject(pygame.image.load("images\\monsterbaseFloor.png"), Point(0, 0))
PALM = GameObject(pygame.image.load("images\\palm.png"), Point(0, 0))
SAND = GameObject(pygame.image.load("images\\sand.png"), Point(0, 0))
SCHOKO_DRINK = GameObject(pygame.image.load("images\\schokoDrink.png"), Point(0, 0))
STONE_0 = GameObject(pygame.image.load("images\\stone0.png"), Point(0, 0))
TREE = GameObject(pygame.image.load("images\\tree.png"), Point(0, 0))
WATER = GameObject(pygame.image.load("images\\water.png"), Point(0, 0))
WOOD_FLOOR = GameObject(pygame.image.load("images\\woodFloor.png"), Point(0, 0))
NPC = GameObject(pygame.image.load("images\\npc.png"), Point(0, 0))
PRESS_E = GameObject(pygame.image.load("images\\pressE.png"), Point(0, 0))
SPEECH_BUBBLE = GameObject(pygame.image.load("images\\speechBubble.png"), Point(0, 0))
GEAR = GameObject(pygame.image.load("images\\gear.png"), Point(0, 0))
ZOMBIE_LEFT = GameObject(pygame.image.load("images\\zombie\\left.png"), Point(0, 0))
ZOMBIE_RIGHT = GameObject(pygame.image.load("images\\zombie\\right.png"), Point(0, 0))
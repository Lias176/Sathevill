import pygame, gc

buttons = []

class Button:
    def __init__(self, screen : pygame.Surface, text : str, font : pygame.font, fontColor : str, bgColor : str, rect : pygame.Rect, onClick : callable):
        self.screen = screen
        self.text = text
        self.font = font
        self.fontColor = fontColor
        self.bgColor = bgColor
        self.onClick = onClick
        self.rect = pygame.draw.rect(screen, bgColor, rect)
        self.fontRect = screen.blit(font.render(text, True, fontColor), (self.rect.x, self.rect.y))
        buttons.append(self)

def mouseClicked():
    for button in buttons:
        if(button.rect.collidepoint(pygame.mouse.get_pos())):
            button.onClick()
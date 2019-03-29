import pygame
import sprites

class stage_platforms(object):
    def __init__(self, x, y, stage):
        self.x = x
        self.y = y
        self.stage = stage
        self.hitbox = (self.x, self.y, 25, 25)
    def draw(self, win, screenWidth, screenHeight):
        #Desenha o chao, que eh comum pra todas as fases
        aux = screenWidth//25
        for i in range(0, aux):
            self.hitbox = ( i*25, screenHeight - 25, 25, 25)
            pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

        if (self.stage == 1):
            for i in range(0, 3):
                self.hitbox = (i * 25, 120, 25, 25)
                pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
            for i in range(0, 4):
                self.hitbox = (screenWidth - (i+1) * 25, 100, 25, 25)
                pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
            for i in range(0, 5):
                self.hitbox = (i * 25, screenHeight - 200, 25, 25)
                pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

        #elif (self.stage == 2):

        #elif (self.stage == 3):
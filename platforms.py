import pygame
import sprites

class stage_platforms(object):
    def __init__(self, x, y, stage):
        self.x = x
        self.y = y
        self.stage = stage
        self.hitbox = (self.x, self.y, 25, 25)
        self.vel = 2
        self.end = x + 300
        self.path = [self.x, self.end] #caminho pre-determinado para o inimigo percorrer
        self.walkCount = 0 #variavel para auxiliar na dinamica do movimento lateral

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel *= (-1)
                self.walkCount = 0

        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel *= (-1)
                self.walkCount = 0

    def draw(self, win, screenWidth, screenHeight):
        self.move()
        #Desenha o chao, que eh comum pra todas as fases
        aux = screenWidth//25
        for i in range(0, aux):
            self.hitbox = ( i*25, screenHeight - 25, 25, 25)
            pygame.draw.rect(win, (0, 255, 0), self.hitbox, 2)

        #Desenha várias plataformas "randômicas"
        if (self.stage == 1):
            win.blit(sprites.spritePlat[3], (120, 470))
            win.blit(sprites.spritePlat[0], (1020, 470))
            win.blit(sprites.spritePlat[3], (870, 430))
            win.blit(sprites.spritePlat[0], (1060, 430))
            win.blit(sprites.spritePlat[0], (1100, 430))
            win.blit(sprites.spritePlat[0], (85, 390))


            win.blit(sprites.spritePlat[2], (120, 470))
            win.blit(sprites.spritePlat[0], (1000, 270))
            win.blit(sprites.spritePlat[0], (1040, 270))
            win.blit(sprites.spritePlat[0], (1080, 270))

import pygame
import sprites

class moving_platforms(object):
    def __init__(self, x, y, width, height, end, numberimg):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.numberimg = numberimg
        self.path = [self.x, self.end] #caminho pre-determinado para a plataforma se mover
        self.walkCount = 0 #variavel para auxiliar na dinamica do movimento lateral
        self.vel = 1.5
        #self.hitbox = (self.x, self.y, 28, 60) #abstracao da plataforma para um retangulo
        self.visible = True 
    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 6:
                self.walkCount = 0

            win.blit(sprites.spritePlat[self.numberimg], (self.x, self.y))
            
            #self.hitbox = (self.x, self.y+2, 135, 40)
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


    #Implementa o movimento da plataforma dentro de um caminho definido
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


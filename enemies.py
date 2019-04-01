import pygame
import sprites

class enemy(object):
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end] #caminho pre-determinado para o inimigo percorrer
        self.walkCount = 0 #variavel para auxiliar na dinamica do movimento lateral
        self.vel = 4
        self.hitbox = (self.x + 20, self.y, 28, 60) #abstracao do inimigo para um retangulo
        self.health = 10 - 1 #vida do inimigo
        self.visible = True #indica se o inimigo esta vivo ou nao
    def draw(self, win):
        self.move()

        #Verifica se esta vivo
        if self.visible:
            if self.walkCount + 1 >= 6:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(sprites.walkRightE[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(sprites.walkLeftE[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            self.hitbox = (self.x, self.y+2, 135, 40)
            pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

            #Desenha a barra de vida, que eh um retangulo verde que diminui por cima de um retangulo vermelho fixo
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 10, self.hitbox[2], 5))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 10, self.hitbox[2] - ((self.hitbox[2]/9) * (9 - self.health)), 5))
    #Implementa o movimento do inimigo dentro do caminho definido
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
    #Metodo que retira a vida do inimigo ou mata ele, caso a vida seja zero
    def hit(self, win, screenWidth, screenHeight):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('Hit!')

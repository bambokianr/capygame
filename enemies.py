import pygame
import sprites

class enemy(object):
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 20, self.y, 28, 60)
        self.health = 10 - 1
        self.visible = True
    def draw(self, win):
        self.move()

        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(sprites.walkRightE[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(sprites.walkLeftE[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            self.hitbox = (self.x + 20, self.y, 28, 60)
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 10, self.hitbox[2], 5))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 10, self.hitbox[2] - ((self.hitbox[2]/9) * (9 - self.health)), 5))
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
    def hit(self, win, screenWidth, screenHeight):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('Hit!')

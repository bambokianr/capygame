import pygame
import sprites

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 20, self.y + 15, 28, 45)
        self.score = 0
    def draw(self, win):
        if (self.walkCount + 1) >= 6:
            self.walkCount = 0

        if not (self.standing):
            if self.left:
                win.blit(sprites.walkLeftP[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(sprites.walkRightP[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.left:
                win.blit(sprites.walkLeftP[0], (self.x, self.y))
            elif self.right:
                win.blit(sprites.walkRightP[0], (self.x, self.y))
            else:
                win.blit(sprites.walkRightP[0], (self.x, self.y))
        self.hitbox = (self.x + 20, self.y + 15, 28, 45)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
    def hit(self, win, screenWidth, screenHeight):
        self.isJump = False
        self.jumpCount = 10
        self.x = 400
        self.y = 480-64
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (screenWidth/2 - text.get_width()/2, screenHeight/2 - text.get_height()/2))
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 101
                    pygame.quit()

class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

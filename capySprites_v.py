import pygame
pygame.init()

screenWidth = 1270
screenHeight = 630

win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Sprites Capy")

#walkRight = [pygame.image.load('resources/img/capy64pxr1.png'), pygame.image.load('resources/img/capy64pxr2.png')]
#walkLeft = [pygame.image.load('resources/img/capy64pxl1.png'), pygame.image.load('resources/img/capy64pxl2.png')]

#bg = pygame.image.load('resources/img/background.png')

clock = pygame.time.Clock()
menu = True
estado = "menu_inicio"

class Relogio:
    def __init__(self, fps):
        self.fps = fps
        self.relogio = pygame.time.Clock()

class Tela:
    def __init__(self, largura, altura, titulo, enderecoImagemFundo):
        self.largura = largura
        self.altura = altura
        self.titulo = titulo
        self.imagemFundo = pygame.image.load(enderecoImagemFundo)
        self.imagemFundo = pygame.transform.scale(self.imagemFundo, (self.largura, self.altura))
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption(self.titulo)

class Audio:
    def __init__(self, endereco, volume):
        self.audio = pygame.mixer.Sound(endereco)
        self.audio.set_volume(volume)

    def play(self):
        self.audio.play()

    def stop(self):
        self.audio.stop()


class Menu:
    def game_menu(self):
        global menu
        global estado
        pygame.init()
        #musicaMenu.play(-1)

        menu_inicio = Tela(screenWidth, screenHeight, "CapyGame", "resources/img/menu_iniciar.png")
        menu_scores = Tela(screenWidth, screenHeight, "CapyGame", "resources/img/menu_scores.png")

        #audio_menu_navigate = Audio("resources/sounds/menu_navigate_0.wav", 1)

        relogio_jogo = Relogio(60)

        fechar_jogo = False

        
        #menu = True
        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    fechar_jogo = True
                    menu = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        estado = "menu_scores"
                    elif event.key == pygame.K_UP:
                        estado = "menu_inicio"
                    elif event.key == 13:
                        menu = False

            if estado == "menu_inicio":
                menu_inicio.tela.blit(menu_inicio.imagemFundo, (0, 0))
            elif estado == "menu_scores":
                menu_scores.tela.blit(menu_scores.imagemFundo, (0, 0))

            #relogio_jogo.relogio.tick(relogio_jogo.fps)
            pygame.display.update()

            if fechar_jogo:
                return "fechar_jogo"
            else:
                return estado
                        

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self. width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.direction = "r"
        #self.standing = True

    def draw(self, win):
        #3 frames por image -> 27 para o exemplo
        frame = 3
        if self.walkCount + 1 >= 6:
            self.walkCount = 0

        #if not(self.standing):
        if self.left:
            self.direction = "l"
            win.blit(walkLeft[self.walkCount//frame], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            self.direction = "r"
            win.blit(walkRight[self.walkCount//frame], (self.x, self.y))
            self.walkCount += 1
        else:
            #if self.left:
            if self.direction == "l":
                win.blit(walkLeft[0], (self.x, self.y))
            #else:
            elif self.direction == "r":
                win.blit(walkRight[0], (self.x, self.y))        
        
class bullet(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        
class enemyMoving(object):
    walkRight = [pygame.image.load('resources/img/allig136pxr1.png'), pygame.image.load('resources/img/allig136pxr2.png')]
    walkLeft = [pygame.image.load('resources/img/allig136pxl1.png'), pygame.image.load('resources/img/allig136pxl2.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3

    def draw(self, win):
        self.move()
        frame = 3
        if self.walkCount + 1 >= 6:
            self.walkCount = 0
        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount // frame], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount // frame], (self.x, self.y))
            self.walkCount += 1

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0


def redrawGameWindow():
    win.blit(bg, (0,0))
    capy.draw(win)
    alligator.draw(win)
    #capy2.draw(win)
    for fruit in fruits:
        fruit.draw(win)
    pygame.display.update()

capy = player(50, 425, 64, 64)
alligator = enemyMoving(100, 410, 136, 136, 450)
fruits = []
#capy2 = player(90, 425, 64, 64)
while menu:
    menu_a = Menu()
    estado = menu_a.game_menu()
if estado == "fechar_jogo":
    gameExit = True
    
run = True
while run:
    #pygame.time.delay(20)
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for fruit in fruits:
        if fruit.x < 500 and fruit.x > 0:
            fruit.x += fruit.vel
        else:
            fruits.pop(fruits.index(fruit))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if capy.direction == "l":
            facing = -1
        else:
            facing = 1
            
        if len(fruits) < 5:
            fruits.append(bullet(round(capy.x + capy.width // 2), round(capy.y + capy.height // 2), 6, (0,0,0), facing))

    if keys[pygame.K_LEFT] and capy.x > capy.vel:
        capy.x -= capy.vel
        capy.left = True
        capy.right = False
        #capy.standing = False
    elif keys[pygame.K_RIGHT] and capy.x < screenWidth - capy.width - capy.vel:
        capy.x+= capy.vel
        capy.left = False
        capy.right = True
        #capy.standing = False
    else:
        capy.right = False
        capy.left = False
        #capy.standing = True
        capy.walkCount = 0
        
    if not(capy.isJump):
        #if keys[pygame.K_UP] and y > vel:
        #    y -= vel
        #if keys[pygame.K_DOWN] and y < 500 - height - vel:
        #    y += vel
        if keys[pygame.K_UP]:
            capy.isJump = True
            capy.right = False
            capy.left = False
            capy.walkCount = 0
    else:
        if capy.jumpCount >= -10:
            neg = 1
            if capy.jumpCount < 0:
                neg = -1
            capy.y -= (capy.jumpCount ** 2) * 0.5 * neg
            capy.jumpCount -= 1
        else:
            capy.isJump = False
            capy.jumpCount = 10
            
    redrawGameWindow()

    

pygame.quit()

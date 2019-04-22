import pygame, sys, random
pygame.init()

X = 1150
Y = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 155, 0)
GREY = (220, 220, 220)

menu = False
state_pag = "init_menu"

screen = pygame.display.set_mode((X, Y))
pygame.display.set_caption("CapyGame")
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT + 1, 10000)

bg = pygame.image.load('sprites/background.png')
init_menu = pygame.transform.scale(pygame.image.load("menu_iniciar.png"), (X, Y))
scores_menu = pygame.transform.scale(pygame.image.load("menu_scores.png"), (X, Y))
final_score = pygame.transform.scale(pygame.image.load("final_score.png"), (X, Y))
coinSound = pygame.mixer.Sound('sounds/coin.wav') #efeito sonoro do projetil
hitSound = pygame.mixer.Sound('sounds/hit.wav') #efeito sonoro do projetil batendo
# music = pygame.mixer.music.load('sounds/music.mp3') #musica de fundo
# pygame.mixer.music.play(-1) #roda a musica de fundo

joysticks = []
for i in range(0, pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()
    print("Detected joystick '", joysticks[-1].get_name(), "'")


class Platform():
    rects = []
    def __init__(self, sizex, sizey, posx, posy, color):
        self.surf = pygame.surface.Surface((sizex, sizey))
        self.rect = self.surf.get_rect(midbottom=(posx, posy))
        self.surf.fill(color)
        Platform.rects.append(self.rect)

    def draw(self):
        # box_plat = pygame.transform.scale(pygame.image.load("sprites/box.png"), (30, 30))
        # screen.blit(box_plat, (0, 0))
        screen.blit(self.surf, self.rect)

    def event(self):
        pass


class Player():
    def __init__(self):
        self.jump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.direction = 1
        self.capLeft = [pygame.transform.scale(pygame.image.load('sprites/capivara1left.png').convert_alpha(), (74, 48)),
                        pygame.transform.scale(pygame.image.load('sprites/capivara2left.png').convert_alpha(), (74, 48))]
        self.capRight = [pygame.transform.scale(pygame.image.load('sprites/capivara1right.png').convert_alpha(), (74, 48)),
                         pygame.transform.scale(pygame.image.load('sprites/capivara2right.png').convert_alpha(), (74, 48))]
        self.surf = pygame.transform.scale(pygame.image.load('sprites/capivara1left.png').convert_alpha(), (74, 48))
        self.rect = self.surf.get_rect(midbottom=(X//2, Y - 100))
        self.rect.height -= 3
        self.y_speed = 0

    def event(self):
        if self.jump:
            self.y_speed = -18
            self.jump = False

        if self.left and self.rect.left > 0:
            self.rect.centerx -= 5
        if self.right and self.rect.right < X:
            self.rect.centerx += 5

        self.rect.bottom += self.y_speed

        if self.on_ground():
            if self.y_speed >= 0:
                self.rect.bottom = Platform.rects[self.rect.collidelist(Platform.rects)].top + 1
                self.y_speed = 0
            else:
                self.rect.top = Platform.rects[self.rect.collidelist(Platform.rects)].bottom
                self.y_speed = 2
        else:
            self.y_speed += game.acc

    def on_ground(self):
        collision = self.rect.collidelist(Platform.rects)
        if collision > -1:
            return True
        else:
            return False

    def draw(self):
        if (self.walkCount+1) >= 6:
            self.walkCount = 0

        if (self.left):
            screen.blit(self.capLeft[self.walkCount//3], self.rect)
            self.walkCount += 1
            self.direction = -1
        elif (self.right):
            screen.blit(self.capRight[self.walkCount//3], self.rect)
            self.walkCount += 1
            self.direction = 1
        else:
            if (self.direction == 1):
                screen.blit(self.capRight[0], self.rect)
            elif (self.direction == -1):
                screen.blit(self.capLeft[0], self.rect)
        #screen.blit(self.surf, self.rect)


class Enemy():
    def __init__(self):
        self.walkCount = 0
        self.alligLeft = [pygame.transform.scale(pygame.image.load('sprites/alligator1left.png').convert_alpha(), (86, 40)),
                        pygame.transform.scale(pygame.image.load('sprites/alligator2left.png').convert_alpha(), (86, 40))]
        self.alligRight = [pygame.transform.scale(pygame.image.load('sprites/alligator1right.png').convert_alpha(), (86, 40)),
                         pygame.transform.scale(pygame.image.load('sprites/alligator2right.png').convert_alpha(), (86, 40))]

        self.surf = pygame.transform.scale(pygame.image.load('sprites/alligator1right.png').convert_alpha(), (86, 40))
        self.rect = self.surf.get_rect(midtop=(X//2, 0))
        self.rect.height -= 13
        self.x_speed = random.randint(3, 7)
        self.y_speed = 0

    def event(self):
        self.rect.centerx += self.x_speed
        if self.rect.left <= 0 or self.rect.right >= X:
            self.x_speed *= -1

        if self.on_ground():
            self.rect.bottom = Platform.rects[self.rect.collidelist(Platform.rects)].top + 1
            self.y_speed = 0
        else:
            self.y_speed += game.acc

        self.rect.bottom += self.y_speed
        self.hit()

        if game.timer:
            game.timer = False
            self.rect.midtop = (X//2, 0)
            self.x_speed = random.randint(3, 7) * ((self.x_speed > 0) - (self.x_speed < 0))

    def on_ground(self):
        collision = self.rect.collidelist(Platform.rects)
        if collision > -1:
            return True
        else:
            return False

    def hit(self):
        if (game.player.rect.colliderect(self.rect) and
            game.player.rect.midbottom != (X//2, Y - 99)):
            game.lives -= 1
            game.player.rect.midbottom = (X//2, Y - 99)
            hitSound.play()

    def draw(self):
        self.walkCount += 1
        if (self.walkCount+1) >= 6:
            self.walkCount = 0

        if (self.x_speed < 0):
            screen.blit(self.alligLeft[self.walkCount//3], self.rect)
            #self.walkCount += 1
            self.direction = -1
        elif (self.x_speed > 0):
            screen.blit(self.alligRight[self.walkCount//3], self.rect)
            #self.walkCount += 1
            self.direction = 1

        #screen.blit(self.surf, self.rect)


class Coin():
    def __init__(self):
        self.positions = [(600, 245), (250, 325), (40, 500), (850, 500), (830, 245), (800, 325)]
        self.surf = pygame.transform.scale(pygame.image.load('sprites/orange.png').convert_alpha(), (25, 25))

        self.rect = self.surf.get_rect(midbottom=random.choice(self.positions))
        self.count = 0

    def event(self):
        if game.player.rect.colliderect(self.rect):
            self.rect.midbottom = random.choice(self.positions)
            game.coin_count += 1
            coinSound.play()
        elif game.enemy.rect.colliderect(self.rect):
            self.rect.midbottom = random.choice(self.positions)

    def draw(self):
        screen.blit(self.surf, self.rect)


class Game():
    def __init__(self):
        self.levels = [self.level_1, self.level_2, self.level_3]
        self.heart_surf = pygame.transform.scale(pygame.image.load('sprites/heart.png').convert_alpha(), (23, 20))
        self.coin_surf = pygame.transform.scale(pygame.image.load('sprites/key.png').convert_alpha(), (20, 20))
        self.acc = 2
        self.timer = False
        self.level = 0
        self.state = self.startpage

    def init(self):
        """
    A game state function.
    Called at the start of a new level.
"""
        self.lives = 5
        self.coin_count = 0
        self.sprites = [self]
        self.levels[self.level]()
        self.state = self.loop

    def level_1(self):
        self.player = Player()
        self.sprites.append(self.player)
        self.enemy = Enemy()
        self.sprites.append(self.enemy)
        self.coin = Coin()
        self.sprites.append(self.coin)

        self.sprites.append(Platform(X, 100, X//2, Y, GREEN))
        self.sprites.append(Platform(200, 15, 500, Y-180, BLUE))
        self.sprites.append(Platform(300, 15, 200, 340, BLUE))
        self.sprites.append(Platform(250, 15, 480, 260, BLUE))
        self.sprites.append(Platform(300, 15, 150, 180, BLUE))
        self.sprites.append(Platform(300, 15, 500, 100, BLUE))
        self.sprites.append(Platform(80, 15, 830, 260, BLUE))
        self.sprites.append(Platform(80, 15, 800, 340, BLUE))

    def level_2(self):
        print("LEVEL 2")
        self.level_1()  # level 1 used as dummy

    def level_3(self):
        print("LEVEL 3")
        self.level_1()  # level 1 used as dummy

    def event(self):
        " a game state function "
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0 and self.player.on_ground():
                    self.player.jump = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.player.on_ground():
                    self.player.jump = True
            elif event.type == pygame.USEREVENT + 1:
                self.timer = True

        self.player.left = False
        self.player.right = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.left = True
        if keys[pygame.K_RIGHT]:
            self.player.right = True

        for i in range(0, pygame.joystick.get_count()):
            if pygame.joystick.Joystick(i).get_axis(0) < -0.8:
                self.player.left = True
            if pygame.joystick.Joystick(i).get_axis(0) > 0.8:
                self.player.right = True

    def draw(self):
        for i in range(self.lives):
            screen.blit(self.heart_surf, [i*25 + 20, 20])
        for i in range(self.coin_count):
            screen.blit(self.coin_surf, [850 - i*20, 20])

    def loop(self):
        " a game state function "
        clock.tick(30)
        screen.blit(bg, (0, 0))

        for s in self.sprites:
            s.event()
        for s in self.sprites:
            s.draw()
        pygame.display.flip()

        if self.lives == 0:
            self.state = self.play_again
        if self.coin_count == 10:
            self.level += 1
            self.state = self.init

    def play_again(self):
        " a game state function "

        # opção de selecionar no teclado e não só no mouse
        play = screen.blit(pygame.image.load("sprites/btn_playmore.png"), ((X-500)//3, Y//8*5))
        stop = screen.blit(pygame.image.load("sprites/btn_stopplay.png"), ((X-300)//3*2+100, Y//8*5))
        
        pygame.display.flip()
        self.buttons = [(play, self.init), (stop, self.endpage)]
        self.state = self.mouse_click

    def mouse_click(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = self.end
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed() == (1, 0, 0):
                    pos = pygame.mouse.get_pos()
                    for btn, action in self.buttons:
                        if btn.collidepoint(pos):
                            self.state = action
                            return
            pygame.time.wait(20)

    def end(self):
        pygame.quit()
        sys.exit()

    def startpage(self):
        " a game state function "
        # screen.fill(GREEN)
        # font = pygame.font.SysFont("Segoe Print", 30)
        # txt_surf = font.render("CapyGame", 1, BLUE)
        # txt_rect = txt_surf.get_rect(center=(X//2, Y//2))
        # screen.blit(txt_surf, txt_rect)
        # play = button("Play Now", BLACK, ((X-100)//2, Y//8*5))
        # self.buttons = [(play, self.init)]
        # pygame.display.flip()
        # self.state = self.mouse_click

        menu = True
        state_pag = "menu_init"

        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    menu = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        state_pag = "menu_scores"
                    elif event.key == pygame.K_UP:
                        state_pag = "menu_init"
                    elif event.key == 13:
                        menu = False

            if state_pag == "menu_init":
                screen.blit(init_menu, (0, 0))
            elif state_pag == "menu_scores":
                screen.blit(scores_menu, (0, 0))

            pygame.display.update()
        
        if menu == False and state_pag == "menu_init":
            self.init()
        elif menu == False and state_pag == "menu_scores":
            pass

    def endpage(self):
        " a game state function "
        screen.blit(final_score, (0, 0))
        font = pygame.font.SysFont("Segoe Print", 140)
        txt_surf = font.render("330", 1, WHITE)
        txt_rect = txt_surf.get_rect(center=(X//2, Y//3 + 20))
        screen.blit(txt_surf, txt_rect)

        # stop = button("Exit", BLACK, ((X-100)//2, Y//8*5))
        stop = screen.blit(pygame.image.load("sprites/btn_exit.png"), ((X-205)//2, Y//8*5))
        
        self.buttons = [(stop, self.end)]
        pygame.display.flip()

        self.state = self.mouse_click


def button(txt, color, pos):
    button_font = pygame.font.SysFont("Segoe Print", 16)
    btn_surf = pygame.Surface((100, 40))
    btn_rect = btn_surf.get_rect(topleft=(pos))
    btn_surf.fill(GREY)
    pygame.draw.rect(btn_surf, BLACK, (0, 0, 100, 40), 1)
    txt_surf = button_font.render(txt, 1, color)
    txt_rect = txt_surf.get_rect(center=(50,20))
    btn_surf.blit(txt_surf, txt_rect)
    screen.blit(btn_surf, btn_rect)
    return btn_rect


game = Game()

while True:
    game.state()

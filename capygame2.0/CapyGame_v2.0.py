import pygame, sys, random
from os import path
pygame.init()

X = 1150
Y = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (220, 215, 0)
GREY = (220, 220, 220)

HS_FILE = "highscore.txt"
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
box_plat = pygame.transform.scale(pygame.image.load("sprites/box.png"), (30, 30))
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
    def __init__(self, sizex, sizey, posx, posy, color, qtd):
        self.qtd = qtd
        self.posx = posx
        self.posy = posy
        self.surf = pygame.surface.Surface((sizex, sizey))
        self.rect = self.surf.get_rect(midbottom=(posx, posy))
        self.surf.fill(color)
        Platform.rects.append(self.rect)

    def draw(self):
        screen.blit(self.surf, self.rect)
        for i in range(self.qtd):
            screen.blit(box_plat, [self.posx - 15*self.qtd + 30*i, self.posy - 30])       

    def event(self):
        pass


class Player():
    def __init__(self):
        self.jump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.direction = 1
        self.capLeft = [pygame.transform.scale(pygame.image.load('sprites/capivara1left.png').convert_alpha(), (51, 42)),
                        pygame.transform.scale(pygame.image.load('sprites/capivara2left.png').convert_alpha(), (51, 42))]
        self.capRight = [pygame.transform.scale(pygame.image.load('sprites/capivara1right.png').convert_alpha(), (51, 42)),
                         pygame.transform.scale(pygame.image.load('sprites/capivara2right.png').convert_alpha(), (51, 42))]
        self.surf = pygame.transform.scale(pygame.image.load('sprites/capivara1left.png').convert_alpha(), (51, 42))
        self.rect = self.surf.get_rect(midbottom=(X//2, Y - 100))
        self.rect.height -= 1
        self.y_speed = 0

    def event(self):
        if self.jump:
            self.y_speed = -25
            self.jump = False

        if self.left and self.rect.left > 0:
            self.rect.centerx -= 12
        if self.right and self.rect.right < X:
            self.rect.centerx += 12

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
        self.rect.width -= 22
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
        if (game.player.rect.colliderect(self.rect) and game.player.rect.midbottom != (X//2, Y - 99)):
            game.lives -= 1
            game.score -= 15
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
        # self.positions = [(580, Y - 100), (250, Y - 100), (420, Y - 100), (830, Y - 100), (800, Y - 100)]
        self.positions1 = [(580, 230), (250, 310), (420, 150), (830, 230), (800, 310), (1010, 70)]
        self.positions2 = [(X - 15, 210), (15, 210), (530, 210), (45, 70), (X - 45, 70)]
        self.positions3 = [(15, 150), (X - 15, 150), (45, 270), (X - 45, 270), (505, 270), (15, Y - 210), (X - 45, Y - 210)]
        self.surf = pygame.transform.scale(pygame.image.load('sprites/orange.png').convert_alpha(), (25, 25))

        self.rect1 = self.surf.get_rect(midbottom=random.choice(self.positions1))
        self.rect2 = self.surf.get_rect(midbottom=random.choice(self.positions2))
        self.rect3 = self.surf.get_rect(midbottom=random.choice(self.positions3))
        self.count = 0

    def event(self):
        if (game.level == 0):
            if game.player.rect.colliderect(self.rect1):
                self.rect1.midbottom = random.choice(self.positions1)
                game.coin_count += 1
                game.score += 5
                coinSound.play()
            elif game.enemy.rect.colliderect(self.rect1):
                self.rect1.midbottom = random.choice(self.positions1)
        elif (game.level == 1):
            if game.player.rect.colliderect(self.rect2):
                self.rect2.midbottom = random.choice(self.positions2)
                game.coin_count += 1
                game.score += 5
                coinSound.play()
            elif game.enemy.rect.colliderect(self.rect2):
                self.rect2.midbottom = random.choice(self.positions2)
        elif (game.level == 2):
            if game.player.rect.colliderect(self.rect3):
                self.rect3.midbottom = random.choice(self.positions3)
                game.coin_count += 1
                game.score += 5
                coinSound.play()
            elif game.enemy.rect.colliderect(self.rect3):
                self.rect3.midbottom = random.choice(self.positions3)

    def draw(self):
        if (game.level == 0):
            screen.blit(self.surf, self.rect1)
        elif (game.level == 1):
            screen.blit(self.surf, self.rect2)
        elif (game.level == 2):
            screen.blit(self.surf, self.rect3)


class Game():
    def __init__(self):
        self.levels = [self.level_1, self.level_2, self.level_3, self.play_again]
        self.heart_surf = pygame.transform.scale(pygame.image.load('sprites/heart.png').convert_alpha(), (23, 20))
        self.coin_surf = pygame.transform.scale(pygame.image.load('sprites/pineapple.png').convert_alpha(), (25, 40))
        self.acc = 3
        self.timer = False
        self.level = 0
        self.state = self.startpage
        self.load_data()

    def load_data(self):
        #load highscore
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
            
    def init(self):
        """
    A game state function.
    Called at the start of a new level.
"""
        self.lives = 3
        self.coin_count = 0
        self.score = 0
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

        self.sprites.append(Platform(X, 100, X//2, Y, GREEN, 0))

        # para adicionar - prim. atributo = 30*ultimo atributo
        self.sprites.append(Platform(210, 30, 500, Y-180, RED, 7))
        self.sprites.append(Platform(300, 30, 200, 340, RED, 10))
        self.sprites.append(Platform(240, 30, 480, 260, RED, 8))
        self.sprites.append(Platform(300, 30, 300, 180, RED, 10))
        self.sprites.append(Platform(300, 30, 500, 100, RED, 10))
        self.sprites.append(Platform(180, 30, 860, 260, RED, 6))
        self.sprites.append(Platform(210, 30, 800, 340, RED, 7))

        self.sprites.append(Platform(90, 30, 1010, 100, RED, 3))
        self.sprites.append(Platform(90, 30, 1050, 180, RED, 3))
        

    def level_2(self):
        print("LEVEL 2")
        self.player = Player()
        self.sprites.append(self.player)
        self.enemy = Enemy()
        self.sprites.append(self.enemy)
        self.coin = Coin()
        self.sprites.append(self.coin)

        self.sprites.append(Platform(X, 100, X // 2, Y, GREEN, 0))

        # para adicionar - prim. atributo = 30*ultimo atributo
        self.sprites.append(Platform(120, 30, 60, Y - 180, RED, 4))
        self.sprites.append(Platform(150, 30, 75, 240, RED, 5))
        #self.sprites.append(Platform(60, 30, 0, 260, RED, 2))
        self.sprites.append(Platform(120, 30, 60, 100, RED, 4))

        self.sprites.append(Platform(30, 30, 330, 340, RED, 1))
        self.sprites.append(Platform(30, 30, 330, 180, RED, 1))

        self.sprites.append(Platform(30, 30, 530, 240, RED, 1))

        self.sprites.append(Platform(30, 30, 840, 140, RED, 1))
        self.sprites.append(Platform(30, 30, 800, 350, RED, 1))

        self.sprites.append(Platform(120, 30, X - 60, Y - 180, RED, 4))
        self.sprites.append(Platform(150, 30, X - 75, 240, RED, 5))
        # self.sprites.append(Platform(60, 30, 0, 260, RED, 2))
        self.sprites.append(Platform(90, 30, X - 45, 100, RED, 3))

    def level_3(self):
        print("LEVEL 3")
        self.player = Player()
        self.sprites.append(self.player)
        self.enemy = Enemy()
        self.sprites.append(self.enemy)
        self.coin = Coin()
        self.sprites.append(self.coin)

        self.sprites.append(Platform(X, 100, X // 2, Y, GREEN, 0))

        # para adicionar - prim. atributo = 30*ultimo atributo
        self.sprites.append(Platform(900, 30, 450, Y - 180, RED, 30))
        self.sprites.append(Platform(60, 30, 30, 300, RED, 2))
        self.sprites.append(Platform(1020, 30, 510, 180, RED, 34))

        self.sprites.append(Platform(150, 30, X - 75, Y - 180, RED, 5))
        self.sprites.append(Platform(990, 30, X - 495, 300, RED, 33))
        self.sprites.append(Platform(30, 30, X - 15, 180, RED, 1))


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
        score_cont = pygame.transform.scale(pygame.image.load("sprites/cont_score.png"), (110, 30))
        screen.blit(score_cont, (X - 200, 20))
        font = pygame.font.SysFont("Segoe Print", 40)
        txt_surf = font.render(str(game.score), 1, BLACK)
        txt_rect = txt_surf.get_rect(center=(X - 70, 35))
        screen.blit(txt_surf, txt_rect)

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

        if self.lives == 0 or self.level == 3:
            self.state = self.play_again
        if self.coin_count == 5:
            Platform.rects.clear()
            self.sprites.clear()
            self.level += 1
            self.state = self.init

    def play_again(self):
        " a game state function "
        self.btn_option = True
        self.btn_state = "play_selected"        

        # play = screen.blit(pygame.image.load("sprites/btn_playmore.png"), ((X-500)//3, Y//8*5))
        # stop = screen.blit(pygame.image.load("sprites/btn_stopplay.png"), ((X-300)//3*2+100, Y//8*5))
        # play_selected = screen.blit(pygame.image.load("sprites/btn_playmore_s.png"), ((X-500)//3, Y//8*5))
        # stop_selected = screen.blit(pygame.image.load("sprites/btn_stopplay_s.png"), ((X-300)//3*2+100, Y//8*5))
        
        # pygame.display.flip()
        # self.buttons = [(play, self.init), (stop, self.endpage)]
        # self.state = self.mouse_click

        play = pygame.image.load("sprites/btn_playmore.png")
        stop = pygame.image.load("sprites/btn_stopplay.png")
        play_selected = pygame.image.load("sprites/btn_playmore_s.png")
        stop_selected = pygame.image.load("sprites/btn_stopplay_s.png")

        while self.btn_option:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    self.btn_option = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.btn_state = "stop_selected"
                    elif event.key == pygame.K_LEFT:
                        self.btn_state = "play_selected"
                    elif event.key == 13:
                        self.btn_option = False

            if self.btn_state == "stop_selected":
                screen.blit(play, ((X-500)//3, Y//8*5))
                screen.blit(stop_selected, ((X-300)//3*2+100, Y//8*5))
            elif self.btn_state == "play_selected":
                screen.blit(play_selected, ((X-500)//3, Y//8*5))
                screen.blit(stop, ((X-300)//3*2+100, Y//8*5))

            pygame.display.update()
        
        if self.btn_option == False and self.btn_state == "play_selected":
            self.init()
        elif self.btn_option == False and self.btn_state == "stop_selected":
            self.endpage()
             

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
                    # if event.key == pygame.K_DOWN:
                    #     state_pag = "menu_scores"
                    # elif event.key == pygame.K_UP:
                    #     state_pag = "menu_init"
                    if event.key == 13:
                        menu = False

            if state_pag == "menu_init":
                screen.blit(init_menu, (0, 0))
            # elif state_pag == "menu_scores":
            #     screen.blit(scores_menu, (0, 0))

            pygame.display.update()
        
        if menu == False and state_pag == "menu_init":
            self.init()
        elif menu == False and state_pag == "menu_scores":
            pass

    def endpage(self):
        " a game state function "
        screen.blit(final_score, (0, 0))

        if self.highscore == 0:
            if game.score < 0:
                self.highscore = game.score
        
        if game.score > self.highscore:
            self.highscore = game.score
            font = pygame.font.SysFont("Segoe Print", 140)
            txt_surf = font.render(str(game.score), 1, WHITE)
            txt_rect = txt_surf.get_rect(center=(X//2, Y//3 + 10))
            screen.blit(txt_surf, txt_rect)
            screen.blit(pygame.image.load("sprites/new_hscore.png"), ((X - 290)//2, Y//8*5 - 60))
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(game.score))
            
        else:
            screen.blit(pygame.image.load("sprites/highscore.png"), ((X - 500)//2, Y//8*5 - 100))
            font1 = pygame.font.SysFont("Segoe Print", 140)
            txt_surf1 = font1.render(str(game.score), 1, WHITE)
            txt_rect1 = txt_surf1.get_rect(center=(X//2, Y//3 + 10))
            screen.blit(txt_surf1, txt_rect1)

            font2 = pygame.font.SysFont("Segoe Print", 100)
            txt_surf2 = font2.render(str(self.highscore), 1, WHITE)
            txt_rect2 = txt_surf2.get_rect(center=(X//2, Y//3 + 180))
            screen.blit(txt_surf2, txt_rect2)

        # stop = button("Exit", BLACK, ((X-100)//2, Y//8*5))

        stop = pygame.image.load("sprites/btn_exit.png")
        screen.blit(stop, (50, Y//8*5 + 100))
        # stop = screen.blit(pygame.image.load("sprites/btn_exit.png"), (50, Y//8*5 + 100))
        
        self.buttons = [(stop, self.end)]
        pygame.display.flip()

        self.btn_exit_select = True
        while self.btn_exit_select:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    pygame.quit()
                    sys.exit()
                    self.btn_exit_select = False


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

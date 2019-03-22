import pygame  # importa a bibilioteca pygame
import players
import enemies
import sprites

pygame.init()  # inicia apropriadamente o pygame
screenWidth = 852
screenHeight = 480
win = pygame.display.set_mode((screenWidth, screenHeight)) #cria uma janela com determinadas dimensões
pygame.display.set_caption("First Game") #fornece um titulo para a janela

bulletSound = pygame.mixer.Sound('sounds/bullet.wav')
hitSound = pygame.mixer.Sound('sounds/hit.wav')

music = pygame.mixer.music.load('sounds/music.mp3')
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()

def redrawGameWindow():
    win.blit(sprites.bg, (0, 0))
    text = font.render('Score: ' + str(man.score), 1, (0, 0, 0))
    win.blit(text, (390, 10))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()  #atualiza a janela

#main loop
font = pygame.font.SysFont('comicsans', 30, True)
man = players.player(20, 480-64, 64, 64)
goblin = enemies.enemy(50, 480-64, 64, 64, 200)
shootLoop = 0
bullets = []
run = True

while run: #verifica constantemente mudanças de entrada e atualiza a janela
    clock.tick(27) #FPS

    if goblin.visible:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2] and man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0]:
                man.hit(win, screenWidth, screenHeight)
                man.score -= 5

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if goblin.visible:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2] and bullet.x + bullet.radius > goblin.hitbox[0]:
                    goblin.hit(win, screenWidth, screenHeight)
                    hitSound.play()
                    man.score += 1
                    bullets.pop(bullets.index(bullet))
        if bullet.x < screenWidth and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed() #verifica por teclas pressionadas
    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 25:
            bullets.append(players.projectile(round(man.x + (man.width//2)), round(man.y + (man.height//2)), 6, (0, 0, 0), facing))
        shootLoop = 1
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < (screenWidth - man.width - man.vel):
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
    if not (man.isJump): #se o objeto esta pulando, nao pode pular e nem mover para cima nem para baixo ate acabar o pulo
        if keys[pygame.K_UP]:
            man.isJump = True
            man.left = False
            man.right = False
            man.walkCount = 0
    else: #implementa o mecanismo do pulo
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()

pygame.quit
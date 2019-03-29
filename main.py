import pygame  #importa a bibilioteca pygame
import players
import enemies
import platforms
import sprites

pygame.init()  #inicia apropriadamente o pygame
screenWidth = 1250
screenHeight = 580
win = pygame.display.set_mode((screenWidth, screenHeight)) #cria uma janela com determinadas dimensões
pygame.display.set_caption("First Game") #fornece um titulo para a janela

bulletSound = pygame.mixer.Sound('sounds/bullet.wav') #efeito sonoro do projetil
hitSound = pygame.mixer.Sound('sounds/hit.wav') #efeito sonoro do projetil batendo
music = pygame.mixer.music.load('sounds/music.mp3') #musica de fundo
pygame.mixer.music.play(-1) #roda a musica de fundo

clock = pygame.time.Clock() #seta uma variavel para ajustar o clock do game

#Funcao para atuazilzar todas as classes na tela
def redrawGameWindow():
    win.blit(sprites.bg, (0, 0)) #posicao do background na tela
    text = font.render('Score: ' + str(man.score), 1, (0, 0, 0)) #mostra o score na tela
    win.blit(text, (390, 10)) #posicao do score na tela
    man.draw(win) #atualiza o player na tela
    goblin.draw(win) #atualiza o inimigo na tela
    for bullet in bullets:
        bullet.draw(win) #atualiza os projeteis na tela
    stage1.draw(win, screenWidth, screenHeight)
    pygame.display.update()  #atualiza a janela

font = pygame.font.SysFont('comicsans', 30, True) #escolha a fonte de texto
man = players.player(20, screenHeight-64-20, 64, 64) #inicia o objeto player
goblin = enemies.enemy(50, screenHeight-64-3, 64, 64, 200) #inicia o objeto inimigo
shootLoop = 0 #coloca um delay entre o disparo de dois projeteis
bullets = [] #vetor que ira armazenas os projeteis
run = True

stage1 = platforms.stage_platforms(0, 0, 1)

#Main loop
while run:
    clock.tick(27) #FPS

    #Verifica se o inimigo esta vivo ou nao
    if goblin.visible:
        #Implementa a colisao entre o player e o inimigo
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2] and man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0]:
                man.hit(win, screenWidth, screenHeight)
                man.score -= 5

    #Se um projetil tiver sido disparado, incrementa a cada main loop; quando chega a 3, pode realizar novo disparo
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    #Verifica se o usuario fecha o game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #Implementa a colisao dos projeteis com o inimigo
    for bullet in bullets:
        if goblin.visible:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2] and bullet.x + bullet.radius > goblin.hitbox[0]:
                    goblin.hit(win, screenWidth, screenHeight) #retira vida ou mata o inimigo
                    hitSound.play()
                    man.score += 1
                    bullets.pop(bullets.index(bullet)) #retira o projetil que colidiu da tela
        #Verifica se o projetil saiu da tela
        if bullet.x < screenWidth and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed() #verifica por teclas pressionadas
    if keys[pygame.K_SPACE] and shootLoop == 0: #tecla espaço para disparar o projetil
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 25: #numero maximo de projeteis que podem aparecer na tela
            bullets.append(players.projectile(round(man.x + (man.width//2)), round(man.y + (man.height//2)), 6, (0, 0, 0), facing))
        shootLoop = 1
    if keys[pygame.K_LEFT] and man.x > man.vel: #seta para esquerda
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < (screenWidth - man.width - man.vel): #seta para direita
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
    if not (man.isJump): #se o objeto esta pulando, nao pode pular e nem mover para cima nem para baixo ate acabar o pulo
        if keys[pygame.K_UP]: #seta para cima para pular
            man.isJump = True
            man.left = False
            man.right = False
            man.walkCount = 0
    #Implementa o mecanismo do pulo
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg #funciona como a gravidade
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()

pygame.quit #finaliza o jogo
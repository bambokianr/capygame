import pygame
pygame.init()

screenWidth = 1270
screenHeight = 630

win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Sprites Capy")

walkRight = [pygame.image.load('resources/img/capy64pxr1.png'), pygame.image.load('resources/img/capy64pxr2.png')]
walkLeft = [pygame.image.load('resources/img/capy64pxl1.png'), pygame.image.load('resources/img/capy64pxl2.png')]

bg = pygame.image.load('resources/img/background.png')

clock = pygame.time.Clock()

x = 50
y = 425
width = 64
height = 64
vel = 5

isJump = False
jumpCount = 10

#para montar os sprites
left = False
right = False
walkCount = 0
direction = "r"

def redrawGameWindow():
    global walkCount
    global direction
    win.blit(bg, (0,0))
    #win.fill((0,0,0))
    #pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    #3 frames por image -> 27 para o exemplo
    frame = 3
    if walkCount + 1 >= 6:
        walkCount = 0
    if left:
        direction = "l"
        win.blit(walkLeft[walkCount//frame], (x, y))
        walkCount += 1
    elif right:
        direction = "r"
        win.blit(walkRight[walkCount//frame], (x, y))
        walkCount += 1
    else:
        if direction == "l":
            win.blit(walkLeft[0], (x, y))
        elif direction == "r":
            win.blit(walkRight[0], (x, y))
    
    pygame.display.update()
    
run = True
while run:
    #pygame.time.delay(20)
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and x < screenWidth - width - vel:
        x+= vel
        left = False
        right = True
    else:
        right = False
        left = False
        walkCount = 0
        
    if not(isJump):
        #if keys[pygame.K_UP] and y > vel:
        #    y -= vel
        #if keys[pygame.K_DOWN] and y < 500 - height - vel:
        #    y += vel
        if keys[pygame.K_SPACE]:
            isJump = True
            right = False
            left = False
            walkCount = 0
    else:
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= (jumpCount ** 2) * 0.5 * neg
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10
            
    redrawGameWindow()

    


pygame.quit()

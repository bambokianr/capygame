import pygame

#Importa os sprites do player
walkLeftP = [pygame.image.load('sprites/capivara1left.png'), pygame.image.load('sprites/capivara2left.png')]
walkRightP = [pygame.image.load('sprites/capivara1right.png'), pygame.image.load('sprites/capivara2right.png')]
#Redimensiona os sprites do player
walkLeftP = [pygame.transform.scale(walkLeftP[0], (78, 64)), pygame.transform.scale(walkLeftP[1], (78, 64))]
walkRightP = [pygame.transform.scale(walkRightP[0], (78, 64)), pygame.transform.scale(walkRightP[1], (78, 64))]

#Importa os sprites do inimigo
walkLeftE = [pygame.image.load('sprites/alligator1left.png'), pygame.image.load('sprites/alligator2left.png')]
walkRightE = [pygame.image.load('sprites/alligator1right.png'), pygame.image.load('sprites/alligator2right.png')]
#Redimensiona os sprites do inimigo
walkLeftE = [pygame.transform.scale(walkLeftE[0], (138, 64)), pygame.transform.scale(walkLeftE[1], (138, 64))]
walkRightE = [pygame.transform.scale(walkRightE[0], (138, 64)), pygame.transform.scale(walkRightE[1], (138, 64))]

#Importa o sprite da plataforma
spritePlat = [pygame.image.load('sprites/box1.png'), pygame.image.load('sprites/box2.png'), pygame.image.load('sprites/box3.png'), pygame.image.load('sprites/box4.png')]
#Redimensiona os sprites do inimigo
spritePlat = [pygame.transform.scale(spritePlat[0], (32, 30)), pygame.transform.scale(spritePlat[1], (64, 30)), pygame.transform.scale(spritePlat[2], (96, 30)), pygame.transform.scale(spritePlat[3], (128, 30))]

#Importa os sprites do player
chickLeft = [pygame.image.load('sprites/chickenL1.png'), pygame.image.load('sprites/chickenL2.png')]
chickRight = [pygame.image.load('sprites/chickenR1.png'), pygame.image.load('sprites/chickenR2.png')]
#Redimensiona os sprites do player
chickLeft = [pygame.transform.scale(chickLeft[0], (50, 50))]
chickRight = [pygame.transform.scale(chickRight[0], (50, 50))]

#Importa os sprites do inimigo
#walkLeftE = [pygame.image.load('sprites/L1E.png'), pygame.image.load('sprites/L2E.png'), pygame.image.load('sprites/L3E.png'),
#             pygame.image.load('sprites/L4E.png'), pygame.image.load('sprites/L5E.png'), pygame.image.load('sprites/L6E.png'),
#             pygame.image.load('sprites/L7E.png'), pygame.image.load('sprites/L8E.png'), pygame.image.load('sprites/L9E.png'),
#             pygame.image.load('sprites/L10E.png'), pygame.image.load('sprites/L11E.png')]
#walkRightE = [pygame.image.load('sprites/R1E.png'), pygame.image.load('sprites/R2E.png'), pygame.image.load('sprites/R3E.png'),
#              pygame.image.load('sprites/R4E.png'), pygame.image.load('sprites/R5E.png'), pygame.image.load('sprites/R6E.png'),
#              pygame.image.load('sprites/R7E.png'), pygame.image.load('sprites/R8E.png'), pygame.image.load('sprites/R9E.png'),
#              pygame.image.load('sprites/R10E.png'), pygame.image.load('sprites/R11E.png')]

#Importa o sprite do background
bg = pygame.image.load('sprites/background.png')





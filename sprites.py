import pygame

walkLeftP = [pygame.image.load('sprites/capivara1left.png'), pygame.image.load('sprites/capivara2left.png')]
walkRightP = [pygame.image.load('sprites/capivara1right.png'), pygame.image.load('sprites/capivara2right.png')]
walkLeftP = [pygame.transform.scale(walkLeftP[0], (78, 64)), pygame.transform.scale(walkLeftP[1], (78, 64))]
walkRightP = [pygame.transform.scale(walkRightP[0], (78, 64)), pygame.transform.scale(walkRightP[1], (78, 64))]

walkLeftE = [pygame.image.load('sprites/L1E.png'), pygame.image.load('sprites/L2E.png'), pygame.image.load('sprites/L3E.png'),
             pygame.image.load('sprites/L4E.png'), pygame.image.load('sprites/L5E.png'), pygame.image.load('sprites/L6E.png'),
             pygame.image.load('sprites/L7E.png'), pygame.image.load('sprites/L8E.png'), pygame.image.load('sprites/L9E.png'),
             pygame.image.load('sprites/L10E.png'), pygame.image.load('sprites/L11E.png')]
walkRightE = [pygame.image.load('sprites/R1E.png'), pygame.image.load('sprites/R2E.png'), pygame.image.load('sprites/R3E.png'),
              pygame.image.load('sprites/R4E.png'), pygame.image.load('sprites/R5E.png'), pygame.image.load('sprites/R6E.png'),
              pygame.image.load('sprites/R7E.png'), pygame.image.load('sprites/R8E.png'), pygame.image.load('sprites/R9E.png'),
              pygame.image.load('sprites/R10E.png'), pygame.image.load('sprites/R11E.png')]

bg = pygame.image.load('sprites/background.png')




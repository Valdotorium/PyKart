def more(screen):
    import pygame, os, sys
    pygame.draw.rect(screen, (255, 0, 0), (50, 50, 100, 100))
    pygame.draw.rect(screen, (0, 255, 0), (150, 50, 100, 100))
    pygame.draw.rect(screen, (0, 0, 255), (250, 50, 100, 100))
    pygame.draw.rect(screen, (255, 255, 0), (350, 50, 100, 100))
    pygame.draw.rect(screen, (255, 0, 255), (450, 50, 100, 100))
    #blit grass
    print("current path"+ os.path.dirname(__file__))
    grass = pygame.image.load(os.path.dirname(__file__)+"/textures/grass.png")
    screen.blit(grass, (50, 50))
    pygame.display.update()
    

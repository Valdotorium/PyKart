import pygame, os, sys
import ext
import time
#load files in othe directories like this: os.path.dirname(__file__) + "/folder/folder/file.png"
#put scripts into top-level directory, put images or other "universal files" into _internal in dist/main
#create a window in fullscreen size with a rectangle in it
pygame.init()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Project Exoplanet")
#place a red rectangle in it
pygame.draw.rect(screen, (255, 0, 0), (50, 50, 100, 100))
#display the window
pygame.display.update()
time.sleep(1)
#main loop
running = True
ext.more(screen)
pygame.display.update()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

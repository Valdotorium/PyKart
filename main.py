import pygame, os, sys
import time
import res.load
#load files in othe directories like this: os.path.dirname(__file__) + "/folder/folder/file.png"
#put scripts into top-level directory, put images or other "universal files" into _internal in dist/main
#create a window in fullscreen size with a rectangle in it
#load file template:     grass = pygame.image.load(os.path.dirname(__file__)+"/textures/grass.png")
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("Project Exoplanet")
#main loop
running = True
pygame.display.update()
fps = 30
inputvalues = []
class Game():
    def __init__(self):
        #game stuff
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.fps = fps
        #loading the font files
        self.font = "textures/FONTS/PixelOperator.ttf"
        self.boldfont = "textures/FONTS/PixelOperator-Bold.ttf"
        self.largefont = "textures/FONTS/PixelOperator.ttf"
        self.largeboldfont = "textures/FONTS/PixelOperator-Bold.ttf"
        #initializing the font
        self.font = pygame.font.Font(self.font, 16)
        self.boldfont = pygame.font.Font(self.boldfont, 16)
        self.largefont = pygame.font.Font(self.largefont, 32)
        self.largeboldfont = pygame.font.Font(self.largeboldfont, 32)
        #dev options
        self.CFG_extensive_logs = True
        self.CFG_visuals = True
        self.CFG_debug_mode = True
        self.CFG_limit_refresh_access = False
        

    def run(self):
            pass
Exo = Game()
screen.fill((100,100,100))
time.sleep(1)
res.load.respond(Exo)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        Exo.run()
        pygame.display.update()
        time.sleep(1/fps)


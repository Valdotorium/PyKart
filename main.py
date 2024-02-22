import pygame, os, sys
import time
#load files in othe directories like this: os.path.dirname(__file__) + "/folder/folder/file.png"
#put scripts into top-level directory, put images or other "universal files" into _internal in dist/main
#create a window in fullscreen size with a rectangle in it
#load file template:     grass = pygame.image.load(os.path.dirname(__file__)+"/textures/grass.png")
pygame.init()
screen = pygame.display.set_mode((900, 600))
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
        self.font = "TEXTURES/FONTS/PixelOperator.ttf"
        self.boldfont = "TEXTURES/FONTS/PixelOperator-Bold.ttf"
        self.largefont = "TEXTURES/FONTS/PixelOperator.ttf"
        self.largeboldfont = "TEXTURES/FONTS/PixelOperator-Bold.ttf"
        #initializing the font
        self.font = pygame.font.Font(self.font, 16)
        self.boldfont = pygame.font.Font(self.boldfont, 16)
        self.largefont = pygame.font.Font(self.largefont, 32)
        self.largeboldfont = pygame.font.Font(self.largeboldfont, 32)
        #dev options
        self.CFG_extensive_logs = True
        self.CFG_visuals = True
        self.CFG_debug_mode = True
        
        def load():
            pass

        def run(self):
            pass
Exo = Game
Exo.load()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        Exo.run()
        time.sleep(1/fps)

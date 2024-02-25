import pygame, os, sys
import time
import res.load
import res.terrain
#load files in othe directories like this: os.path.dirname(__file__) + "/folder/folder/file.png"
#put scripts into top-level directory, put images or other "universal files" into _internal in dist/main
#create a window in fullscreen size with a rectangle in it
#load file template:     grass = pygame.image.load(os.path.dirname(__file__)+"/textures/grass.png")
pygame.init()
pygame.font.init()

#main loop
running = True

fps = 30
inputvalues = []
class Game():
    def __init__(self):
        #game stuff
        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = fps
        #loading the font files
        self.font = os.path.dirname(__file__)+"/assets/FONTS/PixelOperator.ttf"
        self.boldfont = os.path.dirname(__file__)+"/assets/FONTS/PixelOperator-Bold.ttf"
        self.largefont = os.path.dirname(__file__)+"/assets/FONTS/PixelOperator.ttf"
        self.largeboldfont = os.path.dirname(__file__)+"/assets/FONTS/PixelOperator-Bold.ttf"
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

        #options
        self.S_Fitscreen = False
        self.S_Fullscreen = False
        #flat, smooth, chipped, mountainous, extreme, default
        self.S_Terrain_Preset = "mountainous"
        #small, medium, default, large
        self.S_Terrain_Size = "large"
        #spots (old) or lines (new)
        self.S_Terrain_Generator = "lines"
        #scale factor
        self.S_Terrain_Scale_Factor = 1
        




    def run(self):
            pass

frame = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if frame == 0:
        Exo = Game()

        res.load.respond(Exo)
        Exo.screen.fill((100,100,100))
        pygame.display.flip()
        time.sleep(1)
        res.terrain.terrain_quality_presets(Exo)
        res.terrain.generate(Exo)
        frame += 1
    Exo.run()
    pygame.display.flip()
    time.sleep(1/fps)


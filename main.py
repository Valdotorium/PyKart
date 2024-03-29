import pygame, os, sys
import time
import pymunk,pymunk.pygame_util
import res.load
import res.biomes
import res.physics
import res.build  
import res.interactions
import res.transfer
import res.procedural
import res.controls
import res.mechanics
from copy import deepcopy as deepcopy
import pyglet.media
import res.interactions.interactions as interactions
import res.fw.fw as utils
#load files in othe directories like this: os.path.dirname(__file__) + "/folder/folder/file.png"
#put scripts into top-level directory, put images or other "universal files" into _internal in dist/main
#create a window in fullscreen size with a rectangle in it
#load file template:     grass = pygame.image.load(os.path.dirname(__file__)+"/textures/grass.png")
pygame.init()
pygame.mixer.init()
pygame.font.init()

#main loop
running = True
fps = 60
frame = 0
inputvalues = []

class Game():
    def __init__(self):
        #game stuff
        self.selected_part = ""
        self.running = True

        self.clock = pygame.time.Clock()
        self.fps = fps
        self.partdict = {} # all part data in the game
        self.shopdict = {} #includes only part properties necessary while building
        #loading the font files
        self.font = os.path.dirname(__file__)+"/assets/FONTS/PixelOperator.ttf"
        self.boldfont = os.path.dirname(__file__)+"/assets/FONTS/PixelOperator-Bold.ttf"
        self.largefont = os.path.dirname(__file__)+"/assets/FONTS/PixelOperator.ttf"
        self.largeboldfont = os.path.dirname(__file__)+"/assets/FONTS/PixelOperator-Bold.ttf"
        #initializing the font
        self.font = pygame.font.Font(self.font, 22)
        self.boldfont = pygame.font.Font(self.boldfont, 24)
        self.largefont = pygame.font.Font(self.largefont, 32)
        self.largeboldfont = pygame.font.Font(self.largeboldfont, 36)
        #dev options
        self.CFG_extensive_logs = True
        self.CFG_visuals = True
        self.CFG_debug_mode = True
        self.CFG_limit_refresh_access = False
        self.CFG_Build_Enforce_Rules = True
        self.CFG_Reload_Latest_Vehicle = False
        self.CFG_Enable_Biomes = False
        self.CFG_Default_Screen_Size = (1200, 800)
        self.KeyCooldown = 0
        

        #options,olease set fit and fullscreen to false
        self.S_Fitscreen = False
        self.S_Fullscreen = False
        self.gm = "build"
        #flat, smooth, chipped, mountainous, extreme, default
        #self.S_Terrain_Preset = "mountainous"
        #small, medium, default, large
        #self.S_Terrain_Size = "large"
        #spots (old) or lines (new)
        #self.S_Terrain_Generator = "lines"
        #scale factor
        #self.S_Terrain_Scale_Factor = 1
        #new terrain settings:
        self.CFG_Terrain_Scale = 69 #must be below CFG_Terrain_X_Scale
        self.CFG_Terrain_Upscale_Factor = 100
        #size of each "point" in the ground polygon. 10 is 1/10 of the screen x size
        self.CFG_Terrain_X_Scale = 70
        #1 extremely slow, 3 normal, 5 hard, 8 fast, 12 extremely fast
        self.CFG_Terrain_Difficulty_Increase = 3.4
        #20 plain , 8 minimal noise, 6 low noise, 5 normal, 3 hillside, 2 mountainous
        self.CFG_Terrain_Flatness = 4.8

        self.X_Position = 0
        self.Y_Position = 0
        self.pi =3.1415926535897932384626433832795
        self.Throttle = 0
        self.VehicleSpeed = 0
        self.money = 12000
        self.SoundPlayer = pyglet.media.Player()
        self.GroundPolygons = []
        self.restart = False
        self.SelectedEnvironment = "Moon"
        self.Cursor = interactions.Cursor(self)
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
    def run(self):
    
        #res.interactions.interactions.ButtonArea(Exo)
        if self.gm == "game":
            Exo.screen.fill((120,120,120))
            #running the physics
            res.procedural.WritePolygonPositions(Exo)
            res.controls.GameControls(Exo)
            res.mechanics.GameMechanics(Exo)
            res.physics.simulate(Exo, fps)
            
        if self.gm =="build":
            #buiding mode
            Exo.screen.fill((180, 190, 230))
            res.build.run(Exo)
            res.controls.BuildControls(Exo)
        if self.gm == "transfer":
            res.transfer.run(Exo)
            res.physics.setup(Exo)
            res.physics.TransferStage(Exo)
            res.procedural.setup(Exo)
            res.procedural.generate_chunk(Exo)
            res.procedural.WritePolygonPositions(Exo)
        if self.gm == "biomeselection":
            self.BiomeSelector.update(self)
        if pygame.mouse.get_pressed()[0] and self.Cursor.CurrentAnimation == None:
            self.Cursor.Click()
        self.Cursor.update(self)
    def reset(self):
            self.gm = "build"
            self.restart = False
            del(self.space)
            self.GroundPolygons = []
            self.X_Position = 0
            self.Y_Position = 0
            self.pi =3.1415926535897932384626433832795
            self.Throttle = 0
            self.VehicleSpeed = 0
            res.procedural.WritePolygonPositions(self)
            res.physics.setup(self)

def resetFrames(obj, frame):
    frame = 1
    obj.reset()
    return frame

clock = pygame.time.Clock()
while running:
    if frame > 0:        
        running = Exo.running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #q quits the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False


    if frame == 0:
        Exo = Game()

        res.load.respond(Exo)
        Exo.BiomeSelector = res.biomes.BiomeSelection(Exo)
        Exo.screen.fill((100,100,100))
        pygame.display.flip()
        time.sleep(1)
        #res.terrain.terrain_quality_presets(Exo)
        #res.terrain.generate(Exo)
        #res.terrain.place(Exo)
        res.build.setup(Exo)
        #res.physics.setup(Exo)
        
        Exo.draw_options = pymunk.pygame_util.DrawOptions(Exo.screen)
    frame += 1

    Exo.run()
    #handling error messages
    if Exo.Errormessage != None:
        Exo.Errormessage.update(Exo)
    pygame.display.flip()
    clock.tick(fps)
    if Exo.gm == "game":
        if Exo.restart:
            frame = resetFrames(Exo, frame)
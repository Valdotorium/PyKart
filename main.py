# /// script
# dependencies = [
#  "pygame-ce",
#  "cffi",
#  "pymunk",
#  "pyglet",
#  "os",
#  "sys",
#  "time",
#  "copy",
# ]
# ///

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
import res.sounds
from copy import deepcopy as deepcopy
import pyglet.media
import res.interactions.interactions as interactions
import res.fw.fw as utils
import res.tutorial
import asyncio
import cffi
#load files in othe directories like this: os.path.dirname(__file__) + "/folder/folder/file.png"
#load file template:     grass = pygame.image.load(os.path.dirname(__file__)+"/textures/grass.png")

import platform
if sys.platform == "emscripten":
    platform.window.canvas.style.imageRendering = "pixelated"
class Game():
    def __init__(self):
        #PYGAME variables
        self.window = pygame.display.set_mode((1200,800), pygame.RESIZABLE)
        self.window.fill((100,100,100))
        self.lastFrameTime = time.time()
        self.frameTime = time.time()
        #DEV options
        self.isWeb = False
        self.debug = False
        self.selected_part = ""
        self.running = True
        self.fps = 48
        self.restart = False
        self.CFG_extensive_logs = True
        self.CFG_visuals = True
        self.CFG_debug_mode = True
        self.CFG_limit_refresh_access = False
        self.CFG_Build_Enforce_Rules = True
        self.CFG_Reload_Latest_Vehicle = False
        self.CFG_Enable_Biomes = False
        self.CFG_Default_Screen_Size = (1200,800)
        self.KeyCooldown = 0
        self.CFG_New_Game =True

        
        
        #STATIC
        #game vars
        self.TextAnimations = []
        self.partdict = {} # all part data in the game
        self.shopdict = {} #includes only part properties necessary while building
        self.X_Position = 0
        self.Y_Position = 0
        self.pi =3.1415926535897932384626433832795
        self.Throttle = 0
        self.DistanceMoneyForRide = 0
        self.VehicleSpeed = 0
        self.fpsFactor = 1
        self.UserHasRotatedPart = False
        self.money = 25000
        self.particles = []
        self.xp = 0        
        self.SoundPlayer = pyglet.media.Player()
        self.GroundPolygons = []
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        self.clock = pygame.time.Clock()
        #loading the font files
        self.smallfont = os.path.dirname(__file__)+"/assets/FONTS/PixelOperator.ttf"
        self.font = os.path.dirname(__file__)+"/assets/FONTS/PixelOperator.ttf"
        self.boldfont = os.path.dirname(__file__)+"/assets/FONTS/PixelOperator-Bold.ttf"
        self.largefont = os.path.dirname(__file__)+"/assets/FONTS/PixelOperator.ttf"
        self.largeboldfont = os.path.dirname(__file__)+"/assets/FONTS/PixelOperator-Bold.ttf"
        #initializing the font
        self.smallfont = pygame.font.Font(self.smallfont, 20)
        self.font = pygame.font.Font(self.font, 22)
        self.boldfont = pygame.font.Font(self.boldfont, 26)
        self.largefont = pygame.font.Font(self.largefont, 30)
        self.largeboldfont = pygame.font.Font(self.largeboldfont, 38)
        self.Cursor = interactions.Cursor(self)
        #options,set fit and fullscreen to false
        self.S_Fitscreen = False
        self.S_Fullscreen = False
        self.gm = "build"
        self.SelectedEnvironment = "Moon"
        #TERRAIN
        #new terrain settings:
        self.CFG_Terrain_Scale = 69 #must be below CFG_Terrain_X_Scale
        self.CFG_Terrain_Upscale_Factor = 100
        #size of each "point" in the ground polygon. 10 is 1/10 of the screen x size
        self.CFG_Terrain_X_Scale = 70
        #1 extremely slow, 3 normal, 5 hard, 8 fast, 12 extremely fast
        self.CFG_Terrain_Difficulty_Increase = 3.4
        #20 plain , 8 minimal noise, 6 low noise, 5 normal, 3 hillside, 2 mountainous
        self.CFG_Terrain_Flatness = 4.8

    def updateWindow(self,window):
        self.dimensions = (1200,800)
        
        self.rldimensions = self.window.get_size()
        self.screen = pygame.transform.scale(self.screen, self.rldimensions)
        self.window.fill((100,100,100))
        self.window.blit(self.screen, (0, 0))
        pygame.display.flip()
        self.screen = pygame.transform.scale(self.screen, self.CFG_Default_Screen_Size)
    def run(self):
        #the game scripts called every frame
        self.money = round(self.money)
        self.xp = round(self.xp)
        #res.interactions.interactions.ButtonArea(Exo)
        if self.gm == "game":
            self.screen.fill((120,120,120))
            #running the physics
            try:
                #the ground polygon
                res.procedural.WritePolygonPositions(self)
            except:
                print("INTERNAL ERROR:Failed to write ground polygon")
                self.money += (self.DistanceMoneyForRide + self.StuntMoneyForRide) * self.RideMoneyMultiplier
                self.xp += self.MetersTravelled * self.RideMoneyMultiplier
                self.restart = True
                if not self.isWeb:
                    AlertSound = self.sounds["alert.wav"]
                    player = AlertSound.play()
                    del(player)
                self.TextAnimations.append(interactions.TextAnimation("EXCEPTION: Could not write ground poly", 150, self))
                
            res.controls.GameControls(self)
            res.mechanics.GameMechanics(self)
            res.physics.simulate(self, self.fps)
            res.sounds.DrivingSounds(self)
            
        if self.gm =="build":
            #buiding mode
            self.screen.fill((180, 190, 230))
            try:
                res.build.run(self)
                res.controls.BuildControls(self)
            except:
                raise Exception("INTERNAL ERROR:Build mode failed to execute")
        if self.gm == "transfer":
            try:
                #setup physics simulation
                res.transfer.run(self)
                res.physics.setup(self)
                res.physics.TransferStage(self) # write new vehicle file
                res.sounds.setup(self)
                res.procedural.setup(self)
                res.procedural.generate_chunk(self)
                res.procedural.WritePolygonPositions(self)
            except:
                print("INTERNAL ERROR:Failed to run transfer game mode")
                self.TextAnimations.append(interactions.TextAnimation("EXCEPTION: failed transfer stage", 150, self))
                self.money += (self.DistanceMoneyForRide + self.StuntMoneyForRide) * self.RideMoneyMultiplier
                self.xp += self.MetersTravelled * self.RideMoneyMultiplier
                self.restart = True
                if not self.isWeb:
                    AlertSound = self.sounds["alert.wav"]
                    player = AlertSound.play()
                    del(player)

        if self.gm == "biomeselection":
            self.BiomeSelector.update(self)

        if self.gm == "tutorial":
            self.Tutorial.update(self)
        
        if pygame.mouse.get_pressed()[0] and self.Cursor.CurrentAnimation == None:
            self.Cursor.Click()
        self.Cursor.update(self)

        for i in range(len(self.TextAnimations)):
            self.TextAnimations[i].update(self)
        #utils
        utils.DisplayXP(self)
        self.credits.update(self)

        #calculating the execution time of every frame
        self.lastFrameTime = self.frameTime
        self.frameTime = time.time()
        self.clock.tick(self.fps)
        self.updateWindow(self.window)

        #"quit control"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                res.transfer.run(self)
            #q quits the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                    res.transfer.run(self)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.debug:
                        print("Player ESC")
                    self.money += (self.DistanceMoneyForRide + self.StuntMoneyForRide) *self.RideMoneyMultiplier
                    self.xp += self.MetersTravelled *self.RideMoneyMultiplier
                    self.restart = True
                    if not self.isWeb:
                        AlertSound = self.sounds["alert.wav"]
                        player = AlertSound.play()
                        del(player)
                    self.TextAnimations.append(interactions.TextAnimation("EXCEPTION: Could not write ground poly", 150, self))

    def reset(self):
            #resetting the veriables after a ride
            self.restart = False
            for i in self.PymunkBodies:
                self.PymunkBodies.remove(i)
            for i in self.PymunkJoints:
                self.PymunkJoints.remove(i)
            del(self.space)
            del(self.BuildUI)
            del(self.credits)
            del(self.CurrentPartUI)
            res.build.setup(self)
            self.StuntMoneyForRide = 0
            self.DistanceMoneyForRide = 0
            self.gm = "build"
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

async def main():
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()

    #TODO #11
    #make the game clean up obj.vehicle and associated lists when reloading the building mode (remove nonetype objects)

    #main loop
    running = True
    fps = 48
    frame = 0
    inputvalues = []
    while running:
        if frame > 0:        
            running = Exo.running


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
            Exo.Tutorial = res.tutorial.Tutorial(Exo)
            #res.physics.setup(Exo)
            
            Exo.draw_options = pymunk.pygame_util.DrawOptions(Exo.screen)
            time.sleep(1)

        frame += 1
        
        Exo.run()
        
        if Exo.fps * 0.7 > 1 /(Exo.frameTime - Exo.lastFrameTime):
            Exo.fps = round(Exo.fps / 1.3)
        if Exo.fps * 1.2 < 1 /(Exo.frameTime - Exo.lastFrameTime):
            Exo.fps = round(Exo.fps * 1.3)
        if Exo.fps > 60:
            Exo.fps = 60
        if Exo.fps < 16:
            Exo.fps = 16
        if Exo.debug:
            print(Exo.fps)

        await asyncio.sleep(0)
        #handling error messages
        if Exo.Errormessage != None:
            Exo.Errormessage.update(Exo)

        if Exo.gm == "game":
            if Exo.restart:
                frame = resetFrames(Exo, frame)
        if running == False:
            res.transfer.run(Exo)

asyncio.run(main())

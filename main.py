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
#load files in othe directories like this: os.path.dirname(__file__) + "/folder/folder/file.png"
#load file template:     grass = pygame.image.load(os.path.dirname(__file__)+"/textures/grass.png")

import platform
if sys.platform == "emscripten":
    platform.window.canvas.style.imageRendering = "pixelated"
class Game():
    def __init__(self):
        #game stuff
        self.window = pygame.display.set_mode((1200,800), pygame.RESIZABLE)
        self.window.fill((100,100,100))
        self.lastFrameTime = time.time()
        self.frameTime = time.time()
    

        self.selected_part = ""
        self.running = True
        self.fps = 48
        self.clock = pygame.time.Clock()
        
        self.partdict = {} # all part data in the game
        self.shopdict = {} #includes only part properties necessary while building
        #loading the font files
        self.smallfont = os.path.dirname(__file__)+"/assets/FONTS/PixelOperator.ttf"
        self.font = os.path.dirname(__file__)+"/assets/FONTS/PixelOperator.ttf"
        self.boldfont = os.path.dirname(__file__)+"/assets/FONTS/PixelOperator-Bold.ttf"
        self.largefont = os.path.dirname(__file__)+"/assets/FONTS/PixelOperator.ttf"
        self.largeboldfont = os.path.dirname(__file__)+"/assets/FONTS/PixelOperator-Bold.ttf"
        #initializing the font
        self.smallfont = pygame.font.Font(self.smallfont, 18)
        self.font = pygame.font.Font(self.font, 20)
        self.boldfont = pygame.font.Font(self.boldfont, 24)
        self.largefont = pygame.font.Font(self.largefont, 28)
        self.largeboldfont = pygame.font.Font(self.largeboldfont, 36)
        #dev options
        self.CFG_extensive_logs = True
        self.CFG_visuals = True
        self.CFG_debug_mode = True
        self.CFG_limit_refresh_access = False
        self.CFG_Build_Enforce_Rules = True
        self.CFG_Reload_Latest_Vehicle = False
        self.CFG_Enable_Biomes = False
        self.CFG_Default_Screen_Size = (1200,800)
        self.KeyCooldown = 0
        self.CFG_New_Game =False
        self.TextAnimations = []
        

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
        self.fpsFactor = 1
        self.money = 22500
        self.particles = []
        self.xp = 0        
        self.SoundPlayer = pyglet.media.Player()
        self.GroundPolygons = []
        self.restart = False
        self.SelectedEnvironment = "Moon"
        self.Cursor = interactions.Cursor(self)
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        self.clock = pygame.time.Clock()
    def updateWindow(self,window):
        self.dimensions = (1200,800)
        self.rldimensions = self.window.get_size()
        self.screen = pygame.transform.scale(self.screen, self.rldimensions)
        self.window.fill((100,100,100))
        self.window.blit(self.screen, (0, 0))
        pygame.display.flip()
        self.screen = pygame.transform.scale(self.screen, self.CFG_Default_Screen_Size)
        self.screen.fill((100,100,100))
    def run(self):
        self.money = round(self.money)
        self.xp = round(self.xp)

    
        #res.interactions.interactions.ButtonArea(Exo)
        if self.gm == "game":
            self.screen.fill((120,120,120))
            #running the physics
            try:
                res.procedural.WritePolygonPositions(self)
            except:
                print("INTERNAL ERROR:Failed to write ground polygon")
                self.money += (self.DistanceMoneyForRide + self.StuntMoneyForRide) * self.RideMoneyMultiplier
                self.xp += self.MetersTravelled * self.RideMoneyMultiplier
                self.restart = True
                AlertSound = self.sounds["alert.wav"]
                player = AlertSound.play()
                self.TextAnimations.append(interactions.TextAnimation("EXCEPTION: Could not write ground poly", 150, self))
                del(player)
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
                res.transfer.run(self)
                res.physics.setup(self)
                res.physics.TransferStage(self)
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
        utils.DisplayXP(self)
        self.credits.update(self)
        self.clock.tick(self.fps)
        self.updateWindow(self.window)
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
                    print("Player ESC")
                    self.money += (self.DistanceMoneyForRide + self.StuntMoneyForRide) *self.RideMoneyMultiplier
                    self.xp += self.MetersTravelled *self.RideMoneyMultiplier
                    self.restart = True
                    AlertSound = self.sounds["alert.wav"]
                    player = AlertSound.play()
                    self.TextAnimations.append(interactions.TextAnimation("EXCEPTION: Could not write ground poly", 150, self))
                    del(player)


    def reset(self):

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
        Exo.lastFrameTime = Exo.frameTime
        Exo.frameTime = time.time()
        """DynaFrame:
        print("frametime = ", Exo.frameTime - Exo.lastFrameTime)
        recentFrameTime = Exo.frameTime - Exo.lastFrameTime
        if recentFrameTime > (1 / Exo.fps * 1.1):
            print("regulating FPS down to:", (1/recentFrameTime) * 0.75)
            Exo.fps = (1/recentFrameTime) * 0.9
        elif recentFrameTime < (1 / Exo.fps * 0.9):
            print("regulating FPS up to:", (1/recentFrameTime) * 1.1)
            Exo.fps = (1/recentFrameTime) * 1.1"""
        recentFrameTime = Exo.frameTime - Exo.lastFrameTime
        if 0 < recentFrameTime < 0.02 and Exo.fps >48:
            Exo.fps = 48
        elif 0.02 < recentFrameTime < 0.045 and Exo.fps > 32:
            Exo.fps = 32
        elif 0.046 < recentFrameTime < 0.08 and Exo.fps > 20:
            Exo.fps = 20
        else:
            Exo.fps = 16
        Exo.fpsFactor = Exo.fps / 48
        print("fps: ", Exo.fps, "vspd", Exo.VehicleSpeed)

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

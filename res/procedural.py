import random
import pygame
import pymunk
from .fw import fw as utils
import time

def Noise(obj, scale, variability, randomnoise):
        #main  terrain generator function
        #print("----------------------------------------------------------------")
        x = 0
        #Height_Change = random.uniform(-obj.CFG_Terrain_Scale * scale, obj.CFG_Terrain_Scale * scale)
        Height_Change = 0
        Terrain_Direction = 0
        #should be renamed flatness, the higher, the flatter the terrain
        steepness = obj.Environment["Terrain"]["Flatness"]
        
        while x < len(obj.Terrain):
            if x > 25:
                r = random.uniform(0,100)
                if r < variability:
                    Terrain_Direction += random.randint(-1,1)
                #keeping Terrain_Direction within valid area (-3 to 3)
                if Terrain_Direction > 3:
                    Terrain_Direction = 3
                elif Terrain_Direction < -3:
                    Terrain_Direction = -3
                if randomnoise:
                    if Terrain_Direction > 0:
                        Height_Change += random.uniform(0, ((obj.CFG_Terrain_Scale * scale) / 50) * (Terrain_Direction / steepness))
                    elif Terrain_Direction < 0:
                        Height_Change += random.uniform(-((obj.CFG_Terrain_Scale * scale )/ 50) * (-Terrain_Direction / steepness), 0)
                else:
                    Height_Change +=( ((obj.CFG_Terrain_Scale * scale) / 80) * (Terrain_Direction / steepness) )
                    if Terrain_Direction > 0:
                        Height_Change += random.uniform(0, ((obj.CFG_Terrain_Scale * scale) / 600) * (Terrain_Direction / steepness))
                    elif Terrain_Direction < 0:
                        Height_Change += random.uniform(-((obj.CFG_Terrain_Scale * scale )/ 600) * (-Terrain_Direction / steepness), 0)
            Height_Change * scale

            obj.Terrain[x] += Height_Change
            obj.Terrain[x] = round(obj.Terrain[x])
            if obj.Terrain[x] < -25000:
                obj.Terrain[x] = -25000
                Height_Change = 0
                Terrain_Direction = 1
            if obj.Terrain[x] > 25000:
                obj.Terrain[x] = 25000
                Height_Change = 0
                Terrain_Direction = -1
            
            x += 1
            difficultyFactor = obj.Environment["Terrain"]["Difficulty"]
            difficultyFactor /= 10000
            steepness -= difficultyFactor + steepness * (difficultyFactor / 10)
            if steepness > 20:
                steepness = 20
            if steepness < 0.2:
                steepness = 0.2
            #1 screen = around 40 m
            if x == 4000:
               print("steepness at 280000px:",steepness)
            if x == 8000:
               print("steepness at 560000px:",steepness)
            if x == 12000:
               print("steepness at 740000px:",steepness)
        print("steepness at end:",steepness)
def setup(obj):
    obj.Terrain = []
    obj.TerrainAssets = []
    AssetChance = obj.Environment["Visuals"]["AssetFrequency"]
    if obj.isWeb:
        AssetChance = round(AssetChance / 2.5)
    AssetCount = len(obj.Environment["Visuals"]["Assets"])
    x = 0
    obj.Terrain.append(-10000)
    while x < 7500:
        r = random.uniform(0,100)
        if r < AssetChance and x > 40:
            if AssetCount != 0:
                obj.TerrainAssets.append(random.randint(0, AssetCount - 1))
            else:
                obj.TerrainAssets.append(None)
        else:
            obj.TerrainAssets.append(None)
        obj.Terrain.append(650)
        x += 1

def generate_chunk(obj):
    c = 1
    while c < obj.Environment["Terrain"]["Layers"] + 1:
        #scaling the variability and scale values by the upscalefactor by the terrain and generating noise woth the new values
        Noise(obj, round(obj.Environment["Terrain"]["StartScale"] / (obj.Environment["Terrain"]["UpscaleFactor"] * c)), obj.Environment["Terrain"]["StartVariability"] * (obj.Environment["Terrain"]["UpscaleFactor"] * c), obj.Environment["Terrain"]["RandomNoise"][c-1])
        c += 1
    if obj.debug:
        print("total terrain length:", len(obj.Terrain) * obj.Environment["Terrain"]["Scale"])



def PreparePolygons(obj):
    #write a long list of all polygon x and y vertices
    #form a lot of pymunk polys and put them in a list to use later for the physics simulation

    PygamePolygon = []
    Xscale = obj.Environment["Terrain"]["Scale"]
    c = 0
    while c < len(obj.Terrain):
        PygamePolygon.append(((Xscale * c - 10), obj.Terrain[c])) #dont forget bottom edge points later
        c += 1
    #print("PygamePolygon: ", PygamePolygon)

    #creating pymunk and pygame polygons
    PymunkPolygons = []
    PygamePolygons = []
    c = 0
    while c < len(PygamePolygon) - 2:
        #creating the edge vertices for the pymunk poly
        ItemA = PygamePolygon[c]
        ItemB = PygamePolygon[c+1]
        ItemAX = ItemA[0]
        ItemBX = ItemB[0]
        Vertices = [ItemA, ItemB, (ItemBX, 25100), (ItemAX, 25100)]
        #creating the polygon vertices
        Poly = Vertices
        PymunkPolygons.append(Poly)
        c += 1
        #creating the pygame polygons (inverting the Ys)
        Vertices = [ItemA, ItemB, (ItemBX, -25100), (ItemAX, -25100)]
        PygamePolygons.append(Vertices)
    
    obj.PygamePolygons = PygamePolygon
    obj.PymunkPolygons = PymunkPolygons
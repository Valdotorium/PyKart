import pygame
import random
from .interactions import interactions as interactions
def setup(obj):
    scaleX = obj.dimensions[0] / 1200
    scaleY = obj.dimensions[1] / 800
    obj.scalefactor = scaleX 
    #the calculations of the game are performed in a 1200x800 screen, which will later get rescaled onto the actual window size. everything dealing with positions and sizes needs to get multiplied by scaleX
    print(1200 * scaleX , 800 * scaleX)

 
def run(obj):
    scaleX = obj.scalefactor
    #--------------------------Drawing the part inventory---------------------------------------------------
    inventoryTileImage = obj.textures["UI_tile.png"]
    obj.inventoryTile = pygame.transform.scale(inventoryTileImage, (int(64 * scaleX), int(64 * scaleX)))
    c = 0
    while c < len(obj.partdict):
        gap = 10 * scaleX
        part_img = obj.partdict[list(obj.partdict)[c]]["Tex"]
        part_img = obj.textures[part_img]
        IsClicked = interactions.ButtonArea(obj, part_img, (c *(64 * scaleX) + c * gap,obj.dimensions[1] - 100), ((64 * scaleX), int(64 * scaleX)))
        c += 1
        if IsClicked:
            print(f"User just cligged on part {obj.partdict[list(obj.partdict)[c - 1]]["Name"]}")
            

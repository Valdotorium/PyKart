import pygame
import random
from .interactions import interactions as interactions
def setup(obj):
    scaleX = obj.dimensions[0] / 1200
    scaleY = obj.dimensions[1] / 800
    obj.scalefactor = scaleX 
    #the calculations of the game are performed in a 1200x800 screen, which will later get rescaled onto the actual window size. everything dealing with positions and sizes needs to get multiplied by scaleX
    print(1200 * scaleX , 800 * scaleX)
    obj.selectedPart = ""

 
def run(obj):
    scaleX = obj.scalefactor
    mx, my = pygame.mouse.get_pos()
    #------------------------------Upon placement, check if the position of the parts center is within a valid rectangle (BuildBackgroundImg)--------------------------------
    if obj.selectedPart != "" and pygame.mouse.get_pressed()[0]:
        #if the mouse is touching BuildBackgroundImg, the part gets placed
        if obj.dimensions[0] * 0.125 < mx < 0.875 * obj.dimensions[0] and obj.dimensions[1] * 0.125 < my < 0.875 * obj.dimensions[1]:
            print("placed!")
        else:
            #the part gets unselected
            obj.selectedPart = ""
    #--------------------------Drawing the part inventory---------------------------------------------------
    inventoryTileImage = obj.textures["UI_tile.png"]
    obj.inventoryTile = pygame.transform.scale(inventoryTileImage, (int(64 * scaleX), int(64 * scaleX)))
    c = 0
    #background for inventory tiles
    TileBackgroundImg = obj.textures["UI_tile.png"]
    TileBackgroundImg = pygame.transform.scale(TileBackgroundImg, (int(64 * scaleX), int(64 * scaleX)))
    #background for the building area
    BuildBackgroundImg = pygame.transform.scale(TileBackgroundImg,( round(obj.dimensions[0] * 0.75), round(obj.dimensions[1] * 0.75)))
    obj.screen.blit(BuildBackgroundImg, (obj.dimensions[0] / 8, obj.dimensions[1] / 8))
    while c < len(obj.partdict):
        gap = 10 * scaleX
        #getting the name of the texture
        part_img = obj.partdict[list(obj.partdict)[c]]["Tex"]
        #geting the preloaded surface using the name as key
        part_img = obj.textures[part_img]
        obj.screen.blit(TileBackgroundImg, (c *(64 * scaleX) + c * gap,obj.dimensions[1] - 100))
        IsClicked = interactions.ButtonArea(obj, part_img, (c *(64 * scaleX) + c * gap,obj.dimensions[1] - 100), ((64 * scaleX), int(64 * scaleX)))
        c += 1
        
        if IsClicked:
            print(f"User just cligged on part {obj.partdict[list(obj.partdict)[c - 1]]["Name"]}")
            obj.selectedPart = obj.partdict[list(obj.partdict)[c - 1]]["Name"]
    #------------------------------Drawing the selected part at mouse pos-------------------------------------
    if obj.selectedPart != "":
        #jos code
        textur = obj.partdict[obj.selectedPart]["Stex"]
        textur = obj.textures[textur]
        textur = pygame.transform.scale(textur, (int(64 * scaleX), int(64 * scaleX)))
        obj.screen.blit(textur, (mx - int(64 * scaleX) / 2, my - int(64 * scaleX) / 2))


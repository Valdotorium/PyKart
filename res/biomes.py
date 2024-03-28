import pygame
import random,json,os
from .interactions import interactions as interactions
from .fw import fw as utils
def BiomeSelection(obj):
    Biomes = obj.biomes
    obj.screen.fill((130,130,130))
    PlayButtonImg = obj.textures["PlayButton.png"]
    PlayButtonImg = pygame.transform.scale(PlayButtonImg, utils.Scale(obj,[64,64]))
    PlayButton = interactions.ButtonArea(obj, PlayButtonImg, utils.Scale(obj,[568,50]), utils.Scale(obj,[64,64]))
    CurrentItem = 0
    CurrentBiome = list(Biomes)[CurrentItem]
    CurrentBiome = Biomes[CurrentBiome]
    ScrollX = 0
    XPos = obj.dimensions[0] / 2 - 400
    c = 0
    while c < len(Biomes):
        Biome = list(Biomes)[c]
        Biome = Biomes[Biome]
        print(Biome)
        #drawing the current biome in the foreground
        BiomeImage = obj.textures[Biome["Preview"]]
        BiomeImage = pygame.transform.scale(BiomeImage, (500,500))
        obj.screen.blit(BiomeImage, (XPos, obj.dimensions[1] / 2 - 250))
        #draw a white rect around the biome image with width 5
        pygame.draw.rect(obj.screen, (255,255,255), (XPos, obj.dimensions[1] / 2 - 250,500,500), 6,6)

        XPos += 180
        c += 1
    if PlayButton:
        print("User just cligged on the play button")
        obj.gm = "transfer"
        obj.SelectedBiome = CurrentBiome["Name"]




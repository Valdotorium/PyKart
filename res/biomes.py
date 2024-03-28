import pygame
import random,json,os
from .interactions import interactions as interactions
from .fw import fw as utils
class BiomeSelection():
    def __init__(self, obj):
        self.CurrentSelectedBiome = 0
        self.CurrentHoveredBiome = 0
        self.TicksInCurrentSelectedBiome = 0
        self.ScrollX = 0
        self.Biomes = obj.biomes
    def update(self, obj):
        
        obj.screen.fill((130,130,130))
        PlayButtonImg = obj.textures["PlayButton.png"]
        PlayButtonImg = pygame.transform.scale(PlayButtonImg, utils.Scale(obj,[64,64]))
        CurrentItem = 0
        CurrentBiome = list(self.Biomes)[CurrentItem]
        CurrentBiome = self.Biomes[CurrentBiome]
        XPos = obj.dimensions[0] / 2 - 400
        c = 0
        while c < len(self.Biomes):
            mx, my = pygame.mouse.get_pos()
            Biome = list(self.Biomes)[c]
            Biome = self.Biomes[Biome]
            #drawing the current biome in the foreground
            BiomeImage = obj.textures[Biome["Preview"]]

            #background image of selected biome, low alpha
            if c == self.CurrentSelectedBiome:
                BackgroundImage =  pygame.transform.scale(BiomeImage, (obj.dimensions[0],obj.dimensions[1]))
                BackgroundImage = BackgroundImage.convert()
                if self.TicksInCurrentSelectedBiome < 150:
                    BackgroundImage.set_alpha(round(self.TicksInCurrentSelectedBiome / 2))
                else:
                    BackgroundImage.set_alpha(75)
                obj.screen.blit(BackgroundImage, (0,0))
            BiomeImage = BiomeImage.convert()
            BiomeImage = pygame.transform.scale(BiomeImage, (500,500))
            obj.screen.blit(BiomeImage, (XPos, obj.dimensions[1] / 2 - 250))
            #draw a white rect around the biome image with width 5
            pygame.draw.rect(obj.screen, (255,255,255), (XPos, obj.dimensions[1] / 2 - 250,500,500), 6,6)

            self.CurrentHoveredBiome = round((mx  - (obj.dimensions[0] / 2 - 400)- 90 + self.ScrollX) / 180)
            if self.CurrentHoveredBiome < 0:
                self.CurrentHoveredBiome = 0
            if self.CurrentHoveredBiome > len(self.Biomes) - 1:
                self.CurrentHoveredBiome = len(self.Biomes) - 1
            if self.CurrentHoveredBiome != self.CurrentSelectedBiome:
                self.CurrentSelectedBiome = self.CurrentHoveredBiome
                self.TicksInCurrentSelectedBiome = 0
            else:
                self.TicksInCurrentSelectedBiome += 1
            if c == self.CurrentHoveredBiome:
                print(self.TicksInCurrentSelectedBiome)
                obj.screen.blit(BiomeImage, (XPos, obj.dimensions[1] / 2 - 250))
                #draw a white rect around the biome image with width 5
                pygame.draw.rect(obj.screen, (255,255,255), (XPos, obj.dimensions[1] / 2 - 250,500,500), 6,6)
                if 100 < self.TicksInCurrentSelectedBiome < 355:
                    PlayButtonImg.set_alpha(self.TicksInCurrentSelectedBiome - 100)
                    print("DDDD")
                    PlayButton = interactions.ButtonArea(obj, PlayButtonImg, (XPos + 50, obj.dimensions[1] / 2 - 200), utils.Scale(obj,[64,64]))
                    if PlayButton:
                        print("User just cligged on the play button")
                        obj.gm = "transfer"
                        SelectedBiome = list(self.Biomes)[self.CurrentSelectedBiome]
                        SelectedBiome = self.Biomes[SelectedBiome]
                        obj.SelectedEnvironment = SelectedBiome["Name"]
                elif self.TicksInCurrentSelectedBiome >= 355:
                    PlayButton = interactions.ButtonArea(obj, PlayButtonImg, (XPos + 50, obj.dimensions[1] / 2 - 200), utils.Scale(obj,[64,64]))
                    if PlayButton:
                        print("User just cligged on the play button")
                        obj.gm = "transfer"
                        SelectedBiome = list(self.Biomes)[self.CurrentSelectedBiome]
                        SelectedBiome = self.Biomes[SelectedBiome]
                        obj.SelectedEnvironment = SelectedBiome["Name"]
                        print(obj.SelectedEnvironment)
                XPos += 540
            
            
            else:
                obj.screen.blit(BiomeImage, (XPos, obj.dimensions[1] / 2 - 250))
                #draw a white rect around the biome image with width 5
                pygame.draw.rect(obj.screen, (255,255,255), (XPos, obj.dimensions[1] / 2 - 250,500,500), 6,6)
                XPos += 180
            c += 1
        #text
        BiomeName = list(self.Biomes)[self.CurrentSelectedBiome]
        BiomeName = self.Biomes[BiomeName]["Name"]
        text = obj.largeboldfont.render(BiomeName, True, (20,20,20))
        #display it at the top centered
        obj.screen.blit(text, (obj.dimensions[0] / 2 - text.get_width()/ 2, 100))
        





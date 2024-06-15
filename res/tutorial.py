
import pygame
import copy
from .fw import fw as utils
from .interactions import interactions as interactions
import time
class Tutorial():
    def __init__(self, obj):
        self.font = obj.largefont
        self.contents = obj.tutorials
        self.textures = obj.textures
        self.Scroll = 0
        self.Page = 0
        self.cooldown = 0
    def update(self, obj):
        """the articles of the tutorial are stored in a list as json.
        within the articles, there is a list of lines, having a type and content (e.g "TXT", "Tutorial line text)"""
        self.DrawY = 150
        if not obj.isWeb:
            SelectPartSound = obj.sounds["click.wav"]
            AlertSound = obj.sounds["alert.wav"]
        self.cooldown -= 1
        obj.screen.fill((140,140,140))

        pygame.draw.rect(obj.screen, (200, 200, 200), (obj.dimensions[0] / 24, 0, 1100, 800))
        TutButton = interactions.ButtonArea(obj, obj.textures["UnselectButton.png"], utils.Scale(obj,(obj.dimensions[0] - 150,50)), utils.Scale(obj,[64,64]))
        if TutButton and self.cooldown < 0 or pygame.key.get_pressed()[pygame.K_s]:

            obj.gm = "build"
            self.cooldown = 8
            if not obj.isWeb:
                player = AlertSound.play()
                del(player)
        RightButton = interactions.ButtonArea(obj, obj.textures["ButtonRight.png"], utils.Scale(obj,(obj.dimensions[0] - 60,50)), utils.Scale(obj,[64,64]))
        if RightButton and self.cooldown < 0:
            self.Page += 1
            self.cooldown = 8
            self.Scroll = 0
            if not obj.isWeb:
                player = obj.sounds["click.wav"].play()
                del(player)
        LeftButton = interactions.ButtonArea(obj, obj.textures["ButtonLeft.png"], utils.Scale(obj,(30,50)), utils.Scale(obj,[64,64]))
        if LeftButton and self.cooldown < 0:
            self.Page -= 1
            self.cooldown = 8
            self.Scroll = 0
            player = SelectPartSound.play()
            del(player)
        if self.Page < 0:
            self.Page = 0
        if self.Page > len(self.contents) - 1:
            self.Page = len(self.contents) - 1
        text = obj.largeboldfont.render("Page: "+str(self.Page)+" "+ self.contents[self.Page]["Title"], True, (20,20,20))
        obj.screen.blit(text, (int(obj.dimensions[0] * 0.2), 60))
        self.CurrentArticle = self.contents[self.Page]["Contents"]
        if obj.debug:
            print(self.CurrentArticle)
        for element in self.CurrentArticle:
            if element["Element"] == "TEXT":
                for line in element["Content"]:
                    if element["Size"] == "SMALL":
                        text = obj.smallfont.render(line, True, (20,20,20))
                    elif element["Size"] == "MEDIUM":
                        text = obj.font.render(line, True, (20,20,20))
                    elif element["Size"] == "LARGE":
                        text = obj.largefont.render(line, True, (20,20,20))
                    else:
                        text = obj.largeboldfont.render(line, True, (20,20,20))
                    obj.screen.blit(text, (int(obj.dimensions[0] * 0.15), self.DrawY))
                    self.DrawY += text.get_height() + 7
            elif element["Element"] == "IMG":
                image = self.textures[element["Content"]]
                image = pygame.transform.scale(image, element["Size"])
                obj.screen.blit(image, (obj.dimensions[0] * 0.33 - element["Size"][0] / 2, self.DrawY))
                self.DrawY += element["Size"][1] + 5
 

        
        
    


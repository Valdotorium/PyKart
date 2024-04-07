
import pygame
import copy
from .fw import fw as utils
from .interactions import interactions as interactions
import time
class Tutorial():
    def __init__(self, obj):
        self.font = obj.largefont
        self.contents = obj.LoadedTutorial
        self.textures = obj.textures
        self.Scroll = 0
    def update(self, obj):
        """the articles of the tutorial are stored in a list as json.
        within the articles, there is a list of lines, having a type and content (e.g "TXT", "Tutorial line text)"""
        self.DrawY = 0
        obj.screen.fill((140,140,140))
        TutButton = interactions.ButtonArea(obj, obj.textures["UnselectButton.png"], utils.Scale(obj,(obj.dimensions[0] - 630,50)), utils.Scale(obj,[64,64]))
        if TutButton:
            obj.gm = "build"
        
    


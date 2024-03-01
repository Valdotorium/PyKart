import pygame
import time
import os
from .fw import fw as utils
import json
def respond(obj):
    print("ive loaded from the source package!")
    time.sleep(1)
    obj.dimensions = utils.getScreenSize()
    print("LOG: screen dimensions are:", obj.dimensions)
    if obj.S_Fitscreen:
        utils.displayText(obj,"fitting screen sizes")
        if obj.S_Fullscreen:
            obj.screen = pygame.display.set_mode(obj.dimensions[0], pygame.FULLSCREEN)
        else:
            obj.screen = pygame.display.set_mode(obj.dimensions[0])
        obj.screen.fill((100, 100, 100))
        pygame.display.set_caption("Project Exoplanet") 
    else:
        obj.screen = pygame.display.set_mode((1200, 800))
        obj.screen.fill((100, 100, 100))
        pygame.display.set_caption("Project Exoplanet")
    obj.dimensions = obj.dimensions[0]
    utils.displayText(obj,"finding files")

    CurrentPath = os.path.dirname(os.path.realpath(os.path.dirname(__file__)))
    gamefiles = os.listdir(CurrentPath)

    print("LOG: found gamefiles in:", gamefiles)
    utils.displayText(obj,"checking for necessary files")
    if "assets" in gamefiles:
        print("file loader path is: ", CurrentPath)
        utils.displayText(obj,"found assets folder")
        if "images" in os.listdir(CurrentPath+"/assets"):
            imagefiles = os.listdir(CurrentPath+"/assets/images")
            textures = {}
            for image in imagefiles:
                loadedimage = pygame.image.load(CurrentPath+"/assets/images/"+image)

                utils.clear(obj.screen)
                utils.displayText(obj,f"loaded image {image}")
                time.sleep(1)
                textures[image] = loadedimage
            print("LOG: loaded all images into:", textures)
            
            partfiles = os.listdir(CurrentPath+"/assets/parts")
            for part in partfiles:
                loadedpart = json.load(open(CurrentPath+"/assets/parts/"+part))
                utils.DecodePart(loadedpart, obj)
                utils.clear(obj.screen)
                utils.displayText(obj,f"loaded part {part}")
                time.sleep(1)
            print("all parts loaded to game: ", obj.partdict)
            print("all parts loaded to shop: ", obj.shopdict)
        else:
            exit
    else:
        utils.displayText(obj,"ERROR: no textures folder found")
        print("ERRNO_02: No textures or assets folder found in " + CurrentPath)
        exit

    utils.displayText(obj, "All Done!")

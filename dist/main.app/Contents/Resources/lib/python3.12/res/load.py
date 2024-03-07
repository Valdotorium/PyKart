import pygame
import time
import os
from .fw import fw as utils
import json
def respond(obj):
    """This script is responsible for loading the games assets, such as images and parts. it will load everything in the folder it finds.
    WARNING: In py2app, the assets folder must be included TWICE in several locations of the app, see py2app.txt"""
    print("ive loaded from the source package!")
    time.sleep(1)
    #getting the window size
    obj.dimensions = utils.getScreenSize()
    print("LOG: screen dimensions are:", obj.dimensions)
    if obj.S_Fitscreen:
        if obj.S_Fullscreen:
            #makes it fullscreen
            obj.screen = pygame.display.set_mode(obj.dimensions[0], pygame.FULLSCREEN)
        else:
            #makes it windowed, but with the size of the full screen
            obj.screen = pygame.display.set_mode(obj.dimensions[0])
        obj.screen.fill((100, 100, 100))
        pygame.display.set_caption("Project Exoplanet") 
    else:
        #smol version
        obj.screen = pygame.display.set_mode((1200, 800))
        obj.screen.fill((100, 100, 100))
        obj.dimensions[0] = (1200, 800)
        pygame.display.set_caption("Project Exoplanet")
    obj.dimensions = obj.dimensions[0]
    utils.displayTextCenter(obj,"finding files")
    #locating the game assets

    CurrentPath = os.path.dirname(os.path.realpath(os.path.dirname(__file__)))
    gamefiles = os.listdir(CurrentPath)

    print("LOG: found gamefiles in:", gamefiles)
    utils.displayTextCenter(obj,"checking for necessary files")
    if "assets" in gamefiles:
        print("file loader path is: ", CurrentPath)
        utils.displayText(obj,"found assets folder")
        #loading images from the images folder
        if "images" in os.listdir(CurrentPath+"/assets"):
            imagefiles = os.listdir(CurrentPath+"/assets/images")
            textures = {}
            #loading all the images into the game
            for image in imagefiles:
                loadedimage = pygame.image.load(CurrentPath+"/assets/images/"+image)

                utils.clear(obj.screen)
                #center the text

                utils.displayTextCenter(obj,f"loaded image {image}")
                textures[image] = loadedimage
            print("LOG: loaded all images into:", textures)
            obj.textures = textures

            #loading all the parts into the game
            partfiles = os.listdir(CurrentPath+"/assets/parts")
            for part in partfiles:
                loadedpart = json.load(open(CurrentPath+"/assets/parts/"+part))
                utils.DecodePart(loadedpart, obj)
                utils.clear(obj.screen)
                utils.displayTextCenter(obj,f"loaded part {part}")
            print("all parts loaded to game: ", obj.partdict)
            print("all parts loaded to shop: ", obj.shopdict)

        else:
            exit
    else:
        utils.displayTextCenter(obj,"ERROR: no textures folder found")
        print("ERRNO_02: No textures or assets folder found in " + CurrentPath)
        exit

    utils.displayTextCenter(obj, "All Done!")

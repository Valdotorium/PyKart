import pygame
import time
from .fw import fw as utils
def respond(obj):
    print("ive loaded from the source package!")
    utils.displayText(obj,"loading game data")
    time.sleep(1)
    obj.dimensions = utils.getScreenSize()
    print("LOG: screen dimensions are:", obj.dimensions)
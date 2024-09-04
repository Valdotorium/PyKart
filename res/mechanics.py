import pygame
import pymunk
from .fw import fw as utils
def camera(obj):
    #camera positions
    OldX = obj.X_Position
    ReferencePosition = obj.PymunkBodies[0].position
    obj.VehicleSpeed = round((ReferencePosition[0] - obj.dimensions[0] / 2 - OldX + obj.camXOffset) * 5.4) / (48/obj.fps)
    obj.X_Position = round(ReferencePosition[0]) - obj.dimensions[0] / 2 + obj.camXOffset
    obj.Y_Position = round(ReferencePosition[1]) - obj.dimensions[1] / 2 + obj.camYOffset

def GameMechanics(obj):
    camera(obj)
def Engine(obj,EnginePart, WheelPart):
    pass
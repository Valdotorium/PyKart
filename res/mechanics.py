import pygame
import pymunk

def camera(obj):
    #camera positions
    ReferencePosition = obj.PymunkBodies[0].position
    obj.X_Position = round(ReferencePosition[0]) - obj.dimensions[0] / 2
    obj.Y_Position = round(ReferencePosition[1]) - obj.dimensions[1] / 2
def GameMechanics(obj):
    camera(obj)
def Engine(obj,EnginePart, WheelPart):
    pass
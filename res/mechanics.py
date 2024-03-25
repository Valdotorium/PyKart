import pygame
import pymunk

def camera(obj):
    #camera positions
    OldX = obj.X_Position
    ReferencePosition = obj.PymunkBodies[0].position
    obj.VehicleSpeed = round((ReferencePosition[0] - obj.dimensions[0] / 2 - OldX) * 5.4)
    obj.X_Position = round(ReferencePosition[0]) - obj.dimensions[0] / 2
    obj.Y_Position = round(ReferencePosition[1]) - obj.dimensions[1] / 2
    text = obj.largefont.render(str(obj.VehicleSpeed), True, (60,60,60))
    obj.screen.blit(text, (50,50))
def GameMechanics(obj):
    camera(obj)
def Engine(obj,EnginePart, WheelPart):
    pass
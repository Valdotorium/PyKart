import pygame
import pymunk
def Throttle(obj):
    if 0 < obj.Throttle < 0.5:
        obj.Throttle = 0
    if obj.Throttle > 100:
        obj.Throttle = 100
    #same conditions as before, but negative
    if -0.5 < obj.Throttle < 0:
        obj.Throttle = 0
    if obj.Throttle < -100:
        obj.Throttle = -100
    else:
        obj.Throttle = obj.Throttle * 0.96
    

    #apply forces to pymunk bodies
    c = 0
    while c < len(obj.PymunkBodies):
        if obj.VehicleTypes[c][0]=="Wheel":
            force = [obj.Throttle * obj.NewVehicle[c]["Properties"]["Force"],0]
            point = (0, -obj.NewVehicle[c]["Center"][0])
            obj.PymunkBodies[c].apply_force_at_local_point(force, point)
        c += 1
def camera(obj):
    #camera positions
    ReferencePosition = obj.PymunkBodies[0].position
    obj.X_Position = round(ReferencePosition[0]) - obj.dimensions[0] / 2
    obj.Y_Position = round(ReferencePosition[1]) - obj.dimensions[1] / 2
    print(obj.X_Position, obj.Y_Position)
def GameMechanics(obj):
    Throttle(obj)
    camera(obj)
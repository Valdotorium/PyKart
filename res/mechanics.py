import pygame
import pymunk
def Throttle(obj):
    if obj.Throttle < 0.5:
        obj.Throttle = 0
    if obj.Throttle > 100:
        obj.Throttle = 100
    else:
        obj.Throttle = obj.Throttle * 0.96

    #apply forces to pymunk bodies
    c = 0
    while c < len(obj.PymunkBodies):
        if obj.VehicleTypes[c][0]=="Wheel":
            force = [obj.Throttle * 40,0]
            point = (0, -obj.NewVehicle[c]["Center"][0])
            obj.PymunkBodies[c].apply_force_at_local_point(force, point)
        c += 1

def GameMechanics(obj):
    Throttle(obj)
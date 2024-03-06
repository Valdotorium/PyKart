import pygame
import pymunk

def simulate(obj, fps):
    obj.space.step(1/fps)
    pygame.draw.polygon(obj.screen, (0,0,0),obj.body_floor_size)
    pygame.draw.circle(obj.screen,(200,0,100), obj.body_ball1.position, obj.body_ball1_size)
def setup(obj):
    #physics simulation tuns in a 1000 x 600 px space and will be scaled
    obj.space = pymunk.Space()#creating the space
    obj.space.gravity = (0, 98)
    #static floor of the simulation
    obj.body_floor = pymunk.Body(1, 100, body_type=pymunk.Body.STATIC)
    obj.body_floor.position = (0,0)
    

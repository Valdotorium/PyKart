import pygame
import pymunk

def simulate(obj, fps):
    obj.space.step(1/fps)
    #draeing the poligon with the list of points obj.GroundPolygon
    pygame.draw.polygon(obj.screen, (0,0,0),obj.GroundPolygon)
    pygame.draw.circle(obj.screen,(200,0,100),( obj.ball.position[0] + obj.X_Position, obj.ball.position[1] + obj.Y_Position), 10)
    #pygame.draw.circle(obj.screen,(200,0,100), obj.body_ball1.position, obj.body_ball1_size)
def setup(obj):
    #physics simulation tuns in a 1000 x 600 px space and will be scaled
    obj.space = pymunk.Space()#creating the space
    obj.space.gravity = (0, 98)
    #static floor of the simulation
    obj.body_floor = pymunk.Body(1, 100, body_type=pymunk.Body.STATIC)
    obj.body_floor.position = (0,0)
    obj.space.add(obj.body_floor)
    obj.ball = pymunk.Body(1, 100, body_type=pymunk.Body.DYNAMIC)
    obj.ball.position = (100, 0)
    obj.ball.shape=pymunk.Circle(obj.ball, 10)
    obj.space.add(obj.ball)
def RefreshPolygon(obj):
    print(f"initializing ground poly with vertices: ", obj.GroundPolygon)
    obj.body_floor.shape = pymunk.Poly(obj.body_floor, obj.GroundPolygon)


    

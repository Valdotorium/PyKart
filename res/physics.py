import pygame
import pymunk
from .fw import fw as utils
def draw(obj):
    pass
def PhysDraw(obj):
    c = 0
    while c < len(obj.Vehicle):
        if obj.Vehicle[c]!= None:
            PartJoints = obj.Vehicle[c]["Joints"]
            PartPosition = obj.Vehicle[c]["Pos"]
            #draw a box with the parts size at part position       
            HitboxOfPart = obj.Vehicle[c]["Hitbox"]

            #defining shapes of hitboxes
            if HitboxOfPart["Type"] == "Rect":
                HitboxVertices = []
                #take current position of THE PYMUNK BODY and create vertices with them



            elif HitboxOfPart["Type"] == "Circle":
                HitboxPosition = utils.AddTuples(PartPosition, HitboxOfPart["Pos"])
                
            elif HitboxOfPart["Type"] == "Poly":
                #the same as in rect
                pass
                
        c += 1
def simulate(obj, fps):
    obj.space.step(1/fps)
    #draeing the poligon with the list of points obj.GroundPolygon
    pygame.draw.polygon(obj.screen, (0,0,0),obj.GroundPolygon)
    #pygame.draw.circle(obj.screen,(200,0,100), obj.body_ball1.position, obj.body_ball1_size)
    #draw(obj.Vehicle) <--will be used for textures later
    PhysDraw(obj)
def Oldsetup(obj):
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
def OldRefreshPolygon(obj):
    print(f"initializing ground poly with vertices: ", obj.GroundPolygon)
    obj.body_floor.shape = pymunk.Poly(obj.body_floor, obj.GroundPolygon)
def setup(obj):
    obj.space = pymunk.Space()#creating the space
    obj.space.gravity = (0, 98)
    #static floor of the simulation
    obj.body_floor = pymunk.Body(1, 100, body_type=pymunk.Body.STATIC)
    obj.body_floor.position = (0,0)
    obj.body_floor.shape = pymunk.Poly(obj.body_floor, obj.GroundPolygon)
    obj.space.add(obj.body_floor)
def TransferStage(obj):
    obj.gm = "game"
    obj.PhysicsOutputData = []
    obj.PymunkBodies = []
    #creating hitboxes
    c = 0
    while c < len(obj.Vehicle):
        if obj.Vehicle[c]!= None:
            PartJoints = obj.Vehicle[c]["Joints"]
            PartPosition = obj.Vehicle[c]["Pos"]
            #draw a box with the parts size at part position
            
            HitboxOfPart = obj.Vehicle[c]["Hitbox"]
            
            hitbox_body = pymunk.Body(1,100,body_type=pymunk.Body.DYNAMIC)
            hitbox_body.position = utils.AddTuples(PartPosition, HitboxOfPart["Pos"])
            #the following variables can be used for drawing the hitboxes
            hitbox_body.properties = {"Type":HitboxOfPart["Type"],
                                      "Pos":HitboxOfPart["Pos"]
                                      }
            obj.PhysicsOutputData.append({"Type":HitboxOfPart["Type"],
                                      "Pos":HitboxOfPart["Pos"]
                                      })
            HitboxPosition = utils.AddTuples(PartPosition, HitboxOfPart["Pos"])
            #defining shapes of hitboxes
            if HitboxOfPart["Type"] == "Rect":
                HitboxVertices = []
                #top left corner
                HitboxVertices.append(HitboxPosition)
                #top right corner
                HitboxVertices.append(utils.AddTuples(HitboxPosition,(HitboxOfPart["Size"][0],0)))
                #bottom right corner
                HitboxVertices.append(utils.AddTuples(HitboxPosition,(HitboxOfPart["Size"][0],HitboxOfPart["Size"][1])))
                #bottom left corner
                HitboxVertices.append(utils.AddTuples(HitboxPosition , (0,HitboxOfPart["Size"][1])))
                print("Hitbox (rect)vertices for part: ",c," : ", HitboxVertices)
                obj.PhysicsOutputData[c]["Size"] = HitboxVertices
                hitbox_shape = pymunk.Poly(hitbox_body, HitboxVertices)
                obj.space.add(hitbox_body)
                obj.PymunkBodies.append(hitbox_body)

            elif HitboxOfPart["Type"] == "Circle":
                HitboxPosition = utils.AddTuples(PartPosition, HitboxOfPart["Pos"])
                hitbox_shape = pymunk.Circle(hitbox_body, HitboxOfPart["Size"])
                print("radius of hitbox for part ",c," : ", HitboxOfPart["Size"])
                obj.PhysicsOutputData[c]["Size"] = [HitboxPosition,HitboxOfPart["Size"]]
                obj.space.add(hitbox_body)
                obj.PymunkBodies.append(hitbox_body)
            elif HitboxOfPart["Type"] == "Poly":
                cc = 0
                HitboxPosition = utils.AddTuples(PartPosition, HitboxOfPart["Pos"])
                HitboxVertices = []
                while cc < len(HitboxOfPart["Size"]):
                    HitboxVertices.append(utils.AddTuples(HitboxPosition, HitboxOfPart["Size"][cc]))
                    cc += 1
                hitbox_shape = pymunk.Poly(hitbox_body, HitboxVertices)
                obj.PhysicsOutputData[c]["Size"] = HitboxVertices
                print("Hitbox (poly)vertices for part: ",c," : ", HitboxVertices)
                print("Physics output data :", obj.PhysicsOutputData)
                obj.space.add(hitbox_body)
                obj.PymunkBodies.append(hitbox_body)
                
        c += 1

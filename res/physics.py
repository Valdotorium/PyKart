import pygame
import pymunk
from .fw import fw as utils
def Draw(obj):
    c = 0
    while c < len(obj.PymunkBodies):
        #negative because it is somehow inverted
        BodyRotation = -utils.RadiansToDegrees(obj.PymunkBodies[c].angle)
        BodyPosition = obj.PymunkBodies[c].position
        print(BodyPosition)
        PartTextures = obj.PhysicsOutputData[c]["PartTextures"]
        cc = 0
        while cc < len(PartTextures):
            Image = PartTextures[cc]["Image"]
            #getting the actual image object:
            Image = obj.textures[Image]
            Position = utils.AddTuples(BodyPosition, PartTextures[cc]["Pos"])
            Rotation = BodyRotation
            Image = pygame.transform.scale(Image, PartTextures[cc]["Size"])
            Image = pygame.transform.rotate(Image, Rotation)
            obj.screen.blit(Image, Position)
            cc += 1
        c+=1
def PhysDraw(obj):
    c = 0
    while c < len(obj.Vehicle):
        if obj.Vehicle[c]!= None:
            PartJoints = obj.Vehicle[c]["Joints"]
            PartBody = obj.PymunkBodies[c]
            PartPosition = PartBody.position

            #draw a box with the parts size at part position       
            HitboxOfPart = obj.Vehicle[c]["Hitbox"]

            #defining shapes of hitboxes
            if HitboxOfPart["Type"] == "Rect":
                #take current position of THE PYMUNK BODY and create vertices with them
                pygame.draw.rect(obj.screen, (200,150,150), (PartPosition[0], PartPosition[1], HitboxOfPart["Size"][0], HitboxOfPart["Size"][1]))

            elif HitboxOfPart["Type"] == "Circle":
                HitboxPosition = PartPosition
                pygame.draw.circle(obj.screen, (200,150,150), HitboxPosition, HitboxOfPart["Size"])
                
            elif HitboxOfPart["Type"] == "Poly":
                #the same as in rect
                cc = 0
                Vertices = []
                while cc < len(HitboxOfPart["Size"]):
                    Vertices.append((PartPosition[0] + HitboxOfPart["Size"][cc][0], PartPosition[1] + HitboxOfPart["Size"][cc][1]))
                    cc += 1

                pygame.draw.polygon(obj.screen, (200,150,150), Vertices)
                   
        c += 1
def simulate(obj, fps):
    obj.space.step(1/fps)
    #draeing the poligon with the list of points obj.GroundPolygon
    pygame.draw.polygon(obj.screen, (0,0,0),obj.GroundPolygon)
    #pygame.draw.circle(obj.screen,(200,0,100), obj.body_ball1.position, obj.body_ball1_size)
    #draw(obj.Vehicle) <--will be used for textures later
    #PhysDraw(obj)
    Draw(obj)
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
    obj.body_floor.shape.friction = 0.8
    obj.body_floor.shape.elasticity = 0.1
    obj.space.add(obj.body_floor, obj.body_floor.shape)
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
                                      "Pos":HitboxOfPart["Pos"],
                                      "PartName": obj.Vehicle[c]["name"],
                                      "PartTextures": obj.Vehicle[c]["Textures"]
                                      }
            obj.PhysicsOutputData.append({"Type":HitboxOfPart["Type"],
                                      "Pos":HitboxOfPart["Pos"],
                                      "PartName": obj.Vehicle[c]["name"],
                                      "PartTextures": obj.Vehicle[c]["Textures"]
                                      })
            HitboxPosition = HitboxOfPart["Pos"]
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
                obj.PymunkBodies.append(hitbox_body)

            elif HitboxOfPart["Type"] == "Circle":
                HitboxPosition = utils.AddTuples(PartPosition, HitboxOfPart["Pos"])
                hitbox_shape = pymunk.Circle(hitbox_body, HitboxOfPart["Size"])
                print("radius of hitbox for part ",c," : ", HitboxOfPart["Size"])
                obj.PhysicsOutputData[c]["Size"] = [HitboxPosition,HitboxOfPart["Size"]]
                obj.PymunkBodies.append(hitbox_body)
            elif HitboxOfPart["Type"] == "Poly":
                cc = 0
                HitboxPosition = utils.AddTuples(PartPosition, HitboxOfPart["Pos"])
                HitboxVertices = []
                while cc < len(HitboxOfPart["Size"]):
                    HitboxVertices.append(utils.AddTuples(HitboxPosition, HitboxOfPart["Size"][cc]))
                    cc += 1
                hitbox_shape = pymunk.Poly(hitbox_body, HitboxOfPart["Size"])
                obj.PhysicsOutputData[c]["Size"] = HitboxVertices
                print("Hitbox (poly)vertices for part: ",c," : ", HitboxVertices)
                print("Physics output data :", obj.PhysicsOutputData)
                obj.PymunkBodies.append(hitbox_body)

            hitbox_shape.mass = obj.Vehicle[c]["Properties"]["Weight"]
            hitbox_shape.elasticity = obj.Vehicle[c]["Properties"]["Bounciness"]
            hitbox_shape.friction = obj.Vehicle[c]["Properties"]["Friction"]
            obj.space.add(hitbox_body, hitbox_shape)
        c += 1
    

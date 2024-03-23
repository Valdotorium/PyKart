import pygame
import pymunk
import pymunk.pygame_util
from .fw import fw as utils
import pymunk.constraints
import random

def Draw(obj):
    c = 0
    
    obj.TransferredPolygon = []
    #print("GP:", obj.GroundPolygon)
    while c < len(obj.GroundPolygon):
        obj.TransferredPolygon.append(utils.AddTuples(obj.GroundPolygon[c], (-obj.X_Position, -obj.Y_Position)))
        c += 1
    pygame.draw.polygon(obj.screen, (0,0,0),obj.TransferredPolygon)
    obj.body_floor.shape.update
    c = 0
    #obj.space.debug_draw(obj.draw_options)
    while c < len(obj.PymunkBodies):
        #negative because it is somehow inverted
        BodyRotation = -utils.RadiansToDegrees(obj.PymunkBodies[c].angle)
        #scrolling camera?
        BodyPosition = (obj.PymunkBodies[c].position[0] - obj.X_Position, obj.PymunkBodies[c].position[1] - obj.Y_Position)
        #print(BodyPosition,  BodyRotation)
        PartTextures = obj.PhysicsOutputData[c]["PartTextures"]
        cc = 0
        while cc < len(PartTextures):
            Image = PartTextures[cc]["Image"]
            #getting the actual image object:
            Image = obj.textures[Image]
            Position = utils.AddTuples(BodyPosition, PartTextures[cc]["Pos"])
            Rotation = BodyRotation
            #many fixes need to be done here
            Image = pygame.transform.scale(Image, PartTextures[cc]["Size"])
            Image = pygame.transform.rotate(Image, Rotation)
            #applying rotation 
            #rectangle for part rotation cuz it works somehow
            texture_rect = Image.get_rect(center = Position)
            obj.screen.blit(Image, texture_rect)
            cc += 1
        c+=1

def PhysDraw(obj):
    obj.space.debug_draw(obj.draw_options)
def CheckJoints(obj):
    #checking the latest impulse divided by fps
    #if the impulse exceeds a set limit, the joint breaks
    c = 0
    while c < len(obj.PymunkJoints) and c < len(obj.VehicleJoints):
        #TODO: #6 
        #Fix a bug where the list index is OOR, because items maybe get removed asynchronously. check.
        if obj.PymunkJoints[c]!= None:
            JointImpulse = obj.PymunkJoints[c].impulse
            ImpulseLimit = obj.VehicleJoints[c]["JointData"]["BreakPoint"]
            #print(len(obj.PymunkJoints), len(obj.VehicleJoints))
            #print("Impulse of joint ", c, ":", JointImpulse)
            if JointImpulse > ImpulseLimit:
                print("JointImpulse of joint ", c, "(", JointImpulse, ") was too high, it broke.")
                VolumeFactor = JointImpulse / ImpulseLimit
                Sounds = obj.VehicleJoints[c]["SoundData"]
                r = random.randint(0, len(Sounds) -1)
                Sound = Sounds[r][0]
                print(Sound)
                Sound = obj.sounds[Sound]
                print(Sound)
                Sound.set_volume(Sounds[r][1] * VolumeFactor)
                pygame.mixer.Sound.play(Sound)
                obj.space.remove(obj.PymunkJoints[c])
                obj.VehicleJoints[c] = None
                obj.PymunkJoints[c] = None
            elif JointImpulse > ImpulseLimit/3:
                VolumeFactor = JointImpulse / ImpulseLimit
                Sounds = obj.VehicleJoints[c]["SoundData"]
                r = random.randint(0, len(Sounds) -1)
                Sound = Sounds[r][0]
                print(Sound)
                Sound = obj.sounds[Sound]
                print(Sound)
                Sound.set_volume(Sounds[r][1] * VolumeFactor)
                pygame.mixer.Sound.play(Sound)

                
        c += 1
def simulate(obj, fps):
    obj.space.step(1/fps)
    #draeing the poligon with the list of points obj.GroundPolygon
    #pygame.draw.circle(obj.screen,(200,0,100), obj.body_ball1.position, obj.body_ball1_size)
    #draw(obj.Vehicle) <--will be used for textures later
    Draw(obj)
    #PhysDraw(obj)
    CheckJoints(obj)
def OldRefreshPolygon(obj):
    print(f"initializing ground poly with vertices: ", obj.GroundPolygon)
    obj.body_floor.shape = pymunk.Poly(obj.body_floor, obj.GroundPolygon)

def setup(obj):
    Env = obj.Environment
    obj.space = pymunk.Space()#creating the space
    obj.space.gravity = Env["Gravity"]
    #static floor of the simulation
    utils.CreateGroundPolygon(obj, Env)
    obj.RotationOfSelectedPart = 0
    obj.VehicleMotorPower = 0
    obj.VehicleFuel = 0
    obj.VehicleFuelUse = 0

def TransferStage(obj):
    obj.gm = "game"
    obj.PhysicsOutputData = []
    obj.PymunkBodies = []
    obj.VehicleOriginalIndexes = []
    #storing types  of parts and indexes of their bodies in PymunkBodies, used for game calculations
    obj.VehicleTypes = []
    #vehicle without nonetype objects
    obj.NewVehicle = []
    #creating hitboxes
    c = 0
    rc = 0
    while c < len(obj.Vehicle):
        if obj.Vehicle[c]!= None:
            #creating the joints and hitboxes ------------------------------------------------------------------------------------------------
            PartJoints = obj.Vehicle[c]["Joints"]
            PartPosition = obj.Vehicle[c]["Pos"]
            #draw a box with the parts size at part position
            HitboxOfPart = obj.Vehicle[c]["Hitbox"]
            #applying rotation
            Angle = -utils.DegreesToRadians(obj.Vehicle[c]["Rotation"])
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
                                      "Center": obj.Vehicle[c]["Center"],
                                      "PartTextures": obj.Vehicle[c]["Textures"]
                                      })
            HitboxPosition = HitboxOfPart["Pos"]
            #defining shapes of hitboxes
            if HitboxOfPart["Type"] == "Rect":
                #centering the Hitbox
                HitboxPosition = utils.SubstractTuples(HitboxPosition, obj.Vehicle[c]["Center"])
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
                obj.PhysicsOutputData[rc]["Size"] = HitboxVertices
                hitbox_shape = pymunk.Poly(hitbox_body, HitboxVertices)
                hitbox_body.angle = Angle
                obj.PymunkBodies.append(hitbox_body)

            elif HitboxOfPart["Type"] == "Circle":
                #centering the body
                hitbox_body.position = utils.SubstractTuples(hitbox_body.position,obj.Vehicle[c]["Center"])
                HitboxPosition = utils.AddTuples(PartPosition, HitboxOfPart["Pos"])
                #centering the Hitbox
                HitboxPosition = utils.SubstractTuples(HitboxPosition, obj.Vehicle[c]["Center"])
                hitbox_shape = pymunk.Circle(hitbox_body, HitboxOfPart["Size"])
                print("radius of hitbox for part ",c," : ", HitboxOfPart["Size"])
                obj.PhysicsOutputData[rc]["Size"] = [HitboxPosition,HitboxOfPart["Size"]]
                hitbox_body.angle = Angle
                obj.PymunkBodies.append(hitbox_body)
            elif HitboxOfPart["Type"] == "Poly":
                cc = 0
                HitboxPosition = HitboxOfPart["Pos"]
                HitboxVertices = []
                while cc < len(HitboxOfPart["Size"]):
                    VerticePos  = utils.SubstractTuples(HitboxPosition, obj.Vehicle[c]["Center"])
                    HitboxVertices.append(utils.AddTuples(VerticePos, HitboxOfPart["Size"][cc]))
                    cc += 1
                hitbox_shape = pymunk.Poly(hitbox_body, HitboxVertices)
                obj.PhysicsOutputData[rc]["Size"] = HitboxVertices
                print("Hitbox (poly)vertices for part: ",c," : ", HitboxVertices)
                #applying rotation
                hitbox_body.angle = Angle
                obj.PymunkBodies.append(hitbox_body)

            hitbox_shape.mass = obj.Vehicle[c]["Properties"]["Weight"]
            hitbox_shape.elasticity = obj.Vehicle[c]["Properties"]["Bounciness"]
            hitbox_shape.friction = obj.Vehicle[c]["Properties"]["Friction"]
            #different Collision Categories ------------------------------------------------------------------------------------------------    
            #default (all)
            CategoryNum = 4
            CategoryMask = 7
            #"All" collides with everything
            if HitboxOfPart["CollisionType"] == "Full":
                CategoryNum = 1
                CategoryMask = 5
                #collides with everything except "Semi"
            if HitboxOfPart["CollisionType"] == "Semi":
                CategoryNum = 2
                CategoryMask = 6
                #collides with everything except "Full", used in wheels
            hitbox_shape.filter = pymunk.ShapeFilter(categories = CategoryNum, mask = CategoryMask)
            obj.space.add(hitbox_body, hitbox_shape)
            #rc is a counter value for all parts that are != Nine to prevent IOOR errors
            rc += 1
            obj.VehicleOriginalIndexes.append(c)
            obj.VehicleTypes.append((obj.Vehicle[c]["Type"], c))
            obj.NewVehicle.append(obj.Vehicle[c])
            #Assigning Values, such as motor power and fuel etc ----------------------------------------------------------------
        c += 1
    c = 0
    rc = 0
    print("VehicleTypes: ", obj.VehicleTypes)
    obj.PymunkJoints = []
    #print("VehicleJoints: " + str(obj.VehicleJoints))
    #oV[c] = some item c in obj.Vehicle
    #format of VehicleJoints [{JoinedParts: [oV[c],oV[c]], JointData:{},PositionData: [Vec2d,Vec2d]}]
    while c < len(obj.VehicleJoints):
        if obj.VehicleJoints[c] != None:
            PartnerA = obj.VehicleJoints[c]["JoinedParts"][0]
            IndexTypePartnerA = PartnerA
            PartnerB = obj.VehicleJoints[c]["JoinedParts"][1]
            IndexTypePartnerB = PartnerB
            if obj.Vehicle[PartnerA] != None and obj.Vehicle[PartnerB] != None:
                #the size of the hitbox of PartnerA / 2
                AnchorA = utils.RotateVector(obj.Vehicle[PartnerA]["Hitbox"]["Anchor"], -obj.Vehicle[PartnerA]["Rotation"])
                Vector = utils.RotateVector(obj.Vehicle[PartnerA]["Center"], -obj.Vehicle[PartnerA]["Rotation"])
                AnchorA = utils.SubstractTuples(AnchorA, Vector)
                #the size of the hitbox of PartnerB / 2
                AnchorB = utils.RotateVector(obj.Vehicle[PartnerB]["Hitbox"]["Anchor"], -obj.Vehicle[PartnerB]["Rotation"])
                #finding the indexes of joined parts in PymunkBodies
                PartnerA = obj.VehicleOriginalIndexes.index(PartnerA)
                PartnerB = obj.VehicleOriginalIndexes.index(PartnerB)
                PartnerA = obj.PymunkBodies[PartnerA]
                PartnerB = obj.PymunkBodies[PartnerB]
                JointData = obj.VehicleJoints[c]["JointData"]
                JointType = JointData["Type"]
                if JointType == "Spring":

                    print("Creating SpringJoint between anchors:",AnchorA, AnchorB)
                    Joint = pymunk.constraints.DampedSpring(PartnerA,PartnerB,AnchorA,AnchorB, JointData["Data"]["Distance"], JointData["Data"]["Stiffness"], JointData["Data"]["Damping"])
                    obj.PymunkJoints.append(Joint)
                    obj.space.add(Joint)
                    Joint = pymunk.constraints.GrooveJoint(PartnerA, PartnerB, AnchorA, utils.AddTuples(AnchorA,(utils.RotateVector((0,JointData["Data"]["Distance"]), -obj.Vehicle[IndexTypePartnerB]["Rotation"]))), AnchorB)
                    obj.PymunkJoints.append(Joint)
                    obj.space.add(Joint)

                if JointType == "Solid":
                    #relative position of the pivot joint t the position of PartnerA
                    PivotPoint = obj.VehicleJoints[c]["PositionData"][0]
                    Joint = pymunk.constraints.PivotJoint(PartnerA,PartnerB,PivotPoint)
                    Joint.collide_bodies = True
                    print("Creating PivotJoint at position:",PivotPoint)
                    obj.PymunkJoints.append(Joint)
                    obj.space.add(Joint)
        c += 1

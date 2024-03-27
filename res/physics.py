import pygame
import pymunk
import pymunk.pygame_util
from .fw import fw as utils
import pymunk.constraints
import random
import pyglet.media
import os
from .interactions import interactions as interactions


"""IMPORTANT NOTE: Because i did not implement vehicle parts as objects :/,
the game now gets managed using parallel lists. That means, a part is represented by indexes in lists.
So, for example, list index 2 in obj.PymunkBodies, obj.NewVehicle and obj.VehicleTypes refers to the same part
Here a list of lists that are compatible with each other:

obj.Vehicle is not compatible with anything, as well as obj.VehicleJoints

obj.NewVehicle, obj.PymunkBodies, obj.VehicleTypes (and maybe obj.PartData if i add that)refer to the same body

obj.NewVehicleJoints and obj.PymunkJoints refer to the same joints

How to for example get the parts a joint links:
obj.NewVehicleJoints["JoinedParts"] is a tuple containing the parts a joint is linked with.
However, there currently is no way of finding out to which joint a part is connected, so game mechanics are currently
build around joints.
sorry and will do better in the next game, Valdotorium, 24/3/2024"""
#mechanics

"""Function that makes wheels go brrrrrrr"""
def ApplyThrottle(obj, WheelPart, Force):
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
    c = WheelPart
    force = [obj.Throttle * Force,0]
    point = (0, -obj.NewVehicle[c]["Center"][1])
    obj.PymunkBodies[c].apply_force_at_local_point(force, point)
"""Making wheels connected to motors spin"""
def Engine(obj,EnginePart, WheelPart):
    #TODO: for more features: store the obj.NewVehicle as a list of Part objects (new class),
    #for easier value management of individual parts
    if obj.Throttle != 0:
        IndexOfWheelBody = obj.NewVehicle.index(WheelPart)
        EnginePower = EnginePart["Properties"]["Power"] * WheelPart["Properties"]["Force"]
        ApplyThrottle(obj, IndexOfWheelBody, EnginePower)
#preventing things from spinning too fast
def LimitAngularVelocity(body):
    if -200 < body.angular_velocity < 200:
        body.angular_velocity = body.angular_velocity * 0.9984
    else:
        body.angular_velocity = body.angular_velocity * 0.9956
def DisplayDistance(obj):
    x = obj.X_Position + 30
    text = str(round(x / 32)) + " M"
    obj.screen.blit(obj.largefont.render(text, True, (220,220,220)), (140,obj.dimensions[1] -80))
#physics
def DrawBackground(obj):
    c = 0
    #check this function for mistakes(#10)
    obj.TransferredPolygon = []
    #print("GP:", obj.GroundPolygon)
    while c < len(obj.GroundPolygon):
        obj.TransferredPolygon.append(utils.MultiplyTuple(utils.AddTuples(obj.GroundPolygon[c], (0, -obj.Y_Position)), obj.GameZoom))
        c += 1
    obj.TransferredPolygon.append((obj.GroundPolygon[-1][0], 55000))
    obj.TransferredPolygon.append((0, 55000))

    #print("Transferred polygon: ", obj.TransferredPolygon)
    #invert y of the last two points
    obj.TransferredPolygon[-2] = list(obj.TransferredPolygon[-2])
    obj.TransferredPolygon[-2][1] = -obj.TransferredPolygon[-2][1]
    obj.TransferredPolygon[-1] = list(obj.TransferredPolygon[-1])
    obj.TransferredPolygon[-1][1] = -obj.TransferredPolygon[-1][1]
    pygame.draw.polygon(obj.screen, (140,150,190),obj.TransferredPolygon)
    obj.body_floor.shape.update
    #colors of the ground above the ground texture
    Groundcolors = [(120, 200, 110), (170,120, 40), (150, 110, 0), (120, 100, 0)]
    #drawing lines on the edges of the ground poly
    cc = 0
    while cc < len(Groundcolors):
        CurrentColor = Groundcolors[cc]
        c = 0
        while c < len(obj.TransferredPolygon) - 3:
            pygame.draw.line(obj.screen, CurrentColor, (obj.TransferredPolygon[c][0],obj.TransferredPolygon[c][1] +cc * 35), (obj.TransferredPolygon[c+1][0],obj.TransferredPolygon[c+1][1] +cc * 35), 36)
            c += 1
        cc += 1
    #the ground texture
"""Drawing the Vehicle"""
def Draw(obj):
    #drawing the background
    DrawBackground(obj)
    c = 0
    #obj.space.debug_draw(obj.draw_options)
    while c < len(obj.PymunkBodies):
        LimitAngularVelocity(obj.PymunkBodies[c])
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
            Position = utils.AddTuples(utils.MultiplyTuple(BodyPosition, obj.GameZoom), utils.MultiplyTuple(PartTextures[cc]["Pos"], obj.GameZoom))
            Rotation = BodyRotation
            #many fixes need to be done here
            Image = pygame.transform.scale(Image, utils.MultiplyTuple(PartTextures[cc]["Size"], obj.GameZoom))
            Image = pygame.transform.rotate(Image, Rotation)
            #applying rotation 
            #rectangle for part rotation cuz it works somehow
            texture_rect = Image.get_rect(center = Position)
            obj.screen.blit(Image, texture_rect)
            cc += 1
        c+=1
    #calculating rpm using some random variables
    obj.rpm = int(obj.VehicleSpeed * 10) + int(obj.Throttle * 75) + random.randint(896, 904)
    #drawing speed and rpm display
    obj.SpeedDisplay.update(obj,obj.VehicleSpeed, 0.95)
    obj.RPMDisplay.update(obj,obj.rpm, 0.045)
    #displaying distance
    DisplayDistance(obj)
    CurrentPath = os.path.dirname(os.path.realpath(os.path.dirname(__file__)))
    if -8 < obj.VehicleSpeed < 8:
        ReloadButton = interactions.ButtonArea(obj, obj.textures["ReloadButton.png"], utils.Scale(obj,(150,50)), utils.Scale(obj,[64,64]))
        if ReloadButton:
            obj.restart = True
"""Drawing the pymunk physics simulation"""
def PhysDraw(obj):
    obj.space.debug_draw(obj.draw_options)
"""Checking if joints need to be broken, playing crashing sounds, performing core game mechanics besides physics(why is this here?)"""
def CheckJoints(obj):
    #checking the latest impulse divided by fps
    #if the impulse exceeds a set limit, the joint breaks
    c = 0
    while c < len(obj.PymunkJoints) and c < len(obj.NewVehicleJoints):
        #TODO: #6 
        #Fix a bug where the list index is OOR, because items maybe get removed asynchronously. check.
        if obj.PymunkJoints[c]!= None and obj.NewVehicleJoints[c] != None:
            JointImpulse = obj.PymunkJoints[c].impulse
            ImpulseLimit = obj.NewVehicleJoints[c]["JointData"]["BreakPoint"]
            #print(len(obj.PymunkJoints), len(obj.VehicleJoints))
            #print("Impulse of joint ", c, ":", JointImpulse)
            #perform mechanics here
            #is the joint connecting an Engine and an Wheel?
            if utils.JointHasType(obj, obj.NewVehicleJoints[c], "Engine") != False and utils.JointHasType(obj, obj.NewVehicleJoints[c], "Wheel") != False:
                #if yes, perform engine mechanics with the two parts
                Engine(obj,utils.JointHasType(obj, obj.NewVehicleJoints[c], "Engine"),utils.JointHasType(obj, obj.NewVehicleJoints[c], "Wheel"))
                #mechanics.Engine(obj,utils.JointHasType(obj, obj.VehicleJoints[c], "Engine"),utils.JointHasType(obj, obj.VehicleJoints[c], "Wheel"))
            if JointImpulse > ImpulseLimit:
                print("JointImpulse of joint ", c, "(", JointImpulse, ") was too high, it broke.")
                if not obj.SoundInFrame:
                    VolumeFactor = JointImpulse / ImpulseLimit
                    Sounds = obj.VehicleJoints[c]["SoundData"]
                    #selecting a random sounds from a list of sounds
                    r = random.randint(0, len(Sounds) -1)
                    Sound = Sounds[r][0]
                    #get the sound object
                    Sound = obj.sounds[Sound]
                    #create a player for it
                    obj.SoundInFrame = True
                    Player = Sound.play()
                    #setting the players volume
                    if Sounds[r][1]*VolumeFactor > 0.99:
                        Player.volume = 1
                    else:
                        Player.volume = Sounds[r][1] * VolumeFactor
                    #playing the sound object
                    print("latest played sound:", Sounds[r][0])
                    Player.play()
                obj.space.remove(obj.PymunkJoints[c])
                obj.NewVehicleJoints[c] = None
                obj.VehicleJoints[c] = None
                obj.PymunkJoints[c] = None
            elif JointImpulse > ImpulseLimit/3.7:
                if not obj.SoundInFrame:
                    VolumeFactor = JointImpulse / ImpulseLimit
                    Sounds = obj.VehicleJoints[c]["SoundData"]
                    #selecting a random sounds from a list of sounds
                    r = random.randint(0, len(Sounds) -1)
                    Sound = Sounds[r][0]
                    #get the sound object
                    Sound = obj.sounds[Sound]
                    #create a player for it
                    obj.SoundInFrame = True
                    Player = Sound.play()
                    #setting the players volume
                    if Sounds[r][1]*VolumeFactor > 0.99:
                        Player.volume = 1
                    else:
                        Player.volume = Sounds[r][1] * VolumeFactor
                    #playing the sound object
                    print("latest played sound:", Sounds[r][0])
                    Player.play()
        c += 1
"""The pymunk physics simulation"""
def simulate(obj, fps):
    Env = obj.Environment
    utils.CreateGroundPolygon(obj, Env)
    obj.SoundInFrame = False
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
"""Setting some variables"""
def setup(obj):
    obj.GameZoom = 1
    obj.Environment = obj.biomes[obj.SelectedEnvironment]
    Env = obj.Environment
    obj.space = pymunk.Space()#creating the space
    obj.space.gravity = Env["Gravity"]
    #static floor of the simulation
    obj.RotationOfSelectedPart = 0
    obj.VehicleMotorPower = 0
    obj.VehicleFuel = 0
    obj.VehicleFuelUse = 0
    obj.rpm = 0

    #initialize speed and rpm display
    obj.SpeedDisplay = utils.Display(obj, "Speed_display.png",(160,obj.dimensions[1]-120), 315, 1.6)
    obj.RPMDisplay = utils.Display(obj, "Rpm_display.png",(obj.dimensions[0] - 160,obj.dimensions[1]-120), 315, 1.6)
"""Function for translating the old data stored in obj.Vehicle and obj.VehicleJoints into  pymunk joints and bodies.
Creates obj.NewVehicle, obj.VehicleTypes, obj.NewVehicleJoints, obj.PymunkBodies, obj.PymunkJoints (versions of the old data with
"None" objects removed"""
def TransferStage(obj):
    obj.gm = "game"
    obj.PhysicsOutputData = []
    obj.PymunkBodies = []
    obj.VehicleOriginalIndexes = []
    #storing types  of parts and indexes of their bodies in PymunkBodies, used for game calculations
    obj.VehicleTypes = []
    #vehicle without nonetype objects
    obj.NewVehicle = []
    obj.NewVehicleJoints = []
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
                obj.NewVehicleJoints.append(obj.VehicleJoints[c])
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
                    print("Vector of grrove:",(AnchorA,(utils.RotateVector((0,JointData["Data"]["Distance"]), -(obj.Vehicle[IndexTypePartnerB]["Rotation"]- obj.Vehicle[IndexTypePartnerA]["Rotation"])))) )
                    Joint = pymunk.constraints.GrooveJoint(PartnerA, PartnerB, AnchorA, utils.AddTuples(AnchorA,(utils.RotateVector((0,JointData["Data"]["Distance"]), -(obj.Vehicle[IndexTypePartnerB]["Rotation"]- obj.Vehicle[IndexTypePartnerA]["Rotation"])))), AnchorB)
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

    #convenient vehicle placement 
    

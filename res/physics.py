import pygame
import pymunk
import copy
import pymunk.pygame_util
from .fw import fw as utils
import pymunk.constraints
import random
import pyglet.media
import os
from .interactions import interactions as interactions
from . import procedural
from . import particles
from. import sounds


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

def LimitThrottle(obj):
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
        obj.Throttle = obj.Throttle *(1-0.04 / obj.fpsFactor)
def ApplyThrottle(obj, WheelPart, Force):
    #apply forces to pymunk bodies
    c = WheelPart
    force = obj.Throttle * Force
    point = (0, -obj.NewVehicle[c]["Center"][1])
    obj.PymunkBodies[c].torque = 25 * force 
"""Making wheels connected to motors spin"""
def Engine(obj,EnginePart, WheelPart):
    #TODO: for more features: store the obj.NewVehicle as a list of Part objects (new class),
    #for easier value management of individual parts
    if obj.Throttle != 0:
        IndexOfWheelBody = obj.NewVehicle.index(WheelPart)
        EnginePower = EnginePart["Properties"]["Power"] * WheelPart["Properties"]["Force"] * (WheelPart["Properties"]["Weight"] / 28)
        ApplyThrottle(obj, IndexOfWheelBody, EnginePower)
@utils.timing_val
def ExecuteControlPart(obj, index):
    Properties = obj.NewVehicle[index]["Properties"]
    #stabilisators here
    if Properties["LimitsAngularVelocity"] != None:
        obj.PymunkBodies[index].angular_velocity /= Properties["LimitsAngularVelocity"]
    #thrusters here
        #"angle" property format: [Angle of thrust, AngleIsPermanent, Point relative to the center of the body on which the force is applied]
        #AngleIsPermanent is "Permanent" if the angle of thrust should not be changed by the angle nof the part
    if Properties["Thrust"] != None:
        #print(obj.Throttle)
        if obj.Throttle > 15:
            Thrust = (Properties["Thrust"] / 100) * obj.Throttle
            Angle = utils.DegreesToRadians(Properties["Angle"][0])
            if Properties["Angle"][1] != "Permanent":
                Angle += obj.PymunkBodies[index].angle
            obj.PymunkBodies[index].apply_impulse_at_local_point(utils.RotateVector((Thrust, 0), Angle), Properties["Angle"][2])

            particleCount = round(obj.Throttle / 34) + random.randint(-1,1)

            if Properties["Thrust"] < 500:
                particles.RedFlame(obj, index, True, Properties["Angle"][2], particleCount)
            else:
                particles.BlueFlame(obj, index, True, Properties["Angle"][2], particleCount)

#preventing things from spinning too fast
def LimitAngularVelocity(body,obj):
    if not obj.isWeb:
        if -160 < body.angular_velocity < 160:
            body.angular_velocity = body.angular_velocity * (1-0.0022 / obj.fpsFactor)
        else:
            body.angular_velocity = body.angular_velocity * (1-0.0058 / obj.fpsFactor)
    else:
        body.angular_velocity = body.angular_velocity * 0.998
def DisplayDistance(obj):
    x = obj.X_Position + 10 * 32
    obj.MetersTravelled = round(x/32)
    text = str(round(x / 32)) + " M"
    obj.screen.blit(obj.largefont.render(text, True, (220,220,220)), (415,obj.dimensions[1] -200))
def UpdateParticles(obj):
    for particle in obj.particles:
        particle.update(obj)
        if not obj.isWeb:
            if particle.frame > particle.duration:
                #print("delete particle")
                obj.particles.pop(obj.particles.index(particle))
        else:
            if particle.frame > particle.duration / 2:
                #print("delete particle")
                obj.particles.pop(obj.particles.index(particle))
def DisplayEarnedMoney(obj):
    mult = round((round(obj.Environment["MoneyMultiplicator"] * obj.MetersTravelled) + obj.StuntMoneyForRide) *obj.RideMoneyMultiplier) 
    text = "+" + str(mult)
    obj.DistanceMoneyForRide = round((round(obj.Environment["MoneyMultiplicator"] * obj.MetersTravelled) + obj.StuntMoneyForRide) * obj.RideMoneyMultiplier)
    #display coin image in front of text

    CoinImage = obj.textures["coin.png"]
    CoinImage = pygame.transform.scale(CoinImage, (30,30))
    obj.screen.blit(CoinImage, (665,obj.dimensions[1] -200))
    obj.screen.blit(obj.largefont.render(text, True, (220,220,220)), (710,obj.dimensions[1] -200))
#physics
#performance killer! needs to be improved +TODO #17
def WriteTerrainAssets(obj):
    Drawrange = int(obj.dimensions[0] * 4)
    Drawrange = int(Drawrange / obj.Environment["Terrain"]["Scale"])
    x = int(obj.X_Position // obj.Environment["Terrain"]["Scale"])

    PolygonAssets = []

    Drawrange = int(obj.dimensions[0] * 1.25)
    endx = x + Drawrange
    #the polygon points between x and enx get rendered
    while x < round(endx) and endx < len(obj.Terrain):
        Asset = obj.TerrainAssets[x]

        PolygonAssets.append(Asset)
        #PolygonAssets format: [None, None, [AssetData], None...]
        x += 1
    obj.PolygonAssets = PolygonAssets
@utils.timing_val
def PymunkGroundPolygon(obj, Env):
    Drawrange = obj.dimensions[0] * 1.2
    Drawrange = int(Drawrange / obj.Environment["Terrain"]["Scale"])
    CurrentItem = obj.X_Position // obj.Environment["Terrain"]["Scale"]
    x = int(CurrentItem)

    elasticity = Env["Physics"]["Friction"]
    friction = Env["Physics"]["Bounce"]
    while x < CurrentItem + Drawrange:
        Vertices = obj.PymunkPolygons[x]
        shape = pymunk.Poly(obj.body_floor, Vertices)
        shape.elasticity = elasticity
        shape.friction = 1-friction
        
        obj.space.add(shape)
        x += 1
    obj.space.step(1/obj.fps)

    #remove all shapes attached to obj.body_floor
    for shape in obj.body_floor.shapes:
        obj.space.remove(shape)
@utils.timing_val 
def PygamePolygons(obj):
    Drawrange = int(obj.dimensions[0] * 1.25)
    Drawrange = int(Drawrange / obj.Environment["Terrain"]["Scale"])
    CurrentItem = int(obj.X_Position // obj.Environment["Terrain"]["Scale"])
    EndItem = CurrentItem + Drawrange
    XOffset = obj.X_Position
    YOffset = obj.Y_Position
    #now draw all the pygame polygons from CurrentItem to DrawRange on the screen
    Vertices = []
    while CurrentItem < EndItem:
        Vertices.append(obj.PygamePolygons[CurrentItem])
        CurrentItem += 1
    Vertices.append((Vertices[len(Vertices)-1][0], -10000))
    Vertices.append((Vertices[0][0], -10000))

    #offset all vertices by XOffset and YOffset
    Vertices = [(x - XOffset, y - YOffset) for x, y in Vertices]

    #draw all the polygons to the screen
    pygame.draw.polygon(obj.screen, obj.Environment["Background"], Vertices)
    Vertices = Vertices[:-2]
    pygame.draw.lines(obj.screen, (20,20,20), False,Vertices, 20)
    print("drew ",Drawrange, "Polygons" )

    c = 0
    while c < len(obj.PolygonAssets) and c < len(Vertices):
        if obj.PolygonAssets[c] != None:
            Point = Vertices[c]
            AssetImage = obj.Environment["Visuals"]["Assets"][obj.PolygonAssets[c]]["image"]
            AssetImage = obj.textures[AssetImage]
            AssetSize = obj.Environment["Visuals"]["Assets"][obj.PolygonAssets[c]]["size"]
            AssetImage = pygame.transform.scale(AssetImage,AssetSize)
            AssetOffset = obj.Environment["Visuals"]["Assets"][obj.PolygonAssets[c]]["offset"]
            obj.screen.blit(AssetImage, (Point[0] + AssetOffset[0], Point[1] + AssetOffset[1]))
                            
        c += 1
def DrawMinimap(obj):

    #rewrite this, performance TODO #18
    startX = 400
    startY = 600
    sizeX = 400
    sizeY = 180
    #draw rect at startx and stary
    Surface = pygame.Surface((sizeX, sizeY))
    Surface.fill((180,180,180))
    Surface.set_alpha(180)
    obj.screen.blit(Surface, (startX, startY))

    MinimapPolygon = []
    XOffset = obj.MinimapPolygon[0][0] / 10
    YOffset = obj.MinimapPolygon[0][1] / 10 - sizeY/2
    for node in obj.MinimapPolygon:
        if node[0] < startX + sizeX * 45:
            node = list(node)
            MinimapPolygon.append((node[0] /50 + startX - XOffset, node[1] / 50 + startY - YOffset))
    #draw the minimap polygon
    c = 0
    while c < len(MinimapPolygon)-1:
        MinimapPolygon[c] = list(MinimapPolygon[c])
        MinimapPolygon[c+1] = list(MinimapPolygon[c+1])
        if MinimapPolygon[c][1] < startY:
            MinimapPolygon[c][1] = startY
        if MinimapPolygon[c+1][1] < startY:
            MinimapPolygon[c+1][1] = startY
        if MinimapPolygon[c][1] > startY + sizeY:
            MinimapPolygon[c][1] = startY + sizeY
        if MinimapPolygon[c+1][1] > startY + sizeY:
            MinimapPolygon[c+1][1] = startY + sizeY
        pygame.draw.line(obj.screen, (255,255,255), (MinimapPolygon[c][0],MinimapPolygon[c][1]), (MinimapPolygon[c+1][0],MinimapPolygon[c+1][1]), 3)
        if c == 30:
            #draw a circle at the point
            pygame.draw.circle(obj.screen, (240,160,110), (MinimapPolygon[c][0],MinimapPolygon[c][1]), 8, 7)
        c += 1
    obj.screen.blit(obj.MiniMapImage, (startX -15, startY - 15))
"""Drawing the Vehicle"""
#performance killer! needs improvements TODO #16
@utils.timing_val
def Draw(obj):
    #drawing the background
    WriteTerrainAssets(obj)
    PygamePolygons(obj)

    #DrawMinimap(obj)
    c = 0
    #obj.space.debug_draw(obj.draw_options)
    while c < len(obj.PymunkBodies):
        LimitAngularVelocity(obj.PymunkBodies[c], obj)
        #negative because it is somehow inverted
        BodyRotation = -utils.RadiansToDegrees(obj.PymunkBodies[c].angle)
        #scrolling camera?
        BodyPosition = (obj.PymunkBodies[c].position[0] - obj.X_Position, obj.PymunkBodies[c].position[1] - obj.Y_Position)
        #print(BodyPosition,  BodyRotation)
        PartTextures = obj.PhysicsOutputData[c]["PartTextures"]
        cc = 0
        while cc < len(PartTextures):
            PartTextures[cc]["Pos"] = list(PartTextures[cc]["Pos"])
            Image = PartTextures[cc]["Image"]
            #getting the actual image object:
            Image = obj.textures[Image]
            Rotation = BodyRotation
            if obj.isWeb:
                Image = pygame.transform.scale(Image, PartTextures[cc]["Size"])
                Image = pygame.transform.rotate(Image, Rotation)
                Position = utils.AddTuples(BodyPosition, utils.RotateVector(PartTextures[cc]["Pos"], -BodyRotation))
            else:
                Image = pygame.transform.scale(Image, utils.MultiplyTuple(PartTextures[cc]["Size"], obj.GameZoom))
                Image = pygame.transform.rotate(Image, Rotation)
                Position = utils.AddTuples(utils.MultiplyTuple(BodyPosition, obj.GameZoom), utils.MultiplyTuple(utils.RotateVector(PartTextures[cc]["Pos"], -BodyRotation), obj.GameZoom))
            #applying rotation 
            #rectangle for part rotation cuz it works somehow
            texture_rect = Image.get_rect(center = Position)
            obj.screen.blit(Image, texture_rect)
            #pygame.draw.circle(obj.screen, (200,200,200), Position, 6)
            cc += 1
        c+=1
    #calculating rpm using some random variables
    obj.rpm = (int(obj.VehicleSpeed * 10) + int(obj.Throttle * 75) + random.randint(896, 904)) * 1
    #drawing speed and rpm display
    obj.SpeedDisplay.update(obj,obj.VehicleSpeed, 0.95)
    obj.RPMDisplay.update(obj,obj.rpm, 0.045)
    #displaying distance

 
    DisplayDistance(obj)
    DisplayEarnedMoney(obj)
    if -14 < obj.VehicleSpeed < 10:
        ReloadButton = interactions.ButtonArea(obj, obj.textures["UnselectButton.png"], utils.Scale(obj,(150,50)), utils.Scale(obj,[64,64]))
        if ReloadButton or pygame.key.get_pressed()[pygame.K_s]:
            #add the meters travelled as money
            obj.money += (obj.DistanceMoneyForRide + obj.StuntMoneyForRide) * obj.RideMoneyMultiplier
            obj.xp += obj.MetersTravelled * obj.RideMoneyMultiplier
            obj.restart = True
            if not obj.isWeb:
                AlertSound = obj.sounds["alert.wav"]
                player = AlertSound.play()
                del(player)
"""Drawing the pymunk physics simulation"""
def PhysDraw(obj):
    obj.space.debug_draw(obj.draw_options)
"""Checking if joints need to be broken, playing crashing sounds, performing core game mechanics besides physics(why is this here?)"""
def Checkparts(obj):
    c = 0
    while c < len(obj.PymunkBodies) and c < len(obj.NewVehicle):
        if obj.NewVehicle[c]["Type"] == "Engine":
            particles.ParticleEffect(obj, "Exhaust", c)
        elif obj.NewVehicle[c]["Type"] == "Control":
            ExecuteControlPart(obj, c)
        c += 1

def CheckJoints(obj):
    #checking the latest impulse divided by fps
    #if the impulse exceeds a set limit, the joint breaks
    c = 0
    while c < len(obj.PymunkJoints) and c < len(obj.NewVehicleJoints):
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
                if obj.debug:
                    print("JointImpulse of joint ", c, "(", JointImpulse, ") was too high, it broke.")
                r = random.randint(1,4)
                if r == 1:
                    obj.TextAnimations.append(interactions.TextAnimation("CRUNCH +25", 100, obj))
                elif r == 2:
                    obj.TextAnimations.append(interactions.TextAnimation("SMASH + 25", 100, obj))
                elif r == 3:
                    obj.TextAnimations.append(interactions.TextAnimation("BONK +25", 100, obj))
                elif r == 4:
                    obj.TextAnimations.append(interactions.TextAnimation("CRACK +25", 100, obj))
                ParticlePartA = obj.NewVehicleJoints[c]["JoinedParts"][1]
                ParticlePartB = obj.NewVehicleJoints[c]["JoinedParts"][0]
                particles.ParticleEffect(obj, "Break", ParticlePartA)
                particles.ParticleEffect(obj, "Break", ParticlePartB)
                obj.space.remove(obj.PymunkJoints[c])
                obj.NewVehicleJoints[c] = None
                obj.VehicleJoints[c] = None
                obj.PymunkJoints[c] = None
                obj.StuntMoneyForRide += 25

        c += 1
def DistanceBonuses(obj):
    if obj._MetersTravelled  <= obj.NextKilometer and obj.MetersTravelled > obj.NextKilometer:
        obj.NextKilometer += 1000
        if not obj.isWeb:
            AlertSound = obj.sounds["coinbag.wav"]
            player = AlertSound.play()
            del(player)
        #extra large bonuses:
        if obj.NextKilometer == 3000:
            MoneyBonus = round((obj.NextKilometer / 10) * ((obj.NextKilometer / 4000) + 0.5)* round(obj.Environment["MoneyMultiplicator"] * 1.2))
            text = "2km Distance Bonus: +" + str(round(MoneyBonus))
        elif obj.NextKilometer == 6000:
            MoneyBonus = round((obj.NextKilometer / 10) * ((obj.NextKilometer / 4000) + 0.5)* round(obj.Environment["MoneyMultiplicator"] * 2))
            text = "5km Distance Bonus: +" + str(round(MoneyBonus))
        elif obj.NextKilometer == 11000:
            MoneyBonus = round((obj.NextKilometer / 10) * ((obj.NextKilometer / 4000) + 0.5)* round(obj.Environment["MoneyMultiplicator"] * 2.8))
            text = " 10km Distance Bonus: +" + str(round(MoneyBonus))
        elif obj.NextKilometer == 16000:
            MoneyBonus = round((obj.NextKilometer / 10) * ((obj.NextKilometer / 4000) + 0.5)* round(obj.Environment["MoneyMultiplicator"] * 3.5))
            text = " 15km Distance Bonus: +" + str(round(MoneyBonus))
        elif obj.NextKilometer == 21000:
            MoneyBonus = round((obj.NextKilometer / 10) * ((obj.NextKilometer / 4000) + 0.5)* round(obj.Environment["MoneyMultiplicator"] * 4))
            text = " 20km Distance Bonus: +" + str(round(MoneyBonus))
        elif obj.NextKilometer == 31000:
            MoneyBonus = round((obj.NextKilometer / 10) * ((obj.NextKilometer / 4000) + 0.5)* round(obj.Environment["MoneyMultiplicator"] * 3.5))
            text = " 30km Distance Bonus: +" + str(round(MoneyBonus))
        elif obj.NextKilometer == 51000:
            MoneyBonus = round((obj.NextKilometer / 10) * ((obj.NextKilometer / 4000) + 0.5)* round(obj.Environment["MoneyMultiplicator"] * 3))
            text = " 50km Distance Bonus: +" + str(round(MoneyBonus))
        else:
            MoneyBonus = round((obj.NextKilometer / 10) * ((obj.NextKilometer / 4000) + 0.5)* round(obj.Environment["MoneyMultiplicator"] * 0.8))
            text = "Distance Bonus: +" + str(round(MoneyBonus))
        obj.StuntMoneyForRide += MoneyBonus

        obj.TextAnimations.append(interactions.TextAnimation(text, 150, obj))
"""The pymunk physics simulation"""
@utils.timing_val
def simulate(obj, fps):
    obj._MetersTravelled = obj.MetersTravelled
    Env = obj.Environment
    #try:
    PymunkGroundPolygon(obj, Env)
    obj.SoundInFrame = False

    LimitThrottle(obj)
    
    #draeing the poligon with the list of points obj.GroundPolygon
    #pygame.draw.circle(obj.screen,(200,0,100), obj.body_ball1.position, obj.body_ball1_size)
    #draw(obj.Vehicle) <--will be used for textures later
    #DrawMinimap(obj)
    Draw(obj)
    UpdateParticles(obj)
    #PhysDraw(obj)
    CheckJoints(obj)
    Checkparts(obj)
    utils.DisplayMoney(obj)
    DistanceBonuses(obj)
    #except Exception as e:
    #obj.money += (obj.DistanceMoneyForRide + obj.StuntMoneyForRide) * obj.RideMoneyMultiplier
    #obj.xp += obj.MetersTravelled * obj.RideMoneyMultiplier
    #obj.restart = True
    #if not obj.isWeb:
        #AlertSound = obj.sounds["alert.wav"]
        #player = AlertSound.play()
        #del(player)
    #obj.TextAnimations.append(interactions.TextAnimation("EXCEPTION: Could not simulate physics", 150, obj))
    #print("INTERNAL ERROR: Could not simulate physics: " + str(e))

def FindFreight(obj):
    c = 0
    obj.RideMoneyMultiplier = 1
    while c < len(obj.NewVehicle):
        if obj.NewVehicle[c]!= None:
            if obj.NewVehicle[c]["Type"] == "Freight":
                obj.RideMoneyMultiplier += obj.NewVehicle[c]["Properties"]["Value"]
        c += 1
def OldRefreshPolygon(obj):
    if obj.debug:
        print(f"initializing ground poly with vertices: ", obj.GroundPolygon)
    obj.body_floor.shape = pymunk.Poly(obj.body_floor, obj.GroundPolygon)
"""Setting some variables"""
def setup(obj):
    obj.GameZoom = 1
    obj.Environment = obj.biomes[obj.SelectedEnvironment]
    obj.Environment["MoneyMultiplicator"] = round(obj.Environment["MoneyMultiplicator"])
    if obj.debug:
        print("started with env gravity:", obj.Environment["Gravity"])
    Env = obj.Environment
    obj.space = pymunk.Space()#creating the space
    obj.space.gravity = Env["Gravity"]
    #static floor of the simulation
    obj.RotationOfSelectedPart = 0
    obj.VehicleMotorPower = 0
    obj.VehicleFuel = 0
    obj.VehicleFuelUse = 0
    obj.rpm = 0
    obj.StuntMoneyForRide = 0

    #kilometerwise money bonuses
    obj.NextKilometer = 1000
    obj.MetersTravelled = 0
    obj._MetersTravelled = 0
    #initialize speed and rpm display
    obj.SpeedDisplay = utils.Display(obj, "Speed_display.png",(160,obj.dimensions[1]-120), 315, 1.6)
    obj.RPMDisplay = utils.Display(obj, "Rpm_display.png",(obj.dimensions[0] - 160,obj.dimensions[1]-120), 315, 1.6)
    obj.MiniMapImage = pygame.transform.scale(obj.textures["mapoverlay.png"],(400 + 30, 180 + 30))
    #the pymunk floor body
    obj.body_floor = pymunk.Body(1, 100, body_type=pymunk.Body.STATIC)
    obj.body_floor.position = (0,0)
    obj.space.add(obj.body_floor)

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
                if obj.debug:
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
                if obj.debug:
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
                if obj.debug:
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
            obj.VehicleTypes.append((copy.deepcopy(obj.Vehicle[c]["Type"]), c))
            obj.NewVehicle.append(copy.deepcopy(obj.Vehicle[c]))
            #Assigning Values, such as motor power and fuel etc ----------------------------------------------------------------
        c += 1
    c = 0
    rc = 0
    if obj.debug:
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
                    if obj.debug:
                        print("Creating SpringJoint between anchors:",AnchorA, AnchorB)
                    Joint = pymunk.constraints.DampedSpring(PartnerA,PartnerB,AnchorA,AnchorB, JointData["Data"]["Distance"], JointData["Data"]["Stiffness"], JointData["Data"]["Damping"])
                    obj.PymunkJoints.append(Joint)
                    obj.space.add(Joint)
                    if obj.debug:
                        print("Vector of grrove:",(AnchorA,(utils.RotateVector((0,JointData["Data"]["Distance"]), -(obj.Vehicle[IndexTypePartnerB]["Rotation"]- obj.Vehicle[IndexTypePartnerA]["Rotation"])))) )
                    Joint = pymunk.constraints.GrooveJoint(PartnerA, PartnerB, AnchorA, utils.AddTuples(AnchorA,(utils.RotateVector((0,JointData["Data"]["Distance"]), -(obj.Vehicle[IndexTypePartnerB]["Rotation"]- obj.Vehicle[IndexTypePartnerA]["Rotation"])))), AnchorB)
                    obj.PymunkJoints.append(Joint)
                    obj.space.add(Joint)

                if JointType == "Solid":
                    #relative position of the pivot joint t the position of PartnerA
                    PivotPoint = obj.VehicleJoints[c]["PositionData"][0]
                    Joint = pymunk.constraints.PivotJoint(PartnerA,PartnerB,PivotPoint)
                    Joint.collide_bodies = True
                    if obj.debug:
                        print("Creating PivotJoint at position:",PivotPoint)
                    obj.PymunkJoints.append(Joint)
                    obj.space.add(Joint)
        c += 1

    FindFreight(obj)
    text = "Freight value: " + str(obj.RideMoneyMultiplier)
    obj.RideMoneyMultiplier=round(obj.RideMoneyMultiplier)
    obj.TextAnimations.append(interactions.TextAnimation(text, 200, obj))
    #display freight value as text animation
     
    

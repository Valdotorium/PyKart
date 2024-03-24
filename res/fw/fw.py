import pygame, math
import pymunk
#some small helpers to make code shorter and maybe more radable
def getScreenSize():
    try:
        return pygame.display.get_desktop_sizes()
    except:
        raise ValueError("ERRNO_01:Could not get screen size")

def displayText(obj, text):
    #displaying text at a set position (please do not use anymore!)
    txt = obj.largefont.render(text, True, (20, 20, 20))
    obj.screen.blit(txt, (0, 300))
    pygame.display.update()
def displayTextAt(obj, text, pos):
    #displaying text at a variable position
    txt = obj.largefont.render(text, True, (20, 20, 20))
    obj.screen.blit(txt, pos)
    pygame.display.update()
def displayTextCenter(obj, text):
    #displaying text at the center of the screen, only use after the game object has been created
    txt = obj.largefont.render(text, True, (20, 20, 20))
    pos = (obj.dimensions[0] / 2 - txt.get_width() / 2, obj.dimensions[1] / 2)
    obj.screen.blit(txt, pos)
    pygame.display.update()
def clear(screen):
    #...(i wonder what that does)
    screen.fill((100,100,100))

def DecodePart(part, obj):
    #loading parts into the game
    obj.partdict[part["Name"]] = part
    obj.shopdict[part["Name"]] = {"Type" : part["Type"], "Cost":part["Cost"], "Textures":part["Textures"]}
def Scale(obj,element):
    #scaling things, fitting screen sizes, necessary for "dynamic" UI
    if type(element) == tuple:
        return (element[0] * obj.scalefactor, element[1] * obj.scalefactor)
    if type(element) == int:
        return element * obj.scalefactor
    if type(element) == float:
        return element * obj.scalefactor
    #scaling lists of vertices:
    if type(element) == list:
        return [Scale(obj,x) for x in element]
    if type(element) == dict:
        return {k:Scale(obj,v) for k,v in element.items()}
    
def AddTuples(tuple1, tuple2):
    return tuple1[0] + tuple2[0], tuple1[1] + tuple2[1]
def SubtractTuples(tuple1, tuple2):
    return tuple1[0] - tuple2[0], tuple1[1] - tuple2[1]
def MultiplyTuple(tuple1, factor):
    return tuple1[0] * factor, tuple1[1] * factor
def RadiansToDegrees(radians):
    return radians * 180 / 3.14159265359
def DegreesToRadians(degrees):
    return degrees * 3.14159265359 / 180
def Negative(*args):
    c = 0
    ReturnArgs = []
    while c < len(args):
        if type(args[c]) == tuple or type(args[c]) == list:
            cc = 0
            ReturnTuple = []
            while cc < len(args[c]):
                ReturnTuple.append(-args[c][cc])
                cc += 1
            ReturnArgs.append(ReturnTuple)
        elif type(args[c]) == int:
            ReturnArgs.append(-args[c])
        else:
            ReturnArgs.append(None)
        c += 1
    if len(ReturnArgs) > 1:
        return ReturnArgs
    else:
        return ReturnArgs[0]
def RotateVector(vector, angle):
    #angle from degrees to radians
    angle = math.radians(angle)
    sin = math.sin(angle)
    cos = math.cos(angle)
    x = vector[0]
    y = vector[1]
    nx = x * cos - y * sin
    ny = x * sin + y * cos
    return nx, ny
def SubstractTuples(tuple1, tuple2):
    return tuple1[0] - tuple2[0], tuple1[1] - tuple2[1]
def CreateGroundPolygon(obj, Env):
    obj.body_floor = pymunk.Body(1, 100, body_type=pymunk.Body.STATIC)
    obj.body_floor.position = (0,0)
    c = 0
    GroundPolygons = []
    obj.space.add(obj.body_floor)
    while c < len(obj.GroundRelief) - 1:
        VectA = obj.GroundRelief[c]
        VectB = obj.GroundRelief[c+1]
        VectAX = VectA[0]
        VectBX = VectB[0]
        #vertices for the poly, one poly for every x position in obj.GroundRelief
        Vertices = [(VectAX , 9000), (VectBX, 9000), VectB, VectA]
        obj.body_floor.shape = pymunk.Poly(obj.body_floor, Vertices)
        obj.body_floor.shape.friction = Env["Physics"]["Friction"]
        obj.body_floor.shape.elasticity = Env["Physics"]["Bounce"]
        obj.body_floor.shape.filter = pymunk.ShapeFilter(categories= 4, mask= 7)
        GroundPolygons.append(obj.body_floor.shape)
        obj.space.add(obj.body_floor.shape)
        c += 1

    #creating GroundPolygon (adding bottom edges)
    print("ground relief:",obj.GroundRelief)
    obj.GroundPolygon = obj.GroundRelief
    obj.GroundPolygon.append((obj.GroundRelief[len(obj.GroundRelief)-1][0],9000))
    obj.GroundPolygon.append((0,9000))
    print(obj.GroundPolygon)
def GetConnectedParts(obj,joint):
    #joint should come from obj.vehiclejoints
    PartA = obj.NewVehicle[joint["JoinedParts"][0]]
    PartB = obj.NewVehicle[joint["JoinedParts"][1]]
    IndexPartA = joint["JoinedParts"][0]
    IndexPartB = joint["JoinedParts"][1]
    print(IndexPartA,IndexPartB)
    return [PartA,PartB]
def JointHasType(obj,joint, type):
    #check if a joint is connected to a part of a specific type
    PartA = obj.Vehicle[joint["JoinedParts"][0]]
    PartB = obj.Vehicle[joint["JoinedParts"][1]]
    if type == PartA["Type"]:
        return PartA
    elif type == PartB["Type"]:
        return PartB
    else: 
        return False
def JointHasName(obj,joint,name):
    #check if a joint is connected to a part with a specific name
    #try to avoid using this function
    PartA = obj.NewVehicle[joint["JoinedParts"][0]]
    PartB = obj.NewVehicle[joint["JoinedParts"][1]]
    if name == PartA["Name"]:
        return PartA
    elif name == PartB["Name"]:
        return PartB
    else: 
        return False






            
import pygame, math
import pymunk
import copy

#some small helpers to make code shorter and maybe more radable
def getScreenSize():
    try:
        return pygame.display.get_desktop_sizes()
    except:
        raise ValueError("ERRNO_01:Could not get screen size")
def displayLoadText(obj, text):
    #displaying text at a set position (please do not use anymore!)
    txt = obj.largefont.render(text, True, (20, 20, 20))
    obj.window.blit(txt, (obj.window.get_width() / 2 - 50, obj.window.get_height() / 2 - 16))
    pygame.display.flip()
def displayText(obj, text):
    #displaying text at a set position (please do not use anymore!)
    txt = obj.largefont.render(text, True, (20, 20, 20))
    obj.screen.blit(txt, (0, 300))
    pygame.display.update()
def displayTextAt(obj, text, pos):
    #displaying text at a variable position
    if type(text) == str:
        txt = obj.largefont.render(text, True, (20, 20, 20))
        obj.screen.blit(txt, pos)
        pygame.display.update()
    if type(text) == list:
        pos = list(pos)
        y = pos[1]
        for i in text:
            displayTextAt(obj, i,(pos[0], y) )
            y += 30
            pygame.display.update()
def displayTextCenter(obj, text):

    #displaying text at the center of the screen, only use after the game object has been created
    if type(text) == str:
        txt = obj.largefont.render(text, True, (20, 20, 20))
        pos = (obj.dimensions[0] / 2 - txt.get_width() / 2, obj.dimensions[1] / 2)
        obj.screen.blit(txt, pos)
        pygame.display.update()
    if type(text) == list:
        txt = obj.largefont.render(text[0], True, (20, 20, 20))
        pos = (obj.dimensions[0] / 2 - txt.get_width() / 2, obj.dimensions[1] / 2)
        pos = list(pos)
        y = pos[1]
        for i in text:
            displayTextAt(obj, i,(pos[0], y) )
            y += 30
            pygame.display.update()
def clear(screen):
    #...(i wonder what that does)
    screen.fill((100,100,100))

def DecodePart(part, obj):
    #loading parts into the game
    obj.partdict[part["Name"]] = part
    #count stores how many of these parts have been purchased
    obj.partdict[part["Name"]]["Count"] = 0
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
def DivideTuple(tuple1, factor):
    return tuple1[0] / factor, tuple1[1] / factor
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
    while angle > 360:
        angle = angle - 360
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
def DisplayMoney(obj):
        #displaying the money that is in obj
        text = obj.largefont.render(str(obj.money), True, (20,20,20))
        pos = (obj.dimensions[0] * 0.09 - text.get_width() / 2, obj.dimensions[1] * 0.16)
        obj.screen.blit(text, pos)
        #drawing the hand
        Image = obj.textures["coin.png"]
        Image = pygame.transform.scale(Image, (50 ,50))
        obj.screen.blit(Image, (obj.dimensions[0] * 0.05 - text.get_width() / 2, obj.dimensions[1] * 0.17 - 16))
def CreateGroundPolygon(obj, Env):
    #TODO #10 #completely rewrite this function
    c = 0
    while c < len(obj.GroundPolygons):
        if obj.GroundPolygons[c]!= None:
            obj.space.remove(obj.GroundPolygons[c])
        c += 1
    if not obj.HasFloor:
        obj.body_floor = pymunk.Body(1, 100, body_type=pymunk.Body.STATIC)
        obj.body_floor.position = (0,0)
        obj.HasFloor = True
        obj.space.add(obj.body_floor)
    obj.GroundPolygons = []

    obj.GroundPolygon = []

    c = 0
    while c < len(obj.StaticPolygon) - 1:
        VectA = obj.StaticPolygon[c]
        VectB = obj.StaticPolygon[c+1]
        VectAX = VectA[0]
        VectBX = VectB[0]
        #vertices for the poly, one poly for every x position in obj.GroundRelief
        Vertices = [(VectAX , 55000), (VectBX, 55000), VectB, VectA]
        obj.body_floor.shape = pymunk.Poly(obj.body_floor, Vertices)
        obj.body_floor.shape.friction = Env["Physics"]["Friction"]
        obj.body_floor.shape.elasticity = Env["Physics"]["Bounce"]
        obj.body_floor.shape.filter = pymunk.ShapeFilter(categories= 4, mask= 7)
        obj.GroundPolygons.append(obj.body_floor.shape)
        obj.space.add(obj.body_floor.shape)
        c += 1
        obj.GroundPolygon.append(obj.GroundRelief[c])
    

    
def GetConnectedParts(obj,joint):
    #joint should come from obj.vehiclejoints
    PartA = obj.NewVehicle[joint["JoinedParts"][0]]
    PartB = obj.NewVehicle[joint["JoinedParts"][1]]
    IndexPartA = joint["JoinedParts"][0]
    IndexPartB = joint["JoinedParts"][1]
    #(IndexPartA,IndexPartB)
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
class Display:
    def __init__(self, obj,texture, position, maxRotation, scale):
        self.range = range
        self.maxRotation = maxRotation
        self.position = position
        self.scale = scale
        self.hand_texture = obj.textures["hand.png"]
        self.hand_texture = pygame.transform.scale(self.hand_texture, (32 * self.scale,128 * self.scale))
        self.texture = obj.textures[texture]
        self.texture = pygame.transform.scale(self.texture, (128 * self.scale, 128 * self.scale))

        
        self.position = position
    def RotateHand(self, variable, multiplicator,obj):
        NullOrientation = (0,0)
        self.HandAngle = variable * multiplicator
        self.HandAngle = math.radians(self.HandAngle)
        if self.HandAngle > math.radians(self.maxRotation):
            self.HandAngle = math.radians(self.maxRotation)
        elif self.HandAngle < -1:
            self.HandAngle = -1
        self.Handangle = -self.HandAngle
        self.HandPosition = self.position
    def update(self, obj, value, multiplicator):
        self.RotateHand(value, multiplicator,obj)
        self.HandAngle -= math.radians(90) #because of the flipped y axis of pygame

        bg_rect = self.texture.get_rect(center = self.position)
        obj.screen.blit(self.texture, bg_rect)
        texture = pygame.transform.rotate(self.hand_texture, math.degrees(-self.HandAngle))
        texture_rect = texture.get_rect(center = self.position)
            
        obj.screen.blit(texture, texture_rect)
        pygame.draw.circle(obj.screen, (20,20,20), self.position, round(74 * self.scale), round(10 * self.scale))

def DisplayXP(obj):
    text = obj.largefont.render(str(obj.xp), True, (20,20,20))
    pos = ((obj.dimensions[0] * 0.03 - text.get_width() / 2) - 2, obj.dimensions[1] * 0.22)
    textpos = (pos[0] + 70, pos[1])
    Image = obj.textures["xp.png"]
    Image = pygame.transform.scale(Image, (50,30))
    obj.screen.blit(Image, pos)
    obj.screen.blit(text, textpos)

class Credits():
    def __init__(self, obj):
        self.visible = False
        self.font = obj.font
        self.largefont = obj.largefont
        self.image = obj.textures["UI_tile_loweralpha.png"]
        self.size = (obj.dimensions[0], obj.dimensions[1])
        self.image = pygame.transform.scale(self.image, self.size)
        self.frames = 0
    
    def update(self, obj):
        if self.visible:
            self.pos = obj.dimensions[0] / 2 - self.size[0] / 2,obj.dimensions[1] / 2 - self.size[1] / 2
            obj.screen.blit(self.image, self.pos)
            text = self.largefont.render("Credits", True, (20,20,20))
            pos = ((obj.dimensions[0] * 0.5 - text.get_width() / 2) - 2, obj.dimensions[1] * 0.1)
            obj.screen.blit(text, pos)

            FreesoundContributors = [
                "TheMinkman", "qubodup", "sagetyrtle", "Lunardrive", "JustInvoke", "Troutpack", "ethanchase7744", "Romano.Tercero",
                "MarlonHJ", "wishniak", "reqMan", "PatrickLieberkind", "BaggoNotes", "dland", "plasterbrain", "LittleRobotSoundFactory",
                "cabled_mess", "tomf_"
            ]
            c = 0
            li = 1
            l = 1
            text = "Freesound Contributors"
            text = self.font.render(text, True, (20,20,20))
            pos = ((obj.dimensions[0] * 0.5 - text.get_width() / 2) - 2, obj.dimensions[1] * 0.15)
            obj.screen.blit(text, pos)
            while c < len(FreesoundContributors):
                text = self.font.render(FreesoundContributors[c], True, (20,20,20))
                pos = (obj.dimensions[0] * 0.25 * li- text.get_width() / 2, obj.dimensions[1] * 0.16 + (0.03* obj.dimensions[1] * l))
                obj.screen.blit(text, pos)
                li += 1
                if li == 4:
                    li = 1
                    l += 1
                c += 1
            CodeContributors = ["Valdotorium - programming, graphics, assets", "JoEragon - programming, assets", "ItzMooseboy - graphics","pygame - game library", "pymunk (chipmunk) - physics library", "pyglet - sound players"]
            text = "Programmers and Code contributors"
            l = 1
            c = 0
            text = self.largefont.render(text, True, (20,20,20))
            pos = ((obj.dimensions[0] * 0.5 - text.get_width() / 2) - 2, obj.dimensions[1] * 0.45)
            obj.screen.blit(text, pos)
            while c < len(CodeContributors):
                text = self.font.render(CodeContributors[c], True, (20,20,20))
                pos = (obj.dimensions[0] * 0.5 - text.get_width() / 2, obj.dimensions[1] * 0.5 + (0.04* obj.dimensions[1] * l))
                obj.screen.blit(text, pos)
                l += 1
                c += 1
            
            text = "See the app contents 'notes' folder for more credir info."
            text = self.font.render(text, True, (20,20,20))
            pos = ((obj.dimensions[0] * 0.5 - text.get_width() / 2) - 2, obj.dimensions[1] * 0.85)
            obj.screen.blit(text, pos)

            if self.frames > 200:
                text = "click to exit the credit page"
                text = self.largefont.render(text, True, (20,20,20))
                pos = ((obj.dimensions[0] * 0.5 - text.get_width() / 2) - 2, obj.dimensions[1] * 0.8)
                obj.screen.blit(text, pos)
                if pygame.mouse.get_pressed()[0]:
                    self.visible = False
                    self.frames = 0
            self.frames += 1
            


         
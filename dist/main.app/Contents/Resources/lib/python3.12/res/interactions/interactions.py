import pygame,os, random

def ButtonArea(obj, image, pos, size):
   # print("Creating a button at position " + str(pos) + " and size" + str(size))
    try:
        #resize the image to size of the button
        image = pygame.transform.scale(image, size)
        try:
            obj.screen.blit(image, pos)
        except:
            raise SyntaxError("ERRNO_04B: Invalid size parameters!")
    except:
        raise SyntaxError("ERRNO_04: could not find screen to blit on")
    if pygame.mouse.get_pressed()[0]:#
        mx, my = pygame.mouse.get_pos()

        # is the button clicked?  (is the mouse within a box at pos with size when the click occurs?)
        if mx >= pos[0] and mx <= pos[0] + size[0]:
            if my >= pos[1] and my <= pos[1] + size[1]:
                return True
            else:
                return False
        else:
            return False
def ClickArea(pos, size):
    if pygame.mouse.get_pressed()[0]:#
        mx, my = pygame.mouse.get_pos()

        # is the button clicked?  (is the mouse within a box at pos with size when the click occurs?)
        if mx >= pos[0] and mx <= pos[0] + size[0]:
            if my >= pos[1] and my <= pos[1] + size[1]:
                return True
            else:
                return False
        else:
            return False
class Errormessage():
    def __init__(self, message, duration, obj):
        self.message = message
        self.duration = duration
        self.font = obj.largeboldfont
        self.ticks = 0
    def update(self, obj):
        self.ticks += 1
        text = self.font.render(self.message,True, (180, 100, 20))
        pos = (obj.dimensions[0] / 2 - text.get_width() / 2, obj.dimensions[1] / 2)
        obj.screen.blit(text, pos)
        if self.ticks >= self.duration:
            obj.Errormessage = None
            del(self)
class Cursor():
    def __init__(self, obj):
        self.font = obj.largeboldfont
        self.animationticks = 0
        self.mode = "Default"
        self.CurrentAnimation = None
        self.color = (120,120,120)
        self.radius = 12
        self.thickness = 2
    def update(self, obj):
        print(self.CurrentAnimation,self.animationticks)
        self.position = pygame.mouse.get_pos()
        if self.CurrentAnimation == "Delete":
            if self.animationticks >= 11:
                self.animationticks = 0
                self.CurrentAnimation = None
            if self.animationticks <= 8:
                self.color = (120 + 8 * self.animationticks,120 + 8 * self.animationticks,120 + 8 * self.animationticks)
                self.radius = 16
                self.thickness = int(3+self.animationticks/2)
                pygame.draw.circle(obj.screen, self.color, self.position,self.radius, self.thickness)
                startpos = self.position
                pygame.draw.line(obj.screen, (180, 140, 0), (startpos[0] - self.animationticks * 2, startpos[1] - self.animationticks * 2), (startpos[0] + self.animationticks * 2, startpos[1] + self.animationticks * 2), 11)
                pygame.draw.line(obj.screen, (180, 140, 0), (startpos[0] + self.animationticks * 2, startpos[1] - self.animationticks * 2), (startpos[0] - self.animationticks * 2, startpos[1] + self.animationticks * 2), 11)
                print("fgf",self.CurrentAnimation,self.animationticks)
        if self.CurrentAnimation == None:
            
            self.animationticks = 0
            #cursor animations
            self.mode = "Default"
            self.color = (120,120,120)
            self.radius = 16
            self.thickness = 2
            pygame.draw.circle(obj.screen, self.color, self.position,self.radius, self.thickness)
        if self.CurrentAnimation == "ArrowsOut":
            if self.animationticks >= 10:
                self.animationticks = 10
            if self.animationticks <= 10:
                self.color = (120 + 5 * self.animationticks,120 + 5 * self.animationticks,120 + 5 * self.animationticks)
                self.radius = int(16-self.animationticks/3)
                self.thickness = int(3+self.animationticks/3)
                pygame.draw.circle(obj.screen, self.color, self.position,self.radius, self.thickness)
            
        if self.CurrentAnimation == "Click":
            if self.animationticks >= 10:
                self.animationticks = 0
                self.CurrentAnimation = None
            if self.animationticks <= 8:
                self.color = (120 + 8 * self.animationticks,120 + 8 * self.animationticks,120 + 8 * self.animationticks)
                self.radius = 16
                self.thickness = int(3+self.animationticks/2)
                pygame.draw.circle(obj.screen, self.color, self.position,self.radius, self.thickness)
        
        if self.CurrentAnimation == "Buy":
            if self.animationticks >= 10:
                self.animationticks = 0
                self.CurrentAnimation = None
            if self.animationticks <= 10:
                self.color = (100 - 3 * self.animationticks,120 + 6 * self.animationticks,100 - 3 * self.animationticks)
                self.radius = 16 + self.animationticks / 2 + (20 - self.animationticks) / 3
                self.thickness = int(3+self.animationticks / 1.5)
                pygame.draw.circle(obj.screen, self.color, self.position,self.radius, self.thickness)
        self.animationticks += 1

    def SetArrows(self):
        self.CurrentAnimation = "ArrowsOut"
    def SetDefault(self):
        self.CurrentAnimation = None
    def SetDelete(self):
        self.CurrentAnimation = "Delete"
    def Click(self):
        if self.CurrentAnimation == None:
            self.CurrentAnimation = "Click"
    def SetBuy(self):
        self.CurrentAnimation = "Buy"


class TextAnimation():
    def __init__(self, message, duration, obj):
        self.message = message
        self.duration = duration
        self.font = obj.largeboldfont
        self.ticks = 0
        obj.TextAnimations.append(self)
        xr = random.randint(round(obj.dimensions[0] * 0.4), round(obj.dimensions[0] * 0.6))
        yr = random.randint(round(obj.dimensions[1] * 0.4), round(obj.dimensions[1] * 0.6))
        self.pos = (xr, yr)
    def update(self, obj):

        text = self.font.render(self.message,True, (180, 100, 20))
        if self.ticks < 10:
            text = pygame.transform.scale(text, (text.get_width() * (1 + self.ticks / 30), text.get_height() * (1 + self.ticks / 30)))
        if self.ticks > self.duration - 25:
            #set alpha, creating a fade out effect
            alpha = (self.duration - self.ticks) * 10
            text.set_alpha(alpha)
        obj.screen.blit(text, self.pos)
        self.ticks += 1
        if self.ticks == self.duration:
            del(self)

class PartUI():
    def __init__(self, obj, part):
        self.boldfont = obj.boldfont
        self.font = obj.font
        self.image = obj.textures["UI_tile_loweralpha.png"]
        self.size = (800, 600)
        self.part = None
        if part != None:
            self.part = part
            self.part = part
            self.PartName = part["name"]
            self.ShowProperties = part["ShowProperties"]
            self.PartType = part["Type"]
        self.image = pygame.transform.scale(self.image, self.size)
    def setPart(self, part):
        self.part = part
        self.part = part
        self.PartName = part["name"]
        self.ShowProperties = part["ShowProperties"]
        self.PartType = part["Type"]

    def update(self, obj):

        NameText = self.boldfont.render(self.PartName, True, (20,20,20))
        Image = self.part["Textures"][0]["Image"]
        Image = obj.textures[Image]
        Image = pygame.transform.scale(Image,(self.part["Textures"][0]["Size"][0] * 2,self.part["Textures"][0]["Size"][1] * 2 ))
        self.pos = obj.dimensions[0] / 2 - self.size[0] / 2,obj.dimensions[1] / 2 - self.size[1] / 2
        obj.screen.blit(self.image, self.pos )
        obj.screen.blit(NameText, (self.pos[0] + 30, self.pos[1] + 30))
        obj.screen.blit(Image, (obj.dimensions[0] / 2 - Image.get_width() / 2, self.pos[1] + 90))
        ImageHeight = Image.get_height()
        c = 0
        while c < len(self.part["Description"]):
            text = self.font.render(self.part["Description"][c].strip("\n"), True, (20,20,20))
            obj.screen.blit(text, (self.pos[0] + 50 ,self.pos[1]+ ImageHeight + 100))
            ImageHeight += text.get_height() + 20
            c += 1
        text = "Type: "+ self.part["Type"]
        Text = self.boldfont.render(text, True, (20,20,20))
        obj.screen.blit(Text, (self.pos[0] + 50 ,self.pos[1]+ ImageHeight + 140))
        c = 0
        while c < len(self.part["ShowProperties"]):
            text = self.part["ShowProperties"][c] + ": "+ str(self.part["Properties"][self.part["ShowProperties"][c]])
            text = self.boldfont.render(text, True, (20,20,20))
            obj.screen.blit(text, (self.pos[0] + 50 ,self.pos[1]+ ImageHeight + 180 + c * 40))
            c += 1


    



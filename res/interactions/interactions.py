import pygame,os

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



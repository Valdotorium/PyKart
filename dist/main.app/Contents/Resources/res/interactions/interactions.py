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
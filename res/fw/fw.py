import pygame
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
    obj.shopdict[part["Name"]] = {"type" : part["Type"], "cost":part["Cost"], "texture":part["Tex"]}
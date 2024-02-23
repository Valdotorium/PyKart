import pygame
#some small helpers to make code shorter and maybe more radable
def getScreenSize():
    try:
        return pygame.display.get_desktop_sizes()
    except:
        raise ValueError("ERRNO_01:Could not get screen size")

def displayText(obj, text):
    
    txt = obj.largefont.render(text, True, (20, 20, 20))
    obj.screen.fill((100,100,100))
    obj.screen.blit(txt, (0, 300))
    pygame.display.update()
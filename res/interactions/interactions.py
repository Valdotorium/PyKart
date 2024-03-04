import pygame

def ButtonArea(obj, image, pos, size):
    print("Creating a button at position " + str(pos) + " and size" + str(size))
    try:
        obj.screen.blit(image, pos)
    except:
        raise SyntaxError("ERRNO_04: could not find screen to blit on")
    if pygame.mouse.get_pressed()[0]:#
        print("Mouse pressed")
        mx, my = pygame.mouse.get_pos()

        # is the button clicked?  (is the mouse within a box at pos with size when the click occurs?)
        if mx >= pos[0] and mx <= pos[0] + size[0]:
            if my >= pos[1] and my <= pos[1] + size[1]:
                print("ive been clicked on!")
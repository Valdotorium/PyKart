import pygame

def GameControls(obj):
    if not obj.isWeb:
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            obj.Throttle += 2.4 / obj.fpsFactor
        if pygame.key.get_pressed()[pygame.K_b]:
            obj.Throttle -= 4.6 / obj.fpsFactor
    else:
        #if user clicks in the right half of the screen, accelerate, else, brake
        if pygame.mouse.get_pressed()[0]:
            if pygame.mouse.get_pos()[0] > obj.dimensions[0] / 2:
                obj.Throttle += 2.4 / obj.fpsFactor
            else:
                obj.Throttle -= 4.6 / obj.fpsFactor
    for event in pygame.event.get():
        if event.type == pygame.MOUSEWHEEL:
            print("Scroll")
            print(event.x, event.y)
            if event.y < 0:
                obj.GameZoom += 0.01
            elif event.y > 0:
                obj.GameZoom -= 0.01
    if not obj.isWeb:
        if obj.GameZoom < 0.7:
            obj.GameZoom = 0.7
        if obj.GameZoom > 1.15:
            obj.GameZoom = 1.15
    else:
        obj.GameZoom = 1
    

def BuildControls(obj):
    if obj.KeyCooldown <= 0:
        if pygame.key.get_pressed()[pygame.K_p]:
            #precision mode
            if pygame.key.get_pressed()[pygame.K_d]:
                obj.RotationOfSelectedPart -= 9
                obj.KeyCooldown = 12
            if pygame.key.get_pressed()[pygame.K_a]:
                obj.RotationOfSelectedPart += 9
                obj.KeyCooldown = 12
        else:
            if pygame.key.get_pressed()[pygame.K_d]:
                obj.RotationOfSelectedPart -= 45
                obj.KeyCooldown = 18
            if pygame.key.get_pressed()[pygame.K_a]:
                obj.RotationOfSelectedPart += 45
                obj.KeyCooldown = 18
    obj.KeyCooldown -= 1
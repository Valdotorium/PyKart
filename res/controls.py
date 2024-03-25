import pygame

def GameControls(obj):
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        obj.Throttle += 4
    if pygame.key.get_pressed()[pygame.K_b]:
        obj.Throttle -= 6
    for event in pygame.event.get():
        if event.type == pygame.MOUSEWHEEL:
            print("Scroll")
            print(event.x, event.y)
            if event.y < 0:
                obj.GameZoom += 0.01
            elif event.y > 0:
                obj.GameZoom -= 0.01
    if obj.GameZoom < 0.7:
        obj.GameZoom = 0.7
    if obj.GameZoom > 1.15:
        obj.GameZoom = 1.15
    

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
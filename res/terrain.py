#the planet terrain generator
import random
import pygame
from .fw import fw as utils
def terrain_quality_presets(obj):
    #values for the generator:
    #the stepness of the terrain
    obj.terrain_steepness = 2
    #scale factor of all generated values
    obj.terrain_scale = 1
    #how "random" the terrain will be generated, in percent
    obj.min_terrain_variation = 10
    obj.max_terrain_variation = 40
    #different layers in the noise. highly affect detail
    obj.terrain_overlays = 4
    #the higher, the more random and smooth the terrain
    obj.terrain_overlay_downscale = 2
    obj.terrain_step_length = 32
    #length of the map
    obj.terrain_length = 1024

    if obj.S_Terrain_Size == "small":
        obj.terrain_step_length = 16
        obj.terrain_length = 512
        obj.terrain_overlays = 6
    if obj.S_Terrain_Size == "medium":
        obj.terrain_step_length = 32
        obj.terrain_length = 1024
        obj.terrain_overlays = 7
    if obj.S_Terrain_Size == "default":
        obj.terrain_step_length = 64
        obj.terrain_length = 2048
        obj.terrain_overlays = 9
    if obj.S_Terrain_Size == "large":
        obj.terrain_step_length = 128
        obj.terrain_length = 4196
        obj.terrain_overlays = 10

    if obj.S_Terrain_Preset == "default":
        obj.terrain_overlay_downscale = 2
        obj.min_terrain_variation = 10
        obj.max_terrain_variation = 30
        obj.terrain_steepness = 1.5
    if obj.S_Terrain_Preset == "flat":
        obj.terrain_overlay_downscale = 1
        obj.min_terrain_variation = 0
        obj.max_terrain_variation = 0
        obj.terrain_steepness = 0
    if obj.S_Terrain_Preset == "smooth":
        obj.terrain_overlay_downscale = 1.2
        obj.min_terrain_variation = 5
        obj.max_terrain_variation = 15
        obj.terrain_steepness = 0.2
        obj.terrain_overlays *= 2
    if obj.S_Terrain_Preset == "chipped":
        obj.terrain_overlay_downscale = 4
        obj.min_terrain_variation = 10
        obj.max_terrain_variation = 40
        obj.terrain_steepness = 3
        obj.terrain_overlays -= 2
    if obj.S_Terrain_Preset == "mountainous":
        obj.terrain_overlay_downscale = 2
        obj.min_terrain_variation = 10
        obj.max_terrain_variation = 45
        obj.terrain_steepness = 2
    if obj.S_Terrain_Preset == "extreme":
        obj.terrain_overlay_downscale = 1.75
        obj.min_terrain_variation = 20
        obj.max_terrain_variation = 60
        obj.terrain_steepness = 3

    


def visualize_terrain_list(obj):
    maximum = max(obj.terrain)
    if maximum < 400:
        maximum = 400
    minimum = min(obj.terrain)
    minimum -= round(maximum/4)
    dimensions = pygame.display.get_window_size()
    print(f"dimensions: {dimensions}")
    screen_width = dimensions[0]
    screen_height = dimensions[1]
    number_in_pixels = screen_height / maximum
    item_in_pixels = screen_width / len(obj.terrain)
    i= 0
    obj.screen.fill((100,100,100))
    while i < len(obj.terrain):
        #draw a small white rectangle
        pygame.draw.rect(obj.screen, (255, 255, 255),[ round(i * item_in_pixels), screen_height-(round(obj.terrain[i] * number_in_pixels)), round(item_in_pixels) + 1, 4] )
        i += 1
        pygame.display.update()
        
def generate(obj):
    
    utils.displayText(obj, "Generating Terrain")
    terrain_variation_diff = obj.max_terrain_variation - obj.min_terrain_variation
    #start seed
    heightvalue = random.randint(4, 10)
    obj.terrain = []
    #how frequently the terrain value gets updated
    steplength = obj.terrain_step_length
    length = obj.terrain_length
    x = 0
    while x < length:
        obj.terrain.append(0)
        x += 1
    x = 0
    while x < obj.terrain_overlays:
        #if the first iteration is done, modify the existing list, and not restart the entire process

        y = 0
        #modifying the terrain values
        while y < obj.terrain_length:

            if x > 0:
                heightvalue = obj.terrain[y]
            r = random.randint(0, 100)
            if r < obj.min_terrain_variation:
                #generate a slope
                heightvalue += random.uniform(-1*obj.terrain_steepness, obj.terrain_steepness) * steplength
            else:
                pass
            z = 0
            while z < steplength and y < len(obj.terrain):
                #overwriting the values
                if x == 0:
                    obj.terrain[y] += heightvalue
                else:
                    obj.terrain[y] = heightvalue
                if obj.terrain[y] < 0:
                    obj.terrain[y] = 0
  
                y += 1
                z += 1
        print(f"generated heightmap in overlay {x} with variation {obj.min_terrain_variation} and stepsize {steplength} stepsize")
        x += 1
        #the more detail, the higer the randomness
        obj.min_terrain_variation += terrain_variation_diff / obj.terrain_overlays
        #the more overlays there are, the more detailed the terrain is
        steplength /= obj.terrain_overlay_downscale
        #beatiful visualization of the generator working
        visualize_terrain_list(obj)



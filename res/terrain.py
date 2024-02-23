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
    obj.terrain_overlay_downscale = 2
    obj.terrain_step_length = 32
    #length of the map
    obj.terrain_length = 1024

def visualize_terrain_list(obj):
    maximum = max(obj.terrain)
    minimum = min(obj.terrain)
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
        pygame.draw.rect(obj.screen, (255, 255, 255),[ round(i * item_in_pixels), round(obj.terrain[i] * number_in_pixels), 4, 4] )
        i += 1
        pygame.display.update()
        
def generate(obj):
    
    utils.displayText(obj, "Generating Terrain")
    terrain_variation_diff = obj.max_terrain_variation - obj.min_terrain_variation
    heightvalue = random.randint(4, 10)
    obj.terrain = []
    steplength = obj.terrain_step_length
    length = obj.terrain_length
    x = 0
    while x < length:
        obj.terrain.append(0)
        x += 1
    x = 0
    while x < obj.terrain_overlays:
        if x > 0:
            heightvalue = obj.terrain[z]
        y = 0
        while y < obj.terrain_length:
            r = random.randint(0, 100)
            if r < obj.min_terrain_variation:
                #generate a slope
                heightvalue += random.randint(-obj.terrain_steepness, obj.terrain_steepness) * steplength
            else:
                pass
            if heightvalue < 0:
                heightvalue = 0
            elif heightvalue > obj.terrain_length / 2:
                heightvalue = obj.terrain_length / 2
            z = 0
            while z < steplength:
                if y == len(obj.terrain):
                    exit
                obj.terrain[y] += heightvalue
                y += 1
                z += 1
        print(f"generated heightmap in overlay {x} with variation {obj.min_terrain_variation}, the data is {obj.terrain} with len {len(obj.terrain)}")
        x += 1
        #the more detail, the higer the randomness
        obj.min_terrain_variation += terrain_variation_diff / obj.terrain_overlays
        #the more overlays there are, the more detailed the terrain is
        steplength /= obj.terrain_overlay_downscale
        visualize_terrain_list(obj)



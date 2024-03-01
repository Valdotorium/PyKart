#the planet terrain generator
import random
import pygame
import time
import pymunk
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

    #the higher the value, the less noise will be applied to the original seed height of the terrain
    obj.terrain_lacunarity = 10

    if obj.S_Terrain_Size == "small":
        obj.terrain_step_length = 32
        obj.terrain_length = 512
        obj.terrain_overlays = 7
    if obj.S_Terrain_Size == "medium":
        obj.terrain_step_length = 32
        obj.terrain_length = 1024
        obj.terrain_overlays = 7
    if obj.S_Terrain_Size == "default":
        obj.terrain_step_length = 32
        obj.terrain_length = 2048
        obj.terrain_overlays = 7
    if obj.S_Terrain_Size == "large":
        obj.terrain_step_length = 32
        obj.terrain_length = 4196
        obj.terrain_overlays = 7

    obj.terrain_step_length *= obj.S_Terrain_Scale_Factor

    if obj.S_Terrain_Preset == "default":
        obj.terrain_overlay_downscale = 1.35
        obj.min_terrain_variation = 20
        obj.max_terrain_variation = 40
        obj.terrain_steepness = 0.6
    if obj.S_Terrain_Preset == "flat":
        obj.terrain_overlay_downscale = 1
        obj.min_terrain_variation = 0
        obj.max_terrain_variation = 0
        obj.terrain_steepness = 0
    if obj.S_Terrain_Preset == "smooth":
        obj.terrain_overlay_downscale = 1.25
        obj.min_terrain_variation = 10
        obj.max_terrain_variation = 40
        obj.terrain_steepness = 0.15
        obj.terrain_overlays *= 2
    if obj.S_Terrain_Preset == "simple":
        obj.terrain_overlay_downscale = 1.2
        obj.min_terrain_variation = 5
        obj.max_terrain_variation = 15
        obj.terrain_steepness = 0.3
        obj.terrain_overlays = round(obj.terrain_overlays / 2)
    if obj.S_Terrain_Preset == "chipped":
        obj.terrain_overlay_downscale = 6
        obj.min_terrain_variation = 20
        obj.max_terrain_variation = 60
        obj.terrain_steepness = 1.6
        obj.terrain_overlays -= 2
    if obj.S_Terrain_Preset == "mountainous":
        obj.terrain_overlay_downscale = 1.25
        obj.min_terrain_variation = 10
        obj.max_terrain_variation = 45
        obj.terrain_steepness = 1
        obj.terrain_overlays += 1
    if obj.S_Terrain_Preset == "extreme":
        obj.terrain_overlay_downscale = 1.5
        obj.min_terrain_variation = 20
        obj.max_terrain_variation = 60
        obj.terrain_steepness = 1.4

    


def visualize_terrain_list(obj, terrain):
    maximum = 100
    minimum = -100
    dimensions = pygame.display.get_window_size()
    print(f"dimensions: {dimensions}")
    screen_width = dimensions[0]
    screen_height = dimensions[1]
    number_in_pixels = screen_height / (maximum-minimum)
    item_in_pixels = screen_width / len(terrain)
    i= 0
    obj.screen.fill((100,100,100))
    while i < len(terrain):
        #draw a small white rectangle
        pygame.draw.rect(obj.screen, (255, 255, 255),[ round(i * item_in_pixels), screen_height/2-(round((terrain[i]-minimum) * number_in_pixels)/3), round(item_in_pixels) + 1, 4] )
        i += 1
    pygame.display.update()
    utils.displayTextAt(obj, f"max: {max(terrain)}",(100, 10))
    utils.displayTextAt(obj, f"min: {min(terrain)}",(450, 10))
    utils.displayTextAt(obj, f"span: {max(terrain)-min(terrain)}",(800, 10))

    time.sleep(1)
        
def generate(obj):
    if obj.S_Terrain_Generator == "spots":
        
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
    if obj.S_Terrain_Generator == "lines":
       
        utils.displayText(obj, "Generating Terrain")
        terrain_variation_diff = obj.max_terrain_variation - obj.min_terrain_variation
        #start seed
        terrain = []
        obj.noisecollector = []
        length = obj.terrain_length
        x = 0
        seed = random.randint(2,8)
        while x < length:
            terrain.append(seed)
            x += 1
        x = 0
        #x = iterations
        steplength = obj.terrain_step_length

        while x < obj.terrain_overlays:
            tempterrain=[]
            q = 0
            while q < length:
                tempterrain.append(0)
                q += 1
            #how frequently the terrain value gets updated
            add_noise = True
            lacunarity = random.randint(0,100)
            slopechance = obj.min_terrain_variation
            y = 0
            #total position
            while y < len(terrain):
                first_line_point = tempterrain[y]
                r = random.randint(0,100)
                if r < slopechance:
                    #generate a slope by changing the height of the ending point of the line
                    if x == 0 or steplength < 2.5:
                        last_line_point = first_line_point + random.uniform(-1*obj.terrain_steepness, obj.terrain_steepness)*steplength
                    else: 
                        last_line_point = first_line_point + random.uniform(-1*obj.terrain_steepness, obj.terrain_steepness)*(steplength/(x+1))

                else:
                    last_line_point = first_line_point
                line_point_diff = (last_line_point - first_line_point) / steplength
                print(f"generated a line between the heights {first_line_point} and {last_line_point} with an elevation of {line_point_diff / steplength} per unit")
                z = 0
                while z < steplength and y < len(tempterrain):
                    #only generate noise when lacunarity allows it 
                    if lacunarity < obj.terrain_lacunarity:
                        add_noise = False
                    else:
                        add_noise = True
                    #alter lacunarity value
                    lacunarity += random.randint(-1,1)
                    if lacunarity > 100:
                        lacunarity = 100
                    if lacunarity < 0:
                        lacunarity = 0

                    if add_noise:
                        #drawing the line one unit longer than needed
                        #overwriting the values
                        tempterrain[y] = first_line_point + line_point_diff * z
                        if y + 2 < len(tempterrain):
                            tempterrain[y + 1] = tempterrain[y]
                            tempterrain[y + 2] = tempterrain[y]
                        z += 1
                        y += 1
                    else:
                        #skip
                        z += 1
                        y += 1
            print(f"generated heightmap in overlay {x} with variation {obj.min_terrain_variation} and stepsize {steplength}")
            x += 1
            #the more detail, the higer the randomness
            obj.min_terrain_variation += terrain_variation_diff / obj.terrain_overlays
            #the more overlays there are, the more detailed the terrain is
            steplength /= obj.terrain_overlay_downscale
            #beatiful visualization of the generator working
            visualize_terrain_list(obj, tempterrain)
            if steplength < 1:
                steplength = 1
            steplength = round(steplength)
            obj.noisecollector.append(tempterrain)

        #putting the lists together
        x = 0
        while x < len(obj.noisecollector):
            list_to_add = obj.noisecollector[x]
            print(f"adding list {list_to_add} to {terrain}")
            y = 0
            while y < len(list_to_add):
                terrain[y] = terrain[y] + list_to_add[y]
                y += 1
            x += 1
            obj.terrain = terrain
            visualize_terrain_list(obj, obj.terrain)

def place(obj):
    #drawing the terrain as poly and only adding collision physics
    pass

            




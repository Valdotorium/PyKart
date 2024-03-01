import pygame
import random

def UI(obj):
    obj.screen.fill((100,100,100))
    dim = obj.dimensions
    griddim = obj.CFG_Build_Grid_Dimensions
    print("LOG:building UI with dimensions ", dim)

    #calculating the perfect size for each tile in building mode
    tiles = []
    x = 0
    #creating a matrix of tiles for storing them:
    while x < griddim[0]:
        y = 0
        ytiles = []
        while y < griddim[1]:
            ytiles.append(0)
            y += 1
        x += 1
        tiles.append(ytiles)
    smallest_side = min(dim)
    tile_size = (smallest_side - smallest_side / 3) / min(griddim) #assuming the grid is larger on x
    tile_gap = (tile_size / 6) / min(griddim)
    print("LOG:BuildUI tile size is ", tile_size, " tile gap is ", tile_gap)

    start_pos = (dim[0] / 2 - ((tile_size + tile_gap) * griddim[0] / 2), tile_gap)
    print("LOG:BuildUI starting position is ", start_pos)
    #draw the tile grid
    x = 0
    while x < griddim[0]:
        y = 0
        while y < griddim[1]:
            tilepos= (start_pos[0] + (tile_size + tile_gap) * x, start_pos[1] + (tile_size + tile_gap) * y)
            #draw the tile rect
            pygame.draw.rect(obj.screen, (255, 255, 255), (tilepos[0], tilepos[1], tile_size, tile_size))
        
            y += 1
        x += 1

def run(obj):
    UI(obj)

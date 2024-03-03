import pygame
import random
def setupGrid(obj):
    obj.screen.fill((100,100,100))
    dim = obj.dimensions
    griddim = obj.CFG_Build_Grid_Dimensions
    #print("LOG:building UI with dimensions ", dim)

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
    #print("LOG:BuildUI tile size is ", tile_size, " tile gap is ", tile_gap)

    start_pos = (dim[0] / 2 - ((tile_size + tile_gap) * griddim[0] / 2), tile_gap)
    #print("LOG:BuildUI starting position is ", start_pos)
    #draw the tile grid
    tile_img = obj.textures["UI_tile.png"]
    #set the image to the size of the tile grid
    tile_img = pygame.transform.scale(tile_img, (tile_size, tile_size))
    obj.Build_TileGap = tile_gap
    obj.Build_TileSize = tile_size
    obj.Build_TileImg = tile_img

    #position matrix
    x = 0
    obj.Build_TileGridPositions = []
    while x < griddim[0]:
        y = 0
        column = []
        while y < griddim[1]:
            tilepos= (start_pos[0] + (tile_size + tile_gap) * x, start_pos[1] + (tile_size + tile_gap) * y)
            #draw the tile img
            column.append(tilepos)
        
            y += 1
        obj.Build_TileGridPositions.append(column)
        x += 1
    #print(obj.Build_TileGridPositions)
def UI(obj):
    #drawing the tile grid
    tile_size = obj.Build_TileSize
    tile_gap = obj.Build_TileGap
    tile_img = obj.Build_TileImg
    x = 0
    while x < len(obj.Build_TileGridPositions):
        y = 0
        while y < len(obj.Build_TileGridPositions[0]):
            tilepos = obj.Build_TileGridPositions[x][y]
            obj.screen.blit(tile_img, tilepos)
            y += 1

        x += 1

     #THE ACTUAL UI
    obj.UI_TilebarPositions = []
    x = 0
    while x < len(obj.partdict):
        try:
            key = list(obj.partdict)[x]
            part_img = obj.partdict[key]["Tex"]
            part_img = obj.textures[part_img]
            #scale the image to tile size
            part_img = pygame.transform.scale(part_img, (tile_size, tile_size))

            #stores position of tiles in the building menu
            obj.UI_TilebarPositions.append((x * (tile_size + tile_gap) + obj.dimensions[0] / 8, obj.dimensions[1] - obj.dimensions[1] / 6))

            #draw the part img
            obj.screen.blit(part_img, (x * (tile_size + tile_gap)  + obj.dimensions[0] / 8, obj.dimensions[1] - obj.dimensions[1] / 6))
        except:
            raise FileNotFoundError(f"ERRNO_03: Could not find texture for part {obj.partdict[x]["Name"]}")
        x += 1
        
def run(obj):
    UI(obj)

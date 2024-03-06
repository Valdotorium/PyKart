import pygame
import random
from .interactions import interactions as interactions
def setupGrid(obj):
    """This script sets up the sizes of tiles in  the building mode, fit to most conventional screen sizes
    the positions of all the tiles in building mode get stored in a list and passed to UI(), to avoid all those
    calculations every single frame."""
    obj.screen.fill((100,100,100))
    dim = obj.dimensions #the window dimesions as (x, y) tuple
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
    obj.Vehicle = []
    while x < griddim[0]:
        y = 0
        column = []
        column2 = []
        while y < griddim[1]:
            tilepos= (start_pos[0] + (tile_size + tile_gap) * x, start_pos[1] + (tile_size + tile_gap) * y)
            #draw the tile img
            column.append(tilepos)
            column2.append("")
        
            y += 1
        obj.Build_TileGridPositions.append(column)
        obj.Vehicle.append(column2)
        x += 1
    #print(obj.Build_TileGridPositions)
def UI(obj):
    """This script creates the UI elements in building mode and implements their core functions (for example part placement)
    More on part placement: parts will be placed within the obj.Vehicle matrix at index[x][y]. obj.vehicle only stores properties
    important for building mode while in building mode, these will be translated into physics stuff afterwards."""
    #drawing the tile grid
    #obj.Vehicle stores the vehicle
    tile_size = obj.Build_TileSize
    tile_gap = obj.Build_TileGap
    tile_img = obj.Build_TileImg
    x = 0
    while x < len(obj.Build_TileGridPositions):
        y = 0
        while y < len(obj.Build_TileGridPositions[0]):
            tilepos = obj.Build_TileGridPositions[x][y]
            #obj.screen.blit(tile_img, tilepos)

            #placing parts
            IsClicked = interactions.ButtonArea(obj, tile_img,obj.Build_TileGridPositions[x][y], (tile_size, tile_size) )
            if IsClicked:
                #part will be placed
                obj.Vehicle[x][y] = obj.selected_part
            y += 1



        x += 1
    #drawing the Vehicle
    x = 0
    while x < len(obj.Vehicle):
        y = 0
        while y < len(obj.Vehicle[0]):
            if obj.Vehicle[x][y] != "":
                #drawing existing parts
                tilepos = obj.Build_TileGridPositions[x][y]
                
                tile_part_img = obj.textures[obj.partdict[obj.Vehicle[x][y]]["Tex"]]
                #print("drawing part with texture " + tile_part_img)

                IsClicked = interactions.ButtonArea(obj, tile_part_img,tilepos, (tile_size, tile_size))
                if IsClicked:
                    #part will be placed
                    obj.Vehicle[x][y] = obj.selected_part
            y += 1



        x += 1

     #THE ACTUAL UI
    obj.UI_TilebarPositions = []
    x = 0
    while x < len(obj.partdict):
        try:
            key = list(obj.partdict)[x]
            #image of selected part
            part_img = obj.partdict[key]["Tex"]
            part_img = obj.textures[part_img]
            #scale the image to tile size
            part_img = pygame.transform.scale(part_img, (tile_size, tile_size))

            #stores position of tiles in the building menu
            obj.UI_TilebarPositions.append((x * (tile_size + tile_gap) + obj.dimensions[0] / 8, obj.dimensions[1] - obj.dimensions[1] / 6))

            #create a button with the part img
            IsClicked = interactions.ButtonArea(obj, part_img,(x * (tile_size + tile_gap) + obj.dimensions[0] / 8, obj.dimensions[1] - obj.dimensions[1] / 6), (tile_size, tile_size) )
            #IsClicked is True once the button gets clicked
            if IsClicked:
                
                obj.selected_part = obj.partdict[key]["Name"] 
                print("Selected part: " + obj.selected_part)
                textur = obj.partdict[obj.selected_part]["Stex"]
                textur = obj.textures[textur]
            
        except:
            raise FileNotFoundError(f"ERRNO_03: Could not find texture for part {obj.partdict[x]["Name"]}")
        x += 1
    #the start button
    pos = (obj.dimensions[0] - obj.dimensions[0] / 20, obj.dimensions[1] / 20)
    size = (obj.Build_TileSize, obj.Build_TileSize)
    IsClicked = interactions.ButtonArea(obj, obj.textures["UI_StartButton.png"], pos, size)
    if IsClicked:
        obj.gm = "transfer"
        
def run(obj):
    UI(obj)

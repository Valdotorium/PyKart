import pygame
import random
from .interactions import interactions as interactions
def setup(obj):
    scaleX = obj.dimensions[0] / 1200
    scaleY = obj.dimensions[1] / 800
    obj.scalefactor = scaleX 
    #the calculations of the game are performed in a 1200x800 screen, which will later get rescaled onto the actual window size. everything dealing with positions and sizes needs to get multiplied by scaleX
    print(1200 * scaleX , 800 * scaleX)
    obj.selectedPart = ""
    obj.Vehicle = []

 
def run(obj):
    scaleX = obj.scalefactor
    mx, my = pygame.mouse.get_pos()
    UserHasSelectedPart = False

    #--------------------------Drawing the part inventory---------------------------------------------------
    inventoryTileImage = obj.textures["UI_tile.png"]
    obj.inventoryTile = pygame.transform.scale(inventoryTileImage, (int(64 * scaleX), int(64 * scaleX)))
    c = 0
    #background for inventory tiles
    TileBackgroundImg = obj.textures["UI_tile.png"]
    TileBackgroundImg = pygame.transform.scale(TileBackgroundImg, (int(64 * scaleX), int(64 * scaleX)))
    #background for the building area
    BuildBackgroundImg = pygame.transform.scale(TileBackgroundImg,( round(obj.dimensions[0] * 0.75), round(obj.dimensions[1] * 0.75)))
    obj.screen.blit(BuildBackgroundImg, (obj.dimensions[0] / 8, obj.dimensions[1] / 8))
    while c < len(obj.partdict):
        gap = 10 * scaleX
        #getting the name of the texture
        part_img = obj.partdict[list(obj.partdict)[c]]["Tex"]
        #geting the preloaded surface using the name as key
        part_img = obj.textures[part_img]
        obj.screen.blit(TileBackgroundImg, (c *(64 * scaleX) + c * gap,obj.dimensions[1] - 100))
        IsClicked = interactions.ButtonArea(obj, part_img, (c *(64 * scaleX) + c * gap,obj.dimensions[1] - 100), ((64 * scaleX), int(64 * scaleX)))
        c += 1
        
        if IsClicked:
            UserHasSelectedPart = True
            print(f"User just cligged on part {obj.partdict[list(obj.partdict)[c - 1]]["Name"]}")
            obj.selectedPart = obj.partdict[list(obj.partdict)[c - 1]]["Name"]
    #------------------------------The play button----------------------------------------------------------------
    PlayButtonImg = obj.textures["UI_StartButton.png"]
    PlayButtonImg = pygame.transform.scale(PlayButtonImg, (int(64 * scaleX), int(64 * scaleX)))
    PlayButton = interactions.ButtonArea(obj, PlayButtonImg, (obj.dimensions[0] - 128 * scaleX, 64 * scaleX), (int(64 * scaleX), int(64 * scaleX)))
    if PlayButton:
        print("User just cligged on the play button")
        obj.gm = "transfer"
    #------------------------------Drawing the Vehicle--------------------------------------------------------
        
    c = 0
    while c < len(obj.Vehicle):
        Texture = obj.textures[obj.Vehicle[c]["Tex"]] # Surface object of Tex of item c in obj.Vehicle
        Texture = pygame.transform.scale(Texture, (int(64 * scaleX), int(64 * scaleX)))
        obj.screen.blit(Texture, obj.Vehicle[c]["Pos"])
        c += 1
    #------------------------------Drawing the Joints-----------------------------------------------------------
    c = 0
    obj.JointPositions = []
    while c < len(obj.Vehicle):
        PartJoints = obj.Vehicle[c]["Joints"]
        PartPosition = obj.Vehicle[c]["Pos"]
        #draw every joint of the part
        cc = 0
        while cc < len(PartJoints):
            JointPosition = PartJoints[cc]["Pos"]
            FinalJointPosition=[0,0]
            FinalJointPosition[0] = PartPosition[0] + JointPosition[0]
            FinalJointPosition[1] = PartPosition[1] + JointPosition[1]
            obj.JointPositions.append(FinalJointPosition)
            #print(f"creating joint at pos {FinalJointPosition}")
            pygame.draw.circle(obj.screen, (200,0,0), FinalJointPosition, 5 * scaleX)
            cc += 1
        c += 1
    #----------------------------- Getting Temporary Joint Positions of the SelectedPart --------------------------------------------------------
    JointPositionsOfSelectedPart = []
    if obj.selectedPart != "":
        SelectedPartJoints = obj.partdict[obj.selectedPart]["Joints"]
        
        c = 0
        while c < len(SelectedPartJoints):
            JointPosition = SelectedPartJoints[c]["Pos"]
            FJointPosition = [0,0]
            FJointPosition[0] = JointPosition[0] + mx
            FJointPosition[1] = JointPosition[1] + my
            JointPositionsOfSelectedPart.append(FJointPosition)

            c += 1
        print(f"joint positions of currently selected part: {JointPositionsOfSelectedPart}")  
    #------------------------------Sanpping to joints when close to them-------------------------------------------------------------------------
    
    if obj.selectedPart != "":
        c = 0
        while c < len(obj.JointPositions):
            cc = 0
            while cc < len(JointPositionsOfSelectedPart):
                #check if a joint of the part curently selected is closer than 15 * scaleX pixels to a placed joint
                if obj.JointPositions[c][0] - 15 * scaleX < JointPositionsOfSelectedPart[cc][0] < obj.JointPositions[c][0] + 15 * scaleX:
                    if obj.JointPositions[c][1] - 15 * scaleX < JointPositionsOfSelectedPart[cc][1] < obj.JointPositions[c][1] + 15 * scaleX:
                        mx,my = (obj.JointPositions[c][0] - SelectedPartJoints[cc]["Pos"][0], obj.JointPositions[c][1] - SelectedPartJoints[cc]["Pos"][1])
                cc += 1
            c += 1
    #------------------------------Drawing the selected part at mouse pos-------------------------------------
    if obj.selectedPart != "":
        #jos code
        textur = obj.partdict[obj.selectedPart]["Stex"]
        textur = obj.textures[textur]
        textur = pygame.transform.scale(textur, (int(64 * scaleX), int(64 * scaleX)))
        obj.screen.blit(textur, (mx, my))
    #----------------------------- Getting Temporary Joint Positions of the SelectedPart (if it snapped, at a new position) --------------------------------------------------------
    JointPositionsOfSelectedPart = []
    if obj.selectedPart != "":
        SelectedPartJoints = obj.partdict[obj.selectedPart]["Joints"]
        
        c = 0
        while c < len(SelectedPartJoints):
            JointPosition = SelectedPartJoints[c]["Pos"]
            FJointPosition = [0,0]
            FJointPosition[0] = JointPosition[0] + mx
            FJointPosition[1] = JointPosition[1] + my
            JointPositionsOfSelectedPart.append(FJointPosition)

            c += 1
        print(f"joint positions of currently selected part: {JointPositionsOfSelectedPart}") 
    #------------------------------Upon placement, check if the position of the parts center is within a valid rectangle (BuildBackgroundImg)--------------------------------
    if obj.selectedPart != "" and pygame.mouse.get_pressed()[0] and not UserHasSelectedPart:
        #if the mouse is touching BuildBackgroundImg, the part gets placed
        if obj.dimensions[0] * 0.125 < mx < 0.875 * obj.dimensions[0] and obj.dimensions[1] * 0.125 < my < 0.875 * obj.dimensions[1]:
            #checking if the position of the part is otherwise invalid
            PartIsValid = True
            #is the part exactly placed on another part?
            c = 0
            while c < len(obj.Vehicle):
                if (mx,my) == obj.Vehicle[c]["Pos"]:
                    PartIsValid = False
                    print("part placement failed due to invalid positioning")
                c += 1
            #saving the part that has been placed and its data to obj.Vehicle
            if PartIsValid:
                PlacedPart = {
                    #ready to store as json
                    "name": obj.selectedPart,
                    "Index": len(obj.Vehicle),
                    "Tex": obj.partdict[obj.selectedPart]["Tex"],
                    "Pos": (mx,my),
                    "refundValue": obj.partdict[obj.selectedPart]["Cost"],
                    "CanStandAlone": True,
                    "Joints":obj.partdict[obj.selectedPart]["Joints"]
                }
                obj.Vehicle.append(PlacedPart)
                print(f"part {obj.selectedPart} placed at {(mx,my)}")
                #part gets unselected
                obj.selectedPart = ""
        else:
            #the part gets unselected
            obj.selectedPart = ""
    #------------------------------Drawing dots at the currently selected parts joints --------------------------------
    if obj.selectedPart != "":
        c = 0
        while c < len(JointPositionsOfSelectedPart):
            pygame.draw.circle(obj.screen, (200,0,0), JointPositionsOfSelectedPart[c], 5 * scaleX)
            c += 1
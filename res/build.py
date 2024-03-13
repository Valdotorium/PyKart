import pygame
import random
from .interactions import interactions as interactions
from .fw import fw as utils
"""WARNING: BARELY READABLE CODE
This program does not perform very complex operations, but reading it with all the dictionary indexing can be quite challenging
here are some examples:
obj.partdict[list(obj.partdict)[c]]["Textures"]

this searches for the key list(obj.partdict)[c], which is the c-th key of obj.partdict.
Then it searches for "Textures" within this key-value pair.

obj.Vehicle[obj.JointPositions[c][0]]["Joints"][cc]["Type"]

this searches for the key obj.JointPositions[c][0], which is the parent of the joint obj.JointPositions[c]. From this 
parent part, it searches the Type of the cc-th Joint.

IsClicked = interactions.ButtonArea(obj,obj.textures[TexturesOfPart[cc]["Image"]],PositionOfTexture, (TexturesOfPart[cc]["Size"][0] * scaleX, TexturesOfPart[cc]["Size"][1] * scaleX))

this creates a clickable area for the object obj, which has the image of the cc-th texture of the part. It is located at the position
PositionOfTexture, which is the top left corner of the texture. The size of the texture is (TexturesOfPart[cc]["Size"][0] * scaleX, TexturesOfPart[cc]["Size"][1] * scaleX), which is a tuple
containing the sizes of the cc-th texture of the part multiplied by the UI scaling factor scaleX.
I hope this helps. -Valdotorium-
"""
def setup(obj):
    scaleX = obj.dimensions[0] / 1200
    print(f"scale factor: {scaleX}")
    scaleY = obj.dimensions[1] / 800
    obj.scalefactor = scaleX 
    #the calculations of the game are performed in a 1200x800 screen, which will later get rescaled onto the actual window size. everything dealing with positions and sizes needs to get multiplied by scaleX
    print(1200 * scaleX , 800 * scaleX)
    obj.selectedPart = ""
    obj.Vehicle = []
    obj.VehicleJoints = []
    obj.VehicleHitboxes = []
    #if joints have snapped together, it stores their data
    obj.SnappedJointData = None
    obj.SelectedBuiltPart = None

 
def run(obj):
    PartIsValid = True
    scaleX = obj.scalefactor
    mx, my = pygame.mouse.get_pos()
    UserHasSelectedPart = False

    #--------------------------Drawing the part inventory---------------------------------------------------
    inventoryTileImage = obj.textures["UI_tile.png"]
    obj.inventoryTile = pygame.transform.scale(inventoryTileImage, utils.Scale(obj, (64,64)))
    c = 0
    #background for inventory tiles
    TileBackgroundImg = obj.textures["UI_tile.png"]
    TileBackgroundImg = pygame.transform.scale(TileBackgroundImg, utils.Scale(obj,(64,64)))
    #background for the building area
    BuildBackgroundImg = pygame.transform.scale(TileBackgroundImg,( round(obj.dimensions[0] * 0.75), round(obj.dimensions[1] * 0.75)))
    obj.screen.blit(BuildBackgroundImg, (obj.dimensions[0] / 8, obj.dimensions[1] / 8))
    while c < len(obj.partdict):
        gap = 10
        cc = 0
        TexturesOfPart = obj.partdict[list(obj.partdict)[c]]["Textures"]
        #THE "BASE" POSITION (like "Pos" of part in obj.vehicle)
        #data of the texture stored in "Textures" of each part, here retrieved from partdict
        PositionOfTexture_X = 64 * c + 64 + gap*c
        #1/10 screen y's from the bottom:
        PositionOfTexture_Y = obj.dimensions[1] - round(obj.dimensions[1] / 10)
        #the position of the top left corner of the part
        #BasePositionOfTexture = [PositionOfTexture_X, PositionOfTexture_Y]
        while cc < len(obj.partdict[list(obj.partdict)[c]]["Textures"]):
            #THE "BASE" POSITION (like "Pos" of part in obj.vehicle)
            #adding relative position of texture
            PositionOfTexture = [PositionOfTexture_X, PositionOfTexture_Y]
            #the position of the texture
            PositionOfTexture = utils.Scale(obj,utils.AddTuples(PositionOfTexture, TexturesOfPart[cc]["Pos"]))
            IsClicked = interactions.ButtonArea(obj,obj.textures[TexturesOfPart[cc]["Image"]],PositionOfTexture, (TexturesOfPart[cc]["Size"][0] * scaleX, TexturesOfPart[cc]["Size"][1] * scaleX))
            if IsClicked:
                obj.SelectedBuiltPart = None
                UserHasSelectedPart = True
                print(f"User just cligged on part {obj.partdict[list(obj.partdict)[c]]["Name"]}")
                obj.selectedPart = obj.partdict[list(obj.partdict)[c]]["Name"]
            cc += 1
        c += 1
        
    #------------------------------The play button----------------------------------------------------------------
    PlayButtonImg = obj.textures["UI_StartButton.png"]
    PlayButtonImg = pygame.transform.scale(PlayButtonImg, utils.Scale(obj,[64,64]))
    PlayButton = interactions.ButtonArea(obj, PlayButtonImg, utils.Scale(obj,[50,50]), utils.Scale(obj,[64,64]))
    if PlayButton:
        print("User just cligged on the play button")
        obj.gm = "transfer"
    #------------------------------Drawing the Vehicle--------------------------------------------------------
        
    c = 0
    while c < len(obj.Vehicle):
        if obj.Vehicle[c] != None:
            cc = 0
            TexturesOfPart = obj.Vehicle[c]["Textures"]
            while cc < len(obj.Vehicle[c]["Textures"]):
                #data of the texture stored in "Textures"
                PositionOfTexture = utils.AddTuples(obj.Vehicle[c]["Pos"],TexturesOfPart[cc]["Pos"])
                IsClicked = interactions.ButtonArea(obj,obj.textures[TexturesOfPart[cc]["Image"]],PositionOfTexture,  utils.MultiplyTuple(TexturesOfPart[cc]["Size"], scaleX))
                if IsClicked:
                    obj.SelectedBuiltPart = c
                    print("user just selected part ", c, " of Vehicle")
                    #draeing a rect at the position of the texture with the size of the texture
                    pygame.draw.rect(obj.screen, (50,50,50), (obj.Vehicle[c]["Pos"][0], obj.Vehicle[c]["Pos"][1],round(TexturesOfPart[cc]["Size"][0] * scaleX), round(TexturesOfPart[cc]["Size"][1] * scaleX)), 2,2)
                cc += 1
        c += 1
    #------------------------------Drawing the Joints-----------------------------------------------------------
    c = 0
    obj.JointPositions = []
    while c < len(obj.Vehicle):
        if obj.Vehicle[c] != None:
            PartJoints = obj.Vehicle[c]["Joints"]
            PartPosition = obj.Vehicle[c]["Pos"]
            #draw every joint of the part
            cc = 0
            while cc < len(PartJoints):
                JointPosition = PartJoints[cc]["Pos"]
                FinalJointPosition=utils.AddTuples(PartPosition,JointPosition)
                obj.JointPositions.append([c,FinalJointPosition]) #c is also the index of the joints parent part
                #print(f"creating joint at pos {FinalJointPosition} with parent {c}")
                pygame.draw.circle(obj.screen, (200,0,0), FinalJointPosition, 5 * scaleX)
                cc += 1
        c += 1
    
    #print("all joints:", obj.JointPositions)
    #----------------------------- Getting Temporary Joint Positions of the SelectedPart --------------------------------------------------------
    JointPositionsOfSelectedPart = []
    if obj.selectedPart != "":
        SelectedPartJoints = obj.partdict[obj.selectedPart]["Joints"]
        
        c = 0
        while c < len(SelectedPartJoints):
            JointPosition = SelectedPartJoints[c]["Pos"]
            FJointPosition = utils.AddTuples(JointPosition, (mx,my))
            JointPositionsOfSelectedPart.append(FJointPosition)

            c += 1
        #print(f"joint positions of currently selected part: {JointPositionsOfSelectedPart}")  
    #------------------------------Sanpping to joints when close to them-------------------------------------------------------------------------
    obj.SnappedJointData = None
    if obj.selectedPart != "":
        c = 0
        while c < len(obj.JointPositions):
            cc = 0
            if obj.JointPositions[c] != None:
                while cc < len(JointPositionsOfSelectedPart):
                    #check if a joint of the part curently selected is closer than 15 * scaleX pixels to a placed joint
                    if obj.JointPositions[c][1][0] - 15 * scaleX < JointPositionsOfSelectedPart[cc][0] < obj.JointPositions[c][1][0] + 15 * scaleX:
                        if obj.JointPositions[c][1][1] - 15 * scaleX < JointPositionsOfSelectedPart[cc][1] < obj.JointPositions[c][1][1] + 15 * scaleX:
                            mx,my = (obj.JointPositions[c][1][0] - SelectedPartJoints[cc]["Pos"][0], obj.JointPositions[c][1][1] - SelectedPartJoints[cc]["Pos"][1])
                            #check if pairing of joints is invalid (if both joints have type "Accept")
                            if cc < len(obj.Vehicle[obj.JointPositions[c][0]]["Joints"]) and cc < len(obj.partdict[obj.selectedPart]["Joints"]):
                                if obj.Vehicle[obj.JointPositions[c][0]]["Joints"][cc]["Type"] == "Accept" and obj.partdict[obj.selectedPart]["Joints"][cc]["Type"] == "Accept":
                                    PartIsValid = False
                                    print("joint pairing is invalid")
                                #if both involved joints are providers, the joint data of the child part will get applied
                                if obj.Vehicle[obj.JointPositions[c][0]]["Joints"][cc]["Type"] == "Provide" and obj.partdict[obj.selectedPart]["Joints"][cc]["Type"] == "Provide":
                                    obj.SnappedJointData= {"JoinedParts": [obj.JointPositions[c][0], len(obj.Vehicle)], "JointData":obj.partdict[obj.selectedPart]["JointData"] }
                                    #The Joints Data that will be saved to obj.VehicleJoints
                                #if the new part is a acceptor and its parent is a provider, the joint data of the child part will get applied
                                if obj.Vehicle[obj.JointPositions[c][0]]["Joints"][cc]["Type"] == "Provide" and obj.partdict[obj.selectedPart]["Joints"][cc]["Type"] == "Accept":
                                    obj.SnappedJointData= {"JoinedParts": [obj.JointPositions[c][0], len(obj.Vehicle)], "JointData":obj.partdict[obj.selectedPart]["JointData"] }
                                    #The Joints Data that will be saved to obj.VehicleJoints
                                #vice versa
                                if obj.Vehicle[obj.JointPositions[c][0]]["Joints"][cc]["Type"] == "Accept" and obj.partdict[obj.selectedPart]["Joints"][cc]["Type"] == "Provide":
                                    obj.SnappedJointData= {"JoinedParts": [obj.JointPositions[c][0], len(obj.Vehicle)], "JointData":obj.partdict[obj.selectedPart]["JointData"] }
                                    #The Joints Data that will be saved to obj.VehicleJoints
                    cc += 1
            c += 1
    #------------------------------Drawing the selected part at mouse pos-------------------------------------
    if obj.selectedPart != "":
        #jos code
        textur = obj.partdict[obj.selectedPart]["Stex"]
        textur = obj.textures[textur]
        textur = pygame.transform.scale(textur, utils.Scale(obj,[64,64]))
        obj.screen.blit(textur, (mx, my))
    #----------------------------- Getting Temporary Joint Positions of the SelectedPart (if it snapped, at a new position) --------------------------------------------------------
    JointPositionsOfSelectedPart = []
    if obj.selectedPart != "":
        SelectedPartJoints = obj.partdict[obj.selectedPart]["Joints"]
        
        c = 0
        while c < len(SelectedPartJoints):
            JointPosition = SelectedPartJoints[c]["Pos"]
            FJointPosition = utils.AddTuples(JointPosition, (mx,my))
            JointPositionsOfSelectedPart.append(FJointPosition)

            c += 1
        #print(f"joint positions of currently selected part: {JointPositionsOfSelectedPart}") 
    #------------------------------Upon placement, check if the position of the parts center is within a valid rectangle (BuildBackgroundImg)--------------------------------
    if obj.selectedPart != "" and pygame.mouse.get_pressed()[0] and not UserHasSelectedPart:
        #if the mouse is touching BuildBackgroundImg, the part gets placed
        if obj.dimensions[0] * 0.125 < mx < 0.875 * obj.dimensions[0] and obj.dimensions[1] * 0.125 < my < 0.875 * obj.dimensions[1]:
            #checking if the position of the part is otherwise invalid

            #is the part exactly placed on another part?
            c = 0
            while c < len(obj.Vehicle):
                if obj.Vehicle[c] != None:
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
                    "Textures": obj.partdict[obj.selectedPart]["Textures"],
                    "Pos": (mx,my),
                    "refundValue": obj.partdict[obj.selectedPart]["Cost"],
                    "CanStandAlone": True,
                    "Joints": obj.partdict[obj.selectedPart]["Joints"],
                    "Hitbox": obj.partdict[obj.selectedPart]["Hitbox"]
                }
                #if a joint need to be formed, its data will be created here
                if obj.SnappedJointData != None:
                    PlacedPart["JoinedWith"] = obj.SnappedJointData["JoinedParts"]
                    obj.VehicleJoints.append(obj.SnappedJointData)
                else:
                    PlacedPart["JoinedWith"] = []
                obj.Vehicle.append(PlacedPart)
                print(f"part {obj.selectedPart} placed at {(mx,my)}")
                #part gets unselected
                obj.SnappedJointData = None
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
    #------------------------------The Unselect Part Button-------------------------------------
    if obj.SelectedBuiltPart != None:
        UnselectButton = interactions.ButtonArea(obj, obj.textures["UnselectButton.png"], utils.Scale(obj,(250,50)), utils.Scale(obj,[64,64]))
        if UnselectButton:
            obj.SelectedBuiltPart = None
        #---------------------The Delete Part Button--------------------------------
        DeleteButton = interactions.ButtonArea(obj, obj.textures["DeleteButton.png"], utils.Scale(obj,(150,50)), utils.Scale(obj,[64,64]))
        if DeleteButton:
            #removed parts are still list items, but they will be ignored
            obj.Vehicle[obj.SelectedBuiltPart] = None
            print(f"part {obj.SelectedBuiltPart} deleted")
            #removing all joints that are ocnneced to the built part
            c = 0
            while c < len(obj.JointPositions):
                if obj.SelectedBuiltPart == obj.JointPositions[c][0]:
                    #removed joints are still list items, but they will be ignored 
                    obj.JointPositions[c] = None
                c += 1
            obj.SelectedBuiltPart = None

        
    #------------------------------Marking the selected part-------------------------------------
    if obj.SelectedBuiltPart != None:
        RectPos = obj.Vehicle[obj.SelectedBuiltPart]["Pos"]
        pygame.draw.rect(obj.screen, (50,50,50), (RectPos[0], RectPos[1],int(64 * scaleX), int(64 * scaleX) ), 2,2)

    #TODO #3: part removing here!
    #remove parts dependent from the one removed 

import pygame
import random,json,os
from .interactions import interactions as interactions
from .fw import fw as utils
import copy

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
    if not obj.CFG_Reload_Latest_Vehicle:
        obj.Vehicle = []
        obj.VehicleJoints = []
        obj.VehicleHitboxes = []
    #if joints have snapped together, it stores their data
    obj.SnappedJointData = None
    obj.SelectedBuiltPart = None
    obj.RotationOfSelectedPart = 0
    obj.Errormessage = None
    obj.BuildUI = utils.BuildUI(obj)

def run(obj):
    PartIsValid = True
    scaleX = obj.scalefactor
    mx, my = pygame.mouse.get_pos()
    obj.UserHasSelectedPart = False

    #--------------------------Drawing the part inventory---------------------------------------------------
    inventoryTileImage = obj.textures["UI_tile.png"]
    obj.inventoryTile = pygame.transform.scale(inventoryTileImage, utils.Scale(obj, (64,64)))
    c = 0
    #background for inventory tiles
    obj.BuildUI.run(obj)
        
    #------------------------------The play button----------------------------------------------------------------
    PlayButtonImg = obj.textures["PlayButton.png"]
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

                textur = TexturesOfPart[cc]["Image"]
                textur = obj.textures[textur]
                textur = pygame.transform.scale(textur, utils.Scale(obj,obj.Vehicle[c]["Textures"][0]["Size"]))
                #applying rotation 
                textur = pygame.transform.rotate(textur, obj.Vehicle[c]["Rotation"])
                #rectangle for part rotation cuz it works somehow
                texture_rect = textur.get_rect(center = PositionOfTexture)
                obj.screen.blit(textur, texture_rect)
                #centering the part at its center point
                PositionOfTexture = utils.SubstractTuples(PositionOfTexture,obj.Vehicle[c]["Center"])
                IsClicked = interactions.ClickArea(PositionOfTexture, utils.MultiplyTuple(TexturesOfPart[cc]["Size"], scaleX))
                if IsClicked:
                    obj.SelectedBuiltPart = c
                    print("user just selected part ", c, " of Vehicle")
                    #draeing a rect at the position of the texture with the size of the texture
                    pygame.draw.rect(obj.screen, (50,50,50), (PositionOfTexture[0], PositionOfTexture[1],round(TexturesOfPart[cc]["Size"][0] * scaleX), round(TexturesOfPart[cc]["Size"][1] * scaleX)), 2,2)
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
    #stores the joints positions relative to the center of the part
    RelativeJointPositionsOfSelectedPart = []
    if obj.selectedPart != "":
        #TODO #7, this can probably be done by: centering all blitted graphics around their center point instead of their top left corner
        #(utils function for that?)
        #they will then always be referenced by their center point (which could be the anchor of the part)
        SelectedPartJoints = copy.deepcopy(obj.partdict[obj.selectedPart])["Joints"]
        c = 0
        while c < len(SelectedPartJoints):
            JointPosition = SelectedPartJoints[c]["Pos"]
            #Centering the part
            JointPosition = utils.SubstractTuples(JointPosition,obj.partdict[obj.selectedPart]["Center"])
            #rotating the joints position
            JointPosition = utils.RotateVector(JointPosition, -obj.RotationOfSelectedPart)
            FJointPosition = utils.AddTuples(JointPosition, (mx,my))
            JointPositionsOfSelectedPart.append(FJointPosition)
            RelativeJointPositionsOfSelectedPart.append(JointPosition)

            c += 1 
    #------------------------------Sanpping to joints when close to them-------------------------------------------------------------------------
    obj.SnappedJointData = None
    obj.IndexOfSnappedJoint = None
    if obj.selectedPart != "":
        c = 0
        while c < len(obj.JointPositions):
            cc = 0
            if obj.JointPositions[c] != None:
                while cc < len(JointPositionsOfSelectedPart):
                    #check if a joint of the part curently selected is closer than 15 * scaleX pixels to a placed joint
                    if obj.JointPositions[c][1][0] - 15 * scaleX < JointPositionsOfSelectedPart[cc][0] < obj.JointPositions[c][1][0] + 15 * scaleX:
                        if obj.JointPositions[c][1][1] - 15 * scaleX < JointPositionsOfSelectedPart[cc][1] < obj.JointPositions[c][1][1] + 15 * scaleX:
                            mx,my = (obj.JointPositions[c][1][0] - RelativeJointPositionsOfSelectedPart[cc][0], obj.JointPositions[c][1][1] - RelativeJointPositionsOfSelectedPart[cc][1])
                            #check if pairing of joints is invalid (if both joints have type "Accept")
                            #TODO: only one joint can be created in snapping, fix later.
                            ccc = 0
                            while ccc < len(obj.Vehicle[obj.JointPositions[c][0]]["Joints"]) and cc < len(obj.partdict[obj.selectedPart]["Joints"]):
                                if obj.Vehicle[obj.JointPositions[c][0]]["Joints"][ccc]["Type"] == "Accept" and obj.partdict[obj.selectedPart]["Joints"][cc]["Type"] == "Accept":
                                    PartIsValid = False
                                    print("joint pairing is invalid")
                                #if both involved joints are providers, the joint data of the child part will get applied
                                if obj.Vehicle[obj.JointPositions[c][0]]["Joints"][ccc]["Type"] == "Provide" and obj.partdict[obj.selectedPart]["Joints"][cc]["Type"] == "Provide":
                                    obj.SnappedJointData= {"JoinedParts": [obj.JointPositions[c][0], len(obj.Vehicle)], "JointData":obj.partdict[obj.selectedPart]["JointData"],"PositionData": [obj.JointPositions[c][1],JointPositionsOfSelectedPart[cc]], "SoundData": obj.partdict[obj.selectedPart]["Sounds"]["Crash"]}
                                    obj.IndexOfSnappedJoint = cc
                                    #The Joints Data that will be saved to obj.VehicleJoints
                                #if the new part is a acceptor and its parent is a provider, the joint data of the child part will get applied
                                if obj.Vehicle[obj.JointPositions[c][0]]["Joints"][ccc]["Type"] == "Provide" and obj.partdict[obj.selectedPart]["Joints"][cc]["Type"] == "Accept":
                                    obj.SnappedJointData= {"JoinedParts": [obj.JointPositions[c][0], len(obj.Vehicle)], "JointData":obj.partdict[obj.selectedPart]["JointData"],"PositionData": [obj.JointPositions[c][1],JointPositionsOfSelectedPart[cc]], "SoundData": obj.partdict[obj.selectedPart]["Sounds"]["Crash"] }
                                    obj.IndexOfSnappedJoint = cc
                                    #The Joints Data that will be saved to obj.VehicleJoints, format {JoinedParts: [Int,Int], JointData:{},PositionData: [Vec2d,Vec2d]}
                                    #JoinedParts stores the indexes of the two parts in obj.Vehicle
                                    #JointData stores the joint data of the (in this case) child joint
                                    #PositionData stores the position of the joint in world coordinates and the position of the joint relative to the new part
                                    #obj.Jointpositions[c][1] is a tuple containing the world coordinates of the joint.
                                #vice versa
                                if obj.Vehicle[obj.JointPositions[c][0]]["Joints"][ccc]["Type"] == "Accept" and obj.partdict[obj.selectedPart]["Joints"][cc]["Type"] == "Provide":
                                    obj.SnappedJointData= {"JoinedParts": [obj.JointPositions[c][0], len(obj.Vehicle)], "JointData":obj.partdict[obj.selectedPart]["JointData"],"PositionData": [obj.JointPositions[c][1],JointPositionsOfSelectedPart[cc]], "SoundData": obj.partdict[obj.selectedPart]["Sounds"]["Crash"] }
                                    obj.IndexOfSnappedJoint = cc
                                    #The Joints Data that will be saved to obj.VehicleJoints
                                ccc += 1
                    cc += 1
            c += 1
    #------------------------------Drawing the selected part at mouse pos-------------------------------------
    if obj.selectedPart != "":
        #jos code
        textur = copy.deepcopy(obj.partdict[obj.selectedPart])["Stex"]
        textur = obj.textures[textur]
        textur = pygame.transform.scale(textur, utils.Scale(obj,obj.partdict[obj.selectedPart]["Textures"][0]["Size"]))
        #applying rotation 
        textur = pygame.transform.rotate(textur, obj.RotationOfSelectedPart)
        #rectangle for part rotation cuz it works somehow
        texture_rect = textur.get_rect(center = (mx,my))
        obj.screen.blit(textur, texture_rect)
    #----------------------------- Getting Temporary Joint Positions of the SelectedPart (if it snapped, at a new position) --------------------------------------------------------
    JointPositionsOfSelectedPart = []
    #stores the joints positions relative to the center of the part
    RelativeJointPositionsOfSelectedPart = []
    if obj.selectedPart != "":
        #TODO #7, this can probably be done by: centering all blitted graphics around their center point instead of their top left corner
        #(utils function for that?)
        #they will then always be referenced by their center point (which could be the anchor of the part)
        SelectedPartJoints = copy.deepcopy(obj.partdict[obj.selectedPart])["Joints"]
        c = 0
        while c < len(SelectedPartJoints):
            JointPosition = SelectedPartJoints[c]["Pos"]
            #Centering the part
            JointPosition = utils.SubstractTuples(JointPosition,obj.partdict[obj.selectedPart]["Center"])
            #rotating the joints position
            JointPosition = utils.RotateVector(JointPosition, -obj.RotationOfSelectedPart)
            FJointPosition = utils.AddTuples(JointPosition, (mx,my))
            JointPositionsOfSelectedPart.append(FJointPosition)
            RelativeJointPositionsOfSelectedPart.append(JointPosition)

            c += 1
        #print(f"joint positions of currently selected part: {JointPositionsOfSelectedPart}") 
    #------------------------------Upon placement, check if the position of the parts center is within a valid rectangle (BuildBackgroundImg)--------------------------------
    if obj.selectedPart != "" and pygame.mouse.get_pressed()[0] and not obj.UserHasSelectedPart and obj.CFG_Build_Enforce_Rules:
        #is the user trying to place an "unjoined" accepting joint?
        if  obj.dimensions[0] * 0.1 < mx < 0.9 * obj.dimensions[0] and obj.dimensions[1] * 0.12 < my < 0.725 * obj.dimensions[1]:
            #if the mouse is touching BuildBackgroundImg, the part gets placed
            if obj.SnappedJointData == None and obj.partdict[obj.selectedPart]["Properties"]["JoiningBehavior"] != "Accept" or obj.SnappedJointData != None:
                #checking if the position of the part is otherwise invalid

                #is the part exactly placed on another part?
                c = 0
                while c < len(obj.Vehicle):
                    if obj.Vehicle[c] != None:
                        #todo 7
                        if (mx,my) == obj.Vehicle[c]["Pos"]:
                            PartIsValid = False
                            obj.Errormessage = interactions.Errormessage("Part Placement Invalid", 100, obj)
                            print("part placement failed due to invalid positioning")
                    c += 1
                #saving the part that has been placed and its data to obj.Vehicle   

                #overwriting the joints prositions (for rotation) 
                Joints = copy.deepcopy(obj.partdict[obj.selectedPart])["Joints"]
                jc = 0
                while jc < len(Joints):
                    Joints[jc]["Pos"] = RelativeJointPositionsOfSelectedPart[jc]
                    jc += 1         
                if PartIsValid:
                    PlacedPart = {
                        #ready to store as json
                        "name": obj.selectedPart,
                        "Index": len(obj.Vehicle),
                        "Textures": obj.partdict[obj.selectedPart]["Textures"],
                        "Pos": (mx,my),
                        "Type": obj.partdict[obj.selectedPart]["Type"],
                        "Rotation": obj.RotationOfSelectedPart,
                        "Center": obj.partdict[obj.selectedPart]["Center"], 
                        "refundValue": obj.partdict[obj.selectedPart]["Cost"],
                        "CanStandAlone": True,
                        "Joints": Joints,
                        "Hitbox": obj.partdict[obj.selectedPart]["Hitbox"],
                        "Properties": obj.partdict[obj.selectedPart]["Properties"],
                        "CrashSounds": obj.partdict[obj.selectedPart]["Sounds"]["Crash"],
                        "IdleSounds": obj.partdict[obj.selectedPart]["Sounds"]["Idle"],
                        "ActiveSounds": obj.partdict[obj.selectedPart]["Sounds"]["Active"]
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
                    obj.RotationOfSelectedPart = 0
        elif not obj.dimensions[0] * 0.1 < mx < 0.9 * obj.dimensions[0] or not obj.dimensions[1] * 0.12 < my < 0.725 * obj.dimensions[1]:
            pass
        else:
            #the part gets unselected
            obj.selectedPart = ""
            obj.SnappedJointData = None
            obj.RotationOfSelectedPart = 0
            obj.Errormessage = interactions.Errormessage("Part Placement Invalid", 100, obj)
    #------------------------------Drawing dots at the currently selected parts joints --------------------------------
    if obj.selectedPart != "":
        c = 0
        while c < len(JointPositionsOfSelectedPart):
            pygame.draw.circle(obj.screen, (200,0,0), JointPositionsOfSelectedPart[c], 5 * scaleX)
            c += 1
    #------------------------------The Unselect Part Button-------------------------------------
    if obj.SelectedBuiltPart != None:
        UnselectButton = interactions.ButtonArea(obj, obj.textures["UnselectButton.png"], utils.Scale(obj,(350,50)), utils.Scale(obj,[64,64]))
        if UnselectButton:
            obj.SelectedBuiltPart = None
        #---------------------The Delete Part Button--------------------------------
        DeleteButton = interactions.ButtonArea(obj, obj.textures["DeleteButton.png"], utils.Scale(obj,(250,50)), utils.Scale(obj,[64,64]))
        if DeleteButton:
            #removed parts are still list items, but they will be ignored
            obj.Vehicle[obj.SelectedBuiltPart] = None
            print(f"part {obj.SelectedBuiltPart} deleted")
            #removing all joints that are connected to the built part
            c = 0
            while c < len(obj.VehicleJoints):
                if obj.VehicleJoints[c] != None:
                    if obj.SelectedBuiltPart == obj.VehicleJoints[c]["JoinedParts"][0] or obj.SelectedBuiltPart == obj.VehicleJoints[c]["JoinedParts"][1]:
                        #removed joints are still list items, but they will be ignored 
                        obj.VehicleJoints.pop(c)
                c += 1
            obj.SelectedBuiltPart = None
    #------------------------------Marking the selected part-------------------------------------
    if obj.SelectedBuiltPart != None:
        RectPos = utils.SubstractTuples(obj.Vehicle[obj.SelectedBuiltPart]["Pos"], obj.Vehicle[obj.SelectedBuiltPart]["Center"])
        pygame.draw.rect(obj.screen, (250,225,225), (RectPos[0], RectPos[1],obj.Vehicle[obj.SelectedBuiltPart]["Textures"][0]["Size"][0],obj.Vehicle[obj.SelectedBuiltPart]["Textures"][0]["Size"][1]), 2,2)
    #------------------------------The Reload Vehicle Button---------------------------------------
    CurrentPath = os.path.dirname(os.path.realpath(os.path.dirname(__file__)))
    ReloadButton = interactions.ButtonArea(obj, obj.textures["ReloadButton.png"], utils.Scale(obj,(150,50)), utils.Scale(obj,[64,64]))
    if ReloadButton:
        print("loading latest vehicle")
        try:
            VehicleFile = open(CurrentPath+"/assets/saves/latest_vehicle.json")
            obj.Vehicle = json.load(VehicleFile)
            print(f"loaded vehicle: ", obj.Vehicle)
            VehicleJointFile = open(CurrentPath+"/assets/saves/latest_vehicle_joints.json")
            obj.VehicleJoints = json.load(VehicleJointFile)
            print(f"loaded vehicle joints: ", obj.VehicleJoints)
            VehicleHitboxFile = open(CurrentPath+"/assets/saves/latest_vehicle_hitboxes.json")
            obj.VehicleHitboxes = json.load(VehicleHitboxFile)
            print(f"loaded vehicle hitboxes: ", obj.VehicleHitboxes)
            #that could be buggy
            #obj.gm = "transfer"
        except:
            raise ImportError("Vehicle File not found")

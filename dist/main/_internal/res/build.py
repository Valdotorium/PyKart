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
KEYBINDS IN BUILD MODE:
A,D rotate 
A/D + P precision rotate
M Move Part
X Delete Part
S Unslect Part
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
    obj.SnappedJointData = []
    obj.SelectedBuiltPart = None
    obj.UserHasSelectedPart = False
    obj.RotationOfSelectedPart = 0
    obj.Errormessage = None
    obj.CurrentPartUI = interactions.PartUI(obj, None)
    obj.BuildUI = utils.BuildUI(obj)
    obj.credits = utils.Credits(obj)
    print("loading latest vehicle")
    CurrentPath = os.path.dirname(os.path.realpath(os.path.dirname(__file__)))
    if not obj.CFG_New_Game:
        try:
            VehicleFile = open(CurrentPath+"/assets/saves/latest_vehicle.json")
            obj.Vehicle = json.load(VehicleFile)
            print(f"loaded vehicle: ", obj.Vehicle)
            VehicleJointFile = open(CurrentPath+"/assets/saves/latest_vehicle_joints.json")
            obj.VehicleJoints = json.load(VehicleJointFile)
            print(f"loaded vehicle joints: ", obj.VehicleJoints)
            VehicleHitboxFile = open(CurrentPath+"/assets/saves/latest_vehicle_hitboxes.json")
            #this file can be ignored!
            obj.VehicleHitboxes = json.load(VehicleHitboxFile)
            print(f"loaded vehicle hitboxes: ", obj.VehicleHitboxes)
            #that could be buggy
            #obj.gm = "transfer"
        except:
                raise ImportError("Vehicle File not found")

def run(obj):
    PartIsValid = True
    print(obj.RotationOfSelectedPart)
    scaleX = obj.scalefactor
    mx, my = pygame.mouse.get_pos()

    #--------------------------Drawing the part inventory---------------------------------------------------
    inventoryTileImage = obj.textures["UI_tile.png"]
    obj.inventoryTile = pygame.transform.scale(inventoryTileImage, utils.Scale(obj, (64,64)))
    c = 0
    #background for inventory tiles
    obj.BuildUI.run(obj)
        
    #------------------------------The play button----------------------------------------------------------------
    PlacedPartCount = 0
    while c < len(obj.Vehicle):
        if obj.Vehicle[c] != None:
            PlacedPartCount += 1
        c += 1
    if PlacedPartCount >= 5:
        #only vehicles with five or more parts are allowed
        PlayButtonImg = obj.textures["PlayButton.png"]
        PlayButtonImg = pygame.transform.scale(PlayButtonImg, utils.Scale(obj,[80,80]))
        PlayButton = interactions.ButtonArea(obj, PlayButtonImg, utils.Scale(obj,[50,30]), utils.Scale(obj,[80,80]))
        if PlayButton:
            SelectSound = obj.sounds["click.wav"]
            SelectSound.play()
            print("User just cligged on the play button")
            obj.gm = "biomeselection"
    else:
        PlayButtonImg = obj.textures["PlayButtonLocked.png"]
        PlayButtonImg = pygame.transform.scale(PlayButtonImg, utils.Scale(obj,[80,80]))
        interactions.ButtonArea(obj, PlayButtonImg, utils.Scale(obj,[50,30]), utils.Scale(obj,[80,80]))
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

                    print("user just selected part ", c, " of Vehicle")
                    if obj.SelectedBuiltPart != c:
                        SelectSound = obj.sounds["click.wav"]
                        SelectSound.play()
                    obj.SelectedBuiltPart = c
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
            HitboxPosition = obj.Vehicle[c]["Hitbox"]["Pos"]
            #draw every joint of the part
            cc = 0
            while cc < len(PartJoints):
                JointPosition = PartJoints[cc]["Pos"]
                if obj.Vehicle[c]["Hitbox"]["Type"] != "Circle":
                    FinalJointPosition=utils.AddTuples(PartPosition,HitboxPosition)            
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
        HitboxPosition = obj.partdict[obj.selectedPart]["Hitbox"]["Pos"]
        c = 0
        while c < len(SelectedPartJoints):
            JointPosition = SelectedPartJoints[c]["Pos"]
            #Centering the part
            JointPosition = utils.SubstractTuples(JointPosition,obj.partdict[obj.selectedPart]["Center"])
            if obj.partdict[obj.selectedPart]["Hitbox"]["Type"] != "Circle":
                JointPosition = utils.AddTuples(JointPosition,HitboxPosition)
            #rotating the joints position
            JointPosition = utils.RotateVector(JointPosition, -obj.RotationOfSelectedPart)
            FJointPosition = utils.AddTuples(JointPosition, (mx,my))
            JointPositionsOfSelectedPart.append(FJointPosition)
            RelativeJointPositionsOfSelectedPart.append(JointPosition)

            c += 1 
    #------------------------------Sanpping to joints when close to them-------------------------------------------------------------------------
    obj.SnappedJointData = []
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
                            print("Found joint at", cc)
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
                                    obj.SnappedJointData.append({"JoinedParts": [obj.JointPositions[c][0], len(obj.Vehicle)], "JointData":obj.partdict[obj.selectedPart]["JointData"],"PositionData": [obj.JointPositions[c][1],JointPositionsOfSelectedPart[cc]], "SoundData": obj.partdict[obj.selectedPart]["Sounds"]["Crash"]})
                                    #The Joints Data that will be saved to obj.VehicleJoints
                                #if the new part is a acceptor and its parent is a provider, the joint data of the child part will get applied
                                if obj.Vehicle[obj.JointPositions[c][0]]["Joints"][ccc]["Type"] == "Provide" and obj.partdict[obj.selectedPart]["Joints"][cc]["Type"] == "Accept":
                                    obj.SnappedJointData.append({"JoinedParts": [obj.JointPositions[c][0], len(obj.Vehicle)], "JointData":obj.partdict[obj.selectedPart]["JointData"],"PositionData": [obj.JointPositions[c][1],JointPositionsOfSelectedPart[cc]], "SoundData": obj.partdict[obj.selectedPart]["Sounds"]["Crash"] })
                                    #The Joints Data that will be saved to obj.VehicleJoints, format {JoinedParts: [Int,Int], JointData:{},PositionData: [Vec2d,Vec2d]}
                                    #JoinedParts stores the indexes of the two parts in obj.Vehicle
                                    #JointData stores the joint data of the (in this case) child joint
                                    #PositionData stores the position of the joint in world coordinates and the position of the joint relative to the new part
                                    #obj.Jointpositions[c][1] is a tuple containing the world coordinates of the joint.
                                #vice versa
                                if obj.Vehicle[obj.JointPositions[c][0]]["Joints"][ccc]["Type"] == "Accept" and obj.partdict[obj.selectedPart]["Joints"][cc]["Type"] == "Provide":
                                    obj.SnappedJointData.append({"JoinedParts": [obj.JointPositions[c][0], len(obj.Vehicle)], "JointData":obj.partdict[obj.selectedPart]["JointData"],"PositionData": [obj.JointPositions[c][1],JointPositionsOfSelectedPart[cc]], "SoundData": obj.partdict[obj.selectedPart]["Sounds"]["Crash"]})
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
        obj.Cursor.SetArrows()
    #----------------------------- Getting Temporary Joint Positions of the SelectedPart (if it snapped, at a new position) --------------------------------------------------------
    JointPositionsOfSelectedPart = []
    #stores the joints positions relative to the center of the part
    RelativeJointPositionsOfSelectedPart = []
    if obj.selectedPart != "":
        #TODO #7, this can probably be done by: centering all blitted graphics around their center point instead of their top left corner
        #(utils function for that?)
        #they will then always be referenced by their center point (which could be the anchor of the part)
        SelectedPartJoints = copy.deepcopy(obj.partdict[obj.selectedPart])["Joints"]
        HitboxPosition = obj.partdict[obj.selectedPart]["Hitbox"]["Pos"]
        c = 0
        while c < len(SelectedPartJoints):
            JointPosition = SelectedPartJoints[c]["Pos"]
            #Centering the part
            JointPosition = utils.SubstractTuples(JointPosition,obj.partdict[obj.selectedPart]["Center"])
            if obj.partdict[obj.selectedPart]["Hitbox"]["Type"] != "Circle":
                JointPosition = utils.AddTuples(JointPosition,HitboxPosition)
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
        if  obj.dimensions[0] * 0.1 < mx < 0.9 * obj.dimensions[0] and obj.dimensions[1] * 0.12 < my < 0.66 * obj.dimensions[1]:
            #if the mouse is touching BuildBackgroundImg, the part gets placed
            if obj.SnappedJointData == [] or obj.SnappedJointData != []:
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
                        "ActiveSounds": obj.partdict[obj.selectedPart]["Sounds"]["Active"],
                        "ConstraintSounds": obj.partdict[obj.selectedPart]["Sounds"]["Constraints"],
                        "JoinedWith": [],
                        "ShowProperties": obj.partdict[obj.selectedPart]["ShowProperties"],
                        "Description": obj.partdict[obj.selectedPart]["Description"],
                    }
                    obj.partdict[obj.selectedPart]["Count"] -= 1
                    #if a joint need to be formed, its data will be created here
                    if obj.SnappedJointData != []:
                        c = 0
                        while c < len(obj.SnappedJointData):
                            PlacedPart["JoinedWith"].append(obj.SnappedJointData[c]["JoinedParts"])
                            obj.VehicleJoints.append(obj.SnappedJointData[c])
                            c += 1

                    else:
                        PlacedPart["JoinedWith"] = []
                    obj.Vehicle.append(PlacedPart)
                    PlaceSound = obj.sounds["select.wav"]
                    PlaceSound.play()
                    print(f"part {obj.selectedPart} placed at {(mx,my)}")
                    #part gets unselected
                    obj.SnappedJointData = None
                    obj.selectedPart = ""
                    obj.RotationOfSelectedPart = 0
                    obj.Cursor.SetDefault()
                else:
                    #part placement invalid, unselect
                    AlertSound = obj.sounds["alert.wav"]
                    AlertSound.play()
                    obj.SnappedJointData = None
                    obj.selectedPart = ""
                    obj.RotationOfSelectedPart = 0
                    obj.Cursor.SetDefault()
        elif not obj.dimensions[0] * 0.1 < mx < 0.9 * obj.dimensions[0] or not obj.dimensions[1] * 0.12 < my < 0.725 * obj.dimensions[1]:
            #part placement invalid, unselect
            AlertSound = obj.sounds["alert.wav"]
            AlertSound.play()
            obj.SnappedJointData = None
            obj.selectedPart = ""
            obj.RotationOfSelectedPart = 0
            obj.Cursor.SetDefault()
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
    #dragging should now be possible
    if obj.UserHasSelectedPart:
        if not pygame.mouse.get_pressed()[0]:
            obj.UserHasSelectedPart = False
    if obj.SelectedBuiltPart != None:
        UnselectButton = interactions.ButtonArea(obj, obj.textures["UnselectButton.png"], utils.Scale(obj,(350,30)), utils.Scale(obj,[80,80]))
        if UnselectButton or pygame.key.get_pressed()[pygame.K_s]:
            obj.credits.visible = False
            obj.CurrentPartUI.part = None
            obj.SelectedBuiltPart = None
            SelectSound = obj.sounds["click.wav"]
            SelectSound.play()
        
        #---------------------The Delete Part Button--------------------------------
        DeleteButton = interactions.ButtonArea(obj, obj.textures["DeleteButton.png"], utils.Scale(obj,(250,30)), utils.Scale(obj,[80,80]))
        if DeleteButton or pygame.key.get_pressed()[pygame.K_x]:
            SelectSound = obj.sounds["tyre_2.wav"]
            SelectSound.play()
            obj.Cursor.SetDelete()
            obj.partdict[obj.Vehicle[obj.SelectedBuiltPart]["name"]]["Count"] += 1
            #removed parts are still list items, but they will be ignored
            obj.Vehicle[obj.SelectedBuiltPart] = None
            print(f"part {obj.SelectedBuiltPart} deleted")
            #removing all joints that are connected to the built part
            c = 0
            while c < len(obj.VehicleJoints):
                if obj.VehicleJoints[c] != None:
                    if obj.SelectedBuiltPart == obj.VehicleJoints[c]["JoinedParts"][0] or obj.SelectedBuiltPart == obj.VehicleJoints[c]["JoinedParts"][1]:
                        #removed joints are still list items, but they will be ignored -NOT ANYMORE
                        obj.VehicleJoints.pop(c)
                c += 1
            obj.SelectedBuiltPart = None
        
    #------------------------------The Move Part Button------------------------------------------
        MoveButton = interactions.ButtonArea(obj, obj.textures["MoveButton.png"], utils.Scale(obj,(450,30)), utils.Scale(obj,[80,80]))
        if MoveButton or pygame.key.get_pressed()[pygame.K_m]:
            SelectSound = obj.sounds["click.wav"]
            SelectSound.play()
            obj.partdict[obj.Vehicle[obj.SelectedBuiltPart]["name"]]["Count"] += 1
            #esentially deleting the part
            SelectedPart = obj.SelectedBuiltPart
            obj.selectedPart = obj.Vehicle[SelectedPart]["name"]
            #storing the position of the part that is going to be deleted
            PartPosition = obj.Vehicle[SelectedPart]["Pos"]
            PartPosition =utils.AddTuples(PartPosition, obj.Vehicle[SelectedPart]["Center"])
            #removed parts are still list items, but they will be ignored
            obj.Vehicle[obj.SelectedBuiltPart] = None
            print(f"part {obj.SelectedBuiltPart} deleted")
            #removing all joints that are connected to the built part
            c = 0
            while c < len(obj.VehicleJoints):
                if obj.VehicleJoints[c] != None:
                    if obj.SelectedBuiltPart == obj.VehicleJoints[c]["JoinedParts"][0] or obj.SelectedBuiltPart == obj.VehicleJoints[c]["JoinedParts"][1]:
                        #removed joints are still list items, but they will be ignored -NOT ANYMORE
                        obj.VehicleJoints.pop(c)
                c += 1
            obj.SelectedBuiltPart = None
            obj.UserHasSelectedPart = True
            #setting mouse pos to pos of selected part
            pygame.mouse.set_pos(PartPosition)
            mx, my = pygame.mouse.get_pos()
            obj.Cursor.SetArrows()
    #------------------------------Marking the selected part-------------------------------------
    if obj.SelectedBuiltPart != None:
        RectPos = utils.SubstractTuples(obj.Vehicle[obj.SelectedBuiltPart]["Pos"], obj.Vehicle[obj.SelectedBuiltPart]["Center"])
        RectPos = utils.AddTuples(RectPos, obj.Vehicle[obj.SelectedBuiltPart]["Textures"][0]["Pos"])
        pygame.draw.rect(obj.screen, (250,225,225), (RectPos[0], RectPos[1],obj.Vehicle[obj.SelectedBuiltPart]["Textures"][0]["Size"][0],obj.Vehicle[obj.SelectedBuiltPart]["Textures"][0]["Size"][1]), 2,2)
    #------------------------------The Reload Vehicle Button---------------------------------------
    CurrentPath = os.path.dirname(os.path.realpath(os.path.dirname(__file__)))
    ReloadButton = interactions.ButtonArea(obj, obj.textures["ReloadButton.png"], utils.Scale(obj,(150,30)), utils.Scale(obj,[80,80]))
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
    
    #------------------------------The Part Info Button---------------------------------------
    PartInfoButton = interactions.ButtonArea(obj, obj.textures["infoButton.png"], utils.Scale(obj,(550,30)), utils.Scale(obj,[80,80]))
    if PartInfoButton or pygame.key.get_pressed()[pygame.K_i]:
        if obj.SelectedBuiltPart != None and obj.CurrentPartUI.part == None:
            SelectSound = obj.sounds["click.wav"]
            SelectSound.play()
            obj.CurrentPartUI.setPart(obj.Vehicle[obj.SelectedBuiltPart])
    if obj.CurrentPartUI.part != None and obj.SelectedBuiltPart != None:
        obj.CurrentPartUI.update(obj)
    #------------------------------The Credits Button---------------------------------------
    CreditButton = interactions.ButtonArea(obj, obj.textures["logo.png"], utils.Scale(obj,(obj.dimensions[0] - 100,30)), utils.Scale(obj,[80,80]))
    if CreditButton:
        obj.credits.visible = True
    #------------------------------The Tutorial Button---------------------------------------
    TutButton = interactions.ButtonArea(obj, obj.textures["tutorial.png"], utils.Scale(obj,(obj.dimensions[0] - 200,30)), utils.Scale(obj,[80,80]))
    if TutButton:
        obj.gm = "tutorial"


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

"""A class that defines the part inventory """
class PartInventory():
    def __init__(self, obj):
        self.categories = []
        self.parts = {}
        self.partdict = obj.partdict
        self.setup(obj)
        self.ScrollX = 0
        self.dimensions = obj.dimensions
        self.textures = obj.textures
        self.font = obj.font
        self.largefont = obj.largefont
        self.CurrentCategory = self.categories[0]
    def AddCategory(self, category):
        self.categories.append(category)
    def ClickArea(self,pos, size):
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()

            # is the button clicked?  (is the mouse within a box at pos with size when the click occurs?)
            if mx >= pos[0] and mx <= pos[0] + size[0]:
                if my >= pos[1] and my <= pos[1] + size[1]:
                    return True
                else:
                    return False
            else:
                return False
    def setup(self, obj):
        #finding out which categories exist
        for part in self.partdict.values():
            if part["Type"] not in self.categories:
                self.AddCategory(part["Type"])
        self.categories.sort()
        #finding out which parts exist
        self.parts = {}
        for category in self.categories:
            self.parts[category] = []
            for part in self.partdict.values():
                if part["Type"] == category:
                    self.parts[category].append(part["Name"])
        if obj.debug:
            print(self.categories, self.parts)
        self.ClickCooldown = 10
        self.ScrollXSpeed = 0
    def update(self, obj):

        SelectPartSound = obj.sounds["click.ogg"]
        BuySound = obj.sounds["buy.ogg"]
        AlertSound = obj.sounds["alert.ogg"]
        #Button for switching the category, displaying the name of the current category
        img = self.textures["UI_tile.png"]

        XOffset = 10
        for category in self.categories:
            c = self.categories.index(category)
            text = category
            pos = (XOffset, obj.dimensions[1] * 0.68)
            if category != self.CurrentCategory:
                text = self.largefont.render(text, True, (20,20,20))
            else:
                text = self.largefont.render(text, True, (140,35,25))
            img = pygame.transform.scale(img, (text.get_width() + 10, text.get_height() + 10))

            XOffset += text.get_width() + 15
            if category != self.CurrentCategory:
                IsClicked = self.ClickArea(pos, (text.get_width(), text.get_height()))
                obj.screen.blit(img, pos)
                obj.screen.blit(text, (pos[0] + 5, pos[1] + 5))
                if IsClicked and self.ClickCooldown < 0 and not obj.UserIsPlacingPart:
                    
                    SelectPartSound.play()
                    if obj.debug:
                        print("Clicked")
                    self.CurrentCategory = category
                    self.ScrollX = 0
                    self.setup(obj)
            else:
                obj.screen.blit(img, pos)
                obj.screen.blit(text, (pos[0] + 5, pos[1] + 5))
            self.ClickCooldown -= 1
        #tile image as background for the building ui, scaled to cover the bottom quarter of the screen
        Image = self.textures["UI_tile.png"]
        Image = pygame.transform.scale(Image, (obj.dimensions[0] * 2, obj.dimensions[1] * 0.25))
        obj.screen.blit(Image, (-200, obj.dimensions[1] * 0.75))
        
        #drawing the parts of the categories
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                if obj.debug:
                    print("Scroll")
                    print(event.x, event.y)
                if event.x < 0 or event.y < 0:
                    self.ScrollXSpeed = -10
                elif event.x > 0 or event.y > 0:
                    self.ScrollXSpeed = 10
        if -0.05 < self.ScrollXSpeed < 0.05 and self.ScrollXSpeed != 0:
            self.ScrollXSpeed = 0
        else:
            self.ScrollXSpeed *= 0.75
        self.ScrollX += self.ScrollXSpeed

        #drawing the parts of the current category, repositioned using scrollx
        X = round(obj.dimensions[0] / 20)
        gap = 15
        for part in self.parts[self.CurrentCategory]:
            if part in self.partdict:
                part = self.partdict[part]
                Image = self.textures[part["Textures"][0]["Image"]]
                Cost = part["Cost"]
                #draw low alpha version if part is not available
                #Image = pygame.transform.scale(Image, part["Textures"][0]["Size"])

                obj.screen.blit(Image, ( X + self.ScrollX, obj.dimensions[1] * 0.85))
                #making the part clickable
                IsClicked = self.ClickArea((X + self.ScrollX, obj.dimensions[1] * 0.85), part["Textures"][0]["Size"])
                X += part["Textures"][0]["Size"][0]  / 2 - 16
                #only select if part is available
                if IsClicked and self.ClickCooldown < 0 and obj.partdict[part["Name"]]["Count"] > 0: 
                    if obj.debug:
                        print("Clicked")
                    SelectPartSound.play()
                        
                    self.ClickCooldown = 20
                    obj.selectedPart = part["Name"]
                    obj.SelectedPart = True
                    obj.UserIsPlacingPart = True
                #buy part if money is enough
                elif IsClicked and self.ClickCooldown < 0 and obj.money >= Cost and not obj.UserIsPlacingPart:
                    if obj.debug:
                        print("Clicked")
                    self.ClickCooldown = 20
                    obj.money -= Cost
                    if obj.partdict[part["Name"]]["Count"] == 0:
                        obj.xp += round(Cost / 4) + 250
                    else:
                        obj.xp += round(Cost /6)
                    obj.partdict[part["Name"]]["Count"] += 1

                    player = BuySound.play()

                    obj.Cursor.SetBuy()

                elif IsClicked and self.ClickCooldown < 0 and obj.money < Cost:
                    player = AlertSound.play()

                    self.ClickCooldown = 14
                #display the cost above the image
                if part["Cost"] > obj.money:
                    textcolor = (130, 50, 20)
                else:
                    textcolor = (20, 20, 20)
                text = self.font.render(str(Cost), True, textcolor)
                pos = (X + self.ScrollX - text.get_width() / 2 + 30, obj.dimensions[1] * 0.8)
                obj.screen.blit(text, pos)

                CoinImage = obj.textures["coin.png"]
                CoinImage = pygame.transform.scale(CoinImage, (25,25))
                obj.screen.blit(CoinImage, (X + self.ScrollX - text.get_width() / 2, obj.dimensions[1] * 0.8))
                utils.DisplayMoney(obj)
                #display the available part count at the top right of the part img
                if part["Count"] == 0:
                    textcolor = (130, 50, 20)
                else:
                    textcolor = (20, 20, 20)
                text = self.font.render("x"+str(part["Count"]), True, textcolor)
                pos = (X + 10 + self.ScrollX, obj.dimensions[1] * 0.825)
                obj.screen.blit(text, pos)
                X += part["Textures"][0]["Size"][0]  / 2 + gap + 16


def discardPartPlacement(obj):
        if obj.UserHasRotatedPart:
            obj.UserHasRotatedPart = False
            pass
        else:
            obj.SnappedJointData = None
            obj.selectedPart = ""
            obj.RotationOfSelectedPart = 0
            obj.UserIsPlacingPart = False
            obj.Cursor.SetDelete()
        
def DeletePart(obj):
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

def setup(obj):

    scaleX = obj.dimensions[0] / 1200
    if obj.debug:
        print(f"scale factor: {scaleX}")
    scaleY = obj.dimensions[1] / 800
    obj.scalefactor = scaleX 
    #the calculations of the game are performed in a 1200x800 screen, which will later get rescaled onto the actual window size. everything dealing with positions and sizes needs to get multiplied by scaleX
    if obj.debug:
        print(1200 * scaleX , 800 * scaleX)
    obj.selectedPart = ""
    if not obj.CFG_Reload_Latest_Vehicle:
        obj.Vehicle = []
        obj.VehicleJoints = []
        obj.VehicleHitboxes = []
    #if joints have snapped together, it stores their data
    obj.SnappedJointData = []
    obj.SelectedBuiltPart = None
    obj.moveSelectedPart = False
    obj.SelectedPart = False
    obj.UserIsPlacingPart = False
    obj.RotationOfSelectedPart = 0
    obj.Errormessage = None
    obj.CurrentPartUI = interactions.PartUI(obj, None)
    obj.PartInventory = PartInventory(obj)
    obj.credits = utils.Credits(obj)
    if obj.debug:
        print("loading latest vehicle")
    CurrentPath = os.path.dirname(os.path.realpath(os.path.dirname(__file__)))
    if not obj.CFG_New_Game:
        try:
            VehicleFile = open(CurrentPath+"/assets/saves/latest_vehicle.json")
            obj.Vehicle = json.load(VehicleFile)
            if obj.debug:
                print(f"loaded vehicle: ", obj.Vehicle)
            VehicleJointFile = open(CurrentPath+"/assets/saves/latest_vehicle_joints.json")
            obj.VehicleJoints = json.load(VehicleJointFile)
            if obj.debug:
                print(f"loaded vehicle joints: ", obj.VehicleJoints)
            VehicleHitboxFile = open(CurrentPath+"/assets/saves/latest_vehicle_hitboxes.json")
            #this file can be ignored!
            obj.VehicleHitboxes = json.load(VehicleHitboxFile)
            if obj.debug:
                print(f"loaded vehicle hitboxes: ", obj.VehicleHitboxes)
            #that could be buggy
            #obj.gm = "transfer"
        except:
            raise ImportError("Vehicle File not found")

def run(obj):
    #-------------------------miscellaneous --------------------------------
    PartIsValid = True

    if obj.debug:
        print(obj.RotationOfSelectedPart)
    scaleX = obj.scalefactor
    mx, my = pygame.mouse.get_pos()
    MouseIsClicked = pygame.mouse.get_pressed()[0]

    #--------------------------Drawing the part inventory---------------------------------------------------
    inventoryTileImage = obj.textures["UI_tile.png"]
    obj.inventoryTile = pygame.transform.scale(inventoryTileImage, utils.Scale(obj, (64,64)))
    c = 0
    #background for inventory tiles
    obj.PartInventory.update(obj)

    #------------------------------Drawing the Vehicle--------------------------------------------------------
        
    c = 0
    while c < len(obj.Vehicle):
        if obj.Vehicle[c] != None:
            cc = 0
            TexturesOfPart = obj.Vehicle[c]["Textures"]
            while cc < len(obj.Vehicle[c]["Textures"]):
                TextureOffset = TexturesOfPart[cc]["Pos"]
                #rotate the texture offset
                TextureOffset = utils.RotateVector(TextureOffset, -obj.Vehicle[c]["Rotation"])
                #data of the texture stored in "Textures"
                PositionOfTexture = utils.AddTuples(obj.Vehicle[c]["Pos"],TextureOffset)

                textur = TexturesOfPart[cc]["Image"]
                textur = obj.textures[textur]
                textur = pygame.transform.scale(textur, utils.Scale(obj,obj.Vehicle[c]["Textures"][0]["Size"]))
                #applying rotation 
                textur = pygame.transform.rotate(textur, obj.Vehicle[c]["Rotation"])
                #rectangle for part rotation cuz it works somehow
                texture_rect = textur.get_rect(center = PositionOfTexture)
                obj.screen.blit(textur, texture_rect)
                
                cc += 1
        c += 1
    #------------------------------Drawing the Joints-----------------------------------------------------------
    c = 0
    obj.JointPositions = []
    while c < len(obj.Vehicle):
        if obj.Vehicle[c] != None and obj.selectedPart != "":
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
    RotatedRelativeJointPositionsOfSelectedPart = []
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
            RotatedRelativeJointPositionsOfSelectedPart.append(JointPosition)
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
                            
                            mx,my = (obj.JointPositions[c][1][0] - RelativeJointPositionsOfSelectedPart[cc][0], obj.JointPositions[c][1][1] - RelativeJointPositionsOfSelectedPart[cc][1])
                            obj.Cursor.SetSnap()
                            #check if pairing of joints is invalid (if both joints have type "Accept")
                            #TODO: only one joint can be created in snapping, fix later.
                            ccc = 0
                            while ccc < len(obj.Vehicle[obj.JointPositions[c][0]]["Joints"]) and cc < len(obj.partdict[obj.selectedPart]["Joints"]):
                                if obj.Vehicle[obj.JointPositions[c][0]]["Joints"][ccc]["Type"] == "Accept" and obj.partdict[obj.selectedPart]["Joints"][cc]["Type"] == "Accept":
                                    PartIsValid = False
                                    if obj.debug:
                                        print("joint pairing is invalid")
                                #if both involved joints are providers, the joint data of the child part will get applied
                                if obj.Vehicle[obj.JointPositions[c][0]]["Joints"][ccc]["Type"] == "Provide" and obj.partdict[obj.selectedPart]["Joints"][cc]["Type"] == "Provide":
                                    obj.SnappedJointData.append({"JoinedParts": [obj.JointPositions[c][0], len(obj.Vehicle)], "JointData":obj.partdict[obj.selectedPart]["JointData"],"PositionData": [obj.JointPositions[c][1],JointPositionsOfSelectedPart[cc],obj.partdict[obj.selectedPart]["Textures"][0]["Size"]], "SoundData": obj.partdict[obj.selectedPart]["Sounds"]["Crash"]})
                                    #The Joints Data that will be saved to obj.VehicleJoints
                                #if the new part is a acceptor and its parent is a provider, the joint data of the child part will get applied
                                if obj.Vehicle[obj.JointPositions[c][0]]["Joints"][ccc]["Type"] == "Provide" and obj.partdict[obj.selectedPart]["Joints"][cc]["Type"] == "Accept":
                                    obj.SnappedJointData.append({"JoinedParts": [obj.JointPositions[c][0], len(obj.Vehicle)], "JointData":obj.partdict[obj.selectedPart]["JointData"],"PositionData": [obj.JointPositions[c][1],JointPositionsOfSelectedPart[cc], obj.partdict[obj.selectedPart]["Textures"][0]["Size"]], "SoundData": obj.partdict[obj.selectedPart]["Sounds"]["Crash"] })
                                    #The Joints Data that will be saved to obj.VehicleJoints, format {JoinedParts: [Int,Int], JointData:{},PositionData: [Vec2d,Vec2d]}
                                    #JoinedParts stores the indexes of the two parts in obj.Vehicle
                                    #JointData stores the joint data of the (in this case) child joint
                                    #PositionData stores the position of the joint in world coordinates and the position of the joint relative to the new part
                                    #obj.Jointpositions[c][1] is a tuple containing the world coordinates of the joint.
                                    #the relative position of the joint relative to the center of the part is stored at index 2
                                    #and the dimensions of the part is stored at index 3.
                                    #based on these values, the position of the jointpivot joints can be calculated (for example)
                                #vice versa
                                if obj.Vehicle[obj.JointPositions[c][0]]["Joints"][ccc]["Type"] == "Accept" and obj.partdict[obj.selectedPart]["Joints"][cc]["Type"] == "Provide":
                                    obj.SnappedJointData.append({"JoinedParts": [obj.JointPositions[c][0], len(obj.Vehicle)], "JointData":obj.partdict[obj.selectedPart]["JointData"],"PositionData": [obj.JointPositions[c][1],JointPositionsOfSelectedPart[cc], obj.partdict[obj.selectedPart]["Textures"][0]["Size"]], "SoundData": obj.partdict[obj.selectedPart]["Sounds"]["Crash"]})
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
        TextureOffset =obj.partdict[obj.selectedPart]["Textures"][0]["Pos"]
        #rotate the texture offset
        TextureOffset = utils.RotateVector(TextureOffset, -obj.RotationOfSelectedPart)
        texture_rect = textur.get_rect(center = utils.AddTuples((mx,my), TextureOffset))
        obj.screen.blit(textur, texture_rect)
        if obj.Cursor.CurrentAnimation != "Snap":
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

    if obj.UserHasRotatedPart:
        obj.SelectedPart = True
    #------------------------------The Rotate Button---------------------------------------
    if obj.isWeb:
        RotButton = interactions.ButtonArea(obj, obj.textures["RotateButton.png"], utils.Scale(obj,(obj.dimensions[0] - 580,30)), utils.Scale(obj,[60,60]))
        if not RotButton:
            obj.UserHasRotatedPart = False
        if RotButton and not obj.UserHasRotatedPart:
            obj.RotationOfSelectedPart += 45
            obj.UserHasRotatedPart = True
    #------------------------------Upon placement, check if the position of the parts center is within a valid rectangle (BuildBackgroundImg)--------------------------------
    if obj.selectedPart != "" and obj.CFG_Build_Enforce_Rules and not obj.UserHasRotatedPart and obj.UserIsPlacingPart and not MouseIsClicked:
        #is the user trying to place an "unjoined" accepting joint?
        if  obj.dimensions[0] * 0.05 < mx < 0.85 * obj.dimensions[0] and obj.dimensions[1] * 0.1 < my < 0.66 * obj.dimensions[1]:
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
                        "refundValue": round(obj.partdict[obj.selectedPart]["Cost"] * 0.75),
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

                    #reducing the count of the part in obj.partdict
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

                    PlaceSound = obj.sounds["select.ogg"]
                    PlaceSound.play()
                    print(f"part {obj.selectedPart} placed at {(mx,my)}")
                    #part gets unselected
                    discardPartPlacement(obj)
                    obj.UserIsPlacingPart = False
                    obj.Cursor.SetPlace()
                else:
                    #part placement invalid, unselect
                    AlertSound = obj.sounds["alert.ogg"]
                    AlertSound.play()
                    discardPartPlacement(obj)
        elif not obj.dimensions[0] * 0.1 < mx < 0.9 * obj.dimensions[0] or not obj.dimensions[1] * 0.12 < my < 0.725 * obj.dimensions[1]:
            #part placement invalid, unselect
            AlertSound = obj.sounds["alert.ogg"]
            AlertSound.play()
            discardPartPlacement(obj)
        else:
            #the part gets unselected
            discardPartPlacement(obj)
            obj.Errormessage = interactions.Errormessage("Part Placement Invalid", 100, obj)
    #------------------------------Drawing dots at the currently selected parts joints --------------------------------
    if obj.selectedPart != "":
        c = 0
        while c < len(JointPositionsOfSelectedPart):
            pygame.draw.circle(obj.screen, (200,0,0), JointPositionsOfSelectedPart[c], 5 * scaleX)
            c += 1


            #------------------------------The Unselect Part Button-------------------------------------
    #dragging should now be possible
    if obj.SelectedPart:
        if not MouseIsClicked:
            obj.SelectedPart = False
    if obj.SelectedBuiltPart != None:
        #------------------------------Marking the selected part-------------------------------------
        if obj.SelectedBuiltPart != None:
            partSize = (obj.Vehicle[obj.SelectedBuiltPart]["Textures"][0]["Size"][0],obj.Vehicle[obj.SelectedBuiltPart]["Textures"][0]["Size"][1])
            RectPos = utils.SubstractTuples(obj.Vehicle[obj.SelectedBuiltPart]["Pos"], obj.Vehicle[obj.SelectedBuiltPart]["Center"])
            RectPos = utils.AddTuples(RectPos, utils.DivideTuple(obj.Vehicle[obj.SelectedBuiltPart]["Textures"][0]["Pos"], 1))
            rectSurf = pygame.Surface(partSize, pygame.SRCALPHA)
            pygame.draw.rect(rectSurf, (250,225,225), (0,0,partSize[0], partSize[1]), 2,2)
            utils.blitRotateCenter(obj.screen, rectSurf, RectPos, obj.Vehicle[obj.SelectedBuiltPart]["Rotation"])
            #checking if the selected part is being clicked for over 10 frames, if true, then move part
            if RectPos[0] < mx < RectPos[0] + partSize[0] and RectPos[1] < my < RectPos[1] + partSize[1] and obj.Cursor.clickedTicks >= 10:
                obj.moveSelectedPart = True
                obj.Cursor.SetArrows()
        PositionOfSelectedBuildPart = obj.Vehicle[obj.SelectedBuiltPart]["Pos"]
        pygame.draw.rect(obj.screen, (220,220,220), (PositionOfSelectedBuildPart[0] + 40, PositionOfSelectedBuildPart[1] - 100, 180, 360))
        pygame.draw.rect(obj.screen, (30,30,30), (PositionOfSelectedBuildPart[0] + 40, PositionOfSelectedBuildPart[1] - 100, 180, 360), 5)

        UnselectButton = interactions.ButtonArea(obj, obj.textures["_unselectButton.jpg"], utils.Scale(obj,[PositionOfSelectedBuildPart[0] + 200, PositionOfSelectedBuildPart[1] - 120]), utils.Scale(obj,[60,60]))
        if UnselectButton or pygame.key.get_pressed()[pygame.K_s]:
            if not obj.UserIsPlacingPart:
                obj.credits.visible = False
                obj.CurrentPartUI.part = None
                obj.SelectedBuiltPart = None
                SelectSound = obj.sounds["click.ogg"]
                SelectSound.play() 

        #checking if the user has closed the part UI
        if obj.CurrentPartUI.part != None:
            if obj.CurrentPartUI.CloseButton:
                obj.CurrentPartUI.part = None
        #---------------------The Delete Part Button--------------------------------
        DeleteButton = interactions.ButtonArea(obj, obj.textures["_deleteButton.jpg"], utils.Scale(obj, [PositionOfSelectedBuildPart[0] + 45, PositionOfSelectedBuildPart[1] - 80]), utils.Scale(obj,[170,78]))
        if DeleteButton or pygame.key.get_pressed()[pygame.K_x]:
            if not obj.UserIsPlacingPart and obj.SelectedBuiltPart != None:
                SelectSound = obj.sounds["tyre_2.ogg"]
                SelectSound.play()
                obj.Cursor.SetDelete()
                obj.partdict[obj.Vehicle[obj.SelectedBuiltPart]["name"]]["Count"] += 1
                #removed parts are still list items, but they will be ignored
                obj.Vehicle[obj.SelectedBuiltPart] = None
                DeletePart(obj)
        
    #------------------------------The Move Part Button------------------------------------------
        MoveButton = interactions.ButtonArea(obj, obj.textures["_moveButton.jpg"], utils.Scale(obj, [PositionOfSelectedBuildPart[0] + 45, PositionOfSelectedBuildPart[1]+ 160]), utils.Scale(obj,[170,78]))
        if MoveButton or pygame.key.get_pressed()[pygame.K_m] or obj.moveSelectedPart and not obj.UserIsPlacingPart:
            if not obj.UserIsPlacingPart:
                SelectSound = obj.sounds["click.ogg"]
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
                DeletePart(obj)
                obj.SelectedPart = True
                obj.UserIsPlacingPart = True
                #setting mouse pos to pos of selected part
                pygame.mouse.set_pos(PartPosition)
                mx, my = pygame.mouse.get_pos()
                obj.Cursor.SetArrows()
        obj.moveSelectedPart = False
    #---------------------The Sell Part Button--------------------------------
        SellButton = interactions.ButtonArea(obj, obj.textures["_sellButton.jpg"], utils.Scale(obj, [PositionOfSelectedBuildPart[0] + 45, PositionOfSelectedBuildPart[1] + 80]), utils.Scale(obj,[170,78]))
        if SellButton or pygame.key.get_pressed()[pygame.K_s]:
            if not obj.UserIsPlacingPart:
                SelectSound = obj.sounds["coinbag.ogg"]
                SelectSound.play()
                obj.Cursor.SetDelete()
                #returning 80% of the money to the user
                obj.money += obj.Vehicle[obj.SelectedBuiltPart]["refundValue"]
                #removed parts are still list items, but they will be ignored
                obj.Vehicle[obj.SelectedBuiltPart] = None
                obj.Cursor.SetSell()

                DeletePart(obj)
    #------------------------------The Part Info Button---------------------------------------
        PartInfoButton = interactions.ButtonArea(obj, obj.textures["_infoButton.jpg"], utils.Scale(obj, [PositionOfSelectedBuildPart[0] + 45, PositionOfSelectedBuildPart[1]]), utils.Scale(obj,[170,78]))
        if PartInfoButton or pygame.key.get_pressed()[pygame.K_i]:
            if obj.SelectedBuiltPart != None and obj.CurrentPartUI.part == None and not obj.UserIsPlacingPart:
                SelectSound = obj.sounds["click.ogg"]
                SelectSound.play()
                obj.CurrentPartUI.setPart(obj.Vehicle[obj.SelectedBuiltPart])
        if obj.CurrentPartUI.part != None and obj.SelectedBuiltPart != None:
            obj.CurrentPartUI.update(obj)
        
    #------------------------------The Reload Vehicle Button---------------------------------------
    if not obj.isWeb:
        ReloadButton = interactions.ButtonArea(obj, obj.textures["ReloadButton.png"], utils.Scale(obj,(140,30)), utils.Scale(obj,[60,60]))
        if ReloadButton and not obj.UserIsPlacingPart:
            utils.ReloadVehicle(obj)

        
    #------------------------------The Credits Button---------------------------------------
    CreditButton = interactions.ButtonArea(obj, obj.textures["_creditsButton.jpg"], utils.Scale(obj,(200,20)), utils.Scale(obj,[160,60]))
    if CreditButton and not obj.UserIsPlacingPart:
        obj.credits.visible = True
        obj.sounds["click.ogg"].play()
    #------------------------------The Tutorial Button---------------------------------------
    TutButton = interactions.ButtonArea(obj, obj.textures["_helpButton.jpg"], utils.Scale(obj,(380,20)), utils.Scale(obj,[160,60]))
    if TutButton  and not obj.UserIsPlacingPart:
        obj.gm = "tutorial"
        player = obj.sounds["click.ogg"].play()

    #------------------------------The play button----------------------------------------------------------------
    #count the items that are none in obj.vehicle
    c = 0
    PlacedPartCount = 0
    while c < len(obj.Vehicle):
        if obj.Vehicle[c] != None:
            PlacedPartCount += 1
        c += 1
    
    if 4 < PlacedPartCount:
        #only vehicles with five or more parts are allowed
        PlayButtonImg = obj.textures["_driveButton.jpg"]
        #PlayButtonImg = pygame.transform.scale(PlayButtonImg, utils.Scale(obj,[160,80]))
        PlayButton = interactions.ButtonArea(obj, PlayButtonImg, utils.Scale(obj,[20,20]), utils.Scale(obj,[160,60]))
        if PlayButton and not obj.UserIsPlacingPart:
            SelectSound = obj.sounds["click.ogg"]
            SelectSound.play()
            if obj.debug:
                print("User just cligged on the play button")
            obj.gm = "biomeselection"
    else:
        PlayButtonImg = obj.textures["_lockedDriveButton.jpg"]
        PlayButtonImg = pygame.transform.scale(PlayButtonImg, utils.Scale(obj,[160,80]))
        interactions.ButtonArea(obj, PlayButtonImg, utils.Scale(obj,[40,20]), utils.Scale(obj,[160,60]))

    #------------------------------checking if the user is selecting a built part--------------------------------
    c = 0
    while c < len(obj.Vehicle):
        if obj.Vehicle[c] != None:
            cc = 0
            TexturesOfPart = obj.Vehicle[c]["Textures"]
            while cc < len(obj.Vehicle[c]["Textures"]):
                TextureOffset = TexturesOfPart[cc]["Pos"]
                #rotate the texture offset
                TextureOffset = utils.RotateVector(TextureOffset, -obj.Vehicle[c]["Rotation"])
                #data of the texture stored in "Textures"
                PositionOfTexture = utils.AddTuples(obj.Vehicle[c]["Pos"],TextureOffset)
                #centering the part at its center point
                PositionOfTexture = utils.SubstractTuples(PositionOfTexture,obj.Vehicle[c]["Center"])
                IsClicked = interactions.ClickArea(PositionOfTexture, utils.MultiplyTuple(TexturesOfPart[cc]["Size"], scaleX))

                if IsClicked and obj.SelectedPart != None and not obj.moveSelectedPart and not obj.UserIsPlacingPart:
                    if obj.debug:
                        print("user just selected part ", c, " of Vehicle")
                    if obj.SelectedBuiltPart != c:
                        SelectSound = obj.sounds["click.ogg"]
                        SelectSound.play()
                    obj.SelectedBuiltPart = c
                cc += 1
        c += 1


import random
import pymunk

def Noise(obj, scale, variability):
        #main  terrain generator function
        print("----------------------------------------------------------------")
        x = 0
        #Height_Change = random.uniform(-obj.CFG_Terrain_Scale * scale, obj.CFG_Terrain_Scale * scale)
        Height_Change = 0
        Terrain_Direction = 0
        #should be renamed flatness, the higher, the flatter the terrain
        steepness = obj.CFG_Terrain_Flatness
        
        while x < len(obj.Terrain):
            r = random.uniform(0,100)
            if r < variability:
                Terrain_Direction += random.randint(-1,1)
            #keeping Terrain_Direction within valid area (-3 to 3)
            if Terrain_Direction > 3:
                Terrain_Direction = 3
            elif Terrain_Direction < -3:
                Terrain_Direction = -3
           
            if Terrain_Direction > 0:
                Height_Change += random.uniform(0, ((obj.CFG_Terrain_Scale * scale) / 50) * (Terrain_Direction / steepness))
            elif Terrain_Direction < 0:
                Height_Change += random.uniform(-((obj.CFG_Terrain_Scale * scale )/ 50) * (-Terrain_Direction / steepness), 0)
            Height_Change * scale

            obj.Terrain[x] += Height_Change
            obj.Terrain[x] = round(obj.Terrain[x])
            if obj.Terrain[x] < -50000:
                obj.Terrain[x] = -50000
                Height_Change = 0
                Terrain_Direction = 1
            if obj.Terrain[x] > 50000:
                obj.Terrain[x] = 50000
                Height_Change = 0
                Terrain_Direction = -1
            
            x += 1
            difficultyFactor = obj.CFG_Terrain_Difficulty_Increase
            difficultyFactor /= 10000
            steepness -= difficultyFactor + steepness * (difficultyFactor / 10)
            if steepness > 20:
                steepness = 20
            if steepness < 0.3:
                steepness = 0.3
            #1 screen = around 40 m
            if x == 4000:
               print("steepness at 280000px:",steepness)
            if x == 8000:
               print("steepness at 560000px:",steepness)
            if x == 12000:
               print("steepness at 740000px:",steepness)
        print("steepness at end:",steepness)
def setup(obj):
    obj.Terrain = []
    x = 0
    while x < 50000:
        obj.Terrain.append(650)
        x += 1

def generate_chunk(obj):
    Noise(obj, 24, 18)
    Noise(obj, 8, 30)
    Noise(obj, 4, 56)
    print("total terrain length:", len(obj.Terrain) * obj.CFG_Terrain_X_Scale)

    
def WritePolygonPositions(obj):
    
    #making tuples (x,y) out of the y positions of the future polygon vertices stored in obj.Terrain
    x = round((obj.X_Position + obj.CFG_Terrain_X_Scale * 8) /obj.CFG_Terrain_X_Scale)
    endx = round((obj.X_Position + obj.dimensions[0]*2.2)/ obj.CFG_Terrain_X_Scale)
    PolygonPoints = []
    obj.StaticPolygon = []
    #Edge point
    if x < 0: 
        x = 0
    if endx < 2:
        endx = 2
    
    while x < round(endx):
        Point = obj.Terrain[x]
        PolygonPoints.append(((x - 10) * round(obj.CFG_Terrain_X_Scale) - obj.X_Position, Point))
        obj.StaticPolygon.append(((x - 10) * round(obj.CFG_Terrain_X_Scale) , obj.Terrain[x]))
        x += 1
    #edge point
    obj.GroundRelief = PolygonPoints#provisorisch

    #print("THE GROUND POLYGON IS AT:", PolygonPoints)
    #print(f"drawing poly from terrain item {startx} to terrain item {x}")

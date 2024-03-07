import random

def Noise(obj, scale, variability):
        #main  terrain generator function
        print("----------------------------------------------------------------")
        x = 0
        Height_Change = random.uniform(-obj.CFG_Terrain_Scale * scale, obj.CFG_Terrain_Scale * scale)
        Terrain_Direction = "Up"

        while x < len(obj.Terrain):
            r = random.uniform(0,100)
            if r < variability:
                if Terrain_Direction == "Up":
                    Terrain_Direction = "Down"
                elif Terrain_Direction == "Down":
                    Terrain_Direction = "Up"
            if Terrain_Direction == "Up":
                Height_Change += random.uniform(0, (obj.CFG_Terrain_Scale * scale) / 50)
            elif Terrain_Direction == "Down":
                Height_Change += random.uniform(-(obj.CFG_Terrain_Scale * scale )/ 50, 0)
            Height_Change * scale
            obj.Terrain[x] += Height_Change
            obj.Terrain[x] = round(obj.Terrain[x])
            x += 1
def setup(obj):
    obj.Terrain = []
    x = 0
    while x < obj.CFG_Render_Distance * obj.CFG_Terrain_Detail:
        obj.Terrain.append(0)
        x += 1

def generate_chunk(obj):
    Noise(obj, 24, 8)
    Noise(obj, 6, 14)
    Noise(obj, 2, 26)

    print("generated terrain: " + str(obj.Terrain)) 
def WritePolygonPositions(obj):
    #making tuples (x,y) out of the y positions of the future polygon vertices stored in obj.Terrain
    obj.GroundPolygon = []
    x = 0
    PolygonPoints = []
    #Edge point
    PolygonPoints.append((0, 10000))
    while x < len(obj.Terrain):
        Point = obj.Terrain[x] + obj.Y_Position
        PolygonPoints.append((x * round(obj.dimensions[0] / obj.CFG_Terrain_X_Scale) - obj.X_Position, Point))
        x += 1
    #edge point
    PolygonPoints.append(((x - 1) * round(obj.dimensions[0] / obj.CFG_Terrain_X_Scale), 10000))
    obj.GroundPolygon = PolygonPoints
    #print("THE GROUND POLYGON IS AT:", PolygonPoints)

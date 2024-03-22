import random
import pymunk

def Noise(obj, scale, variability):
        #main  terrain generator function
        print("----------------------------------------------------------------")
        x = 0
        Height_Change = random.uniform(-obj.CFG_Terrain_Scale * scale, obj.CFG_Terrain_Scale * scale)
        Terrain_Direction = 0

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
                Height_Change += random.uniform(0, ((obj.CFG_Terrain_Scale * scale) / 50) * Terrain_Direction)
            elif Terrain_Direction < 0:
                Height_Change += random.uniform(-((obj.CFG_Terrain_Scale * scale )/ 50) * -Terrain_Direction, 0)
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
    Noise(obj, 24, 13)
    Noise(obj, 6, 20)
    Noise(obj, 2, 31)

    print("generated terrain: " + str(obj.Terrain)) 
def WritePolygonPositions(obj):
    #making tuples (x,y) out of the y positions of the future polygon vertices stored in obj.Terrain
    x = round((obj.X_Position - 100) / round(obj.dimensions[0] / obj.CFG_Terrain_X_Scale))
    endx = round((obj.X_Position + obj.dimensions[0]*1.1) / round(obj.dimensions[0] / obj.CFG_Terrain_X_Scale))
    PolygonPoints = []
    startx = x
    #Edge point
    PolygonPoints.append((0, 10000))
    while x < round(endx):
        Point = obj.Terrain[x] + obj.Y_Position
        PolygonPoints.append((x * round(obj.dimensions[0] / obj.CFG_Terrain_X_Scale) - obj.X_Position, Point))
        x += 1
    #edge point
    PolygonPoints.append(((x - 1) * round(obj.dimensions[0] / obj.CFG_Terrain_X_Scale), 10000))
    obj.GroundRelief = [(0, 600), (200, 650), (1000, 400), (1500, 400), (1800, 500), (2200, 340), (2400, 320), (3200, 200), (4000, -300), (8000, -200), (9000, -1500)] #provisorisch
    #print("THE GROUND POLYGON IS AT:", PolygonPoints)
    #print(f"drawing poly from terrain item {startx} to terrain item {x}")
